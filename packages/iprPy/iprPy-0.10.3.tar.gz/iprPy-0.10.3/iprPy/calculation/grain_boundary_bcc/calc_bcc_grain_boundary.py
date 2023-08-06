#!/usr/bin/env python

#Standard library imports
import os
import sys
import uuid
import shutil
from multiprocessing import Pool

#http://www.numpy.org/
import numpy as np

#https://github.com/usnistgov/DataModelDict 
from DataModelDict import DataModelDict as DM

#https://github.com/usnistgov/atomman 
import atomman as am
import atomman.lammps as lmp
import atomman.unitconvert as uc

#https://github.com/usnistgov/iprPy
import iprPy

#Automatically identify the calculation's name
__calc_name__ = os.path.splitext(os.path.basename(__file__))[0]  
assert __calc_name__[:5] == 'calc_', 'Calculation file name must start with "calc_"' 
__calc_type__ = __calc_name__[5:]

def main(pool, *args):
    """Main function for running calculation"""
    
    #Read in parameters from input file
    with open(args[0]) as f:
        input_dict = read_input(f, *args[1:])
        
    interpret_input(input_dict)
    
    #Identify number of steps to take in each direction
    Lx =     input_dict['alat'] * np.linalg.norm(input_dict['axes_1'][0])
    Lz = 2 * input_dict['alat'] * np.linalg.norm(input_dict['axes_1'][2])
    max_x = int(Lx / input_dict['x_stepsize'])
    max_z = int(Lz / input_dict['z_stepsize'])
    
    #Initialize lists for results
    energies = []
    xshifts = []
    zshifts = []
    
    #Iterate over all x, z shift combinations
    for i in xrange(max_x):
        for j in xrange(max_z):
            
            #Set calculation arguments and keyword arguments
            calc_args = (input_dict['lammps_command'], 
                         input_dict['potential'], 
                         input_dict['symbols'], 
                         input_dict['alat'],
                         input_dict['axes_1'],
                         input_dict['axes_2'],
                         input_dict['E_coh'])
            calc_kwargs = {'mpi_command': input_dict['mpi_command'],
                           'xshift':      input_dict['x_stepsize'] * i,
                           'zshift':      input_dict['z_stepsize'] * j}
            xshifts.append(calc_kwargs['xshift'])
            zshifts.append(calc_kwargs['zshift'])
            
            #Submit gb_energy call to pool
            energies.append(pool.apply_async(gb_energy, args=calc_args, kwds=calc_kwargs))
    
    #Finish running and get results
    pool.close()
    pool.join()
    for i in xrange(len(energies)):
        energies[i] = energies[i].get()
    
    #Collect results in results_dict
    results_dict = {}
    results_dict['E_gb'] = energies
    results_dict['xshifts'] = xshifts
    results_dict['zshifts'] = zshifts
    
    #Find minimum energy
    energies = np.array(energies)
    xshifts = np.array(xshifts)
    zshifts = np.array(zshifts)
    results_dict['min_E_gb'] = energies.min()
    results_dict['xshift_min'] = xshifts[energies==results_dict['min_E_gb']][0]
    results_dict['zshift_min'] = zshifts[energies==results_dict['min_E_gb']][0]
    
    #Save data model of results 
    results = data_model(input_dict, results_dict)
    with open('results.json', 'w') as f:
        results.json(fp=f, indent=4) 
    
def gb_energy(lammps_command, potential, symbols, alat, axes_1, axes_2, E_coh,
              mpi_command=None, xshift=0.0, zshift=0.0):
    """Computes the grain boundary energy using the grain_boundary.in LAMMPS script"""
    
    axes_1 = np.asarray(axes_1, dtype=int)
    axes_2 = np.asarray(axes_2, dtype=int)
    lx = alat * np.linalg.norm(axes_1[0])
    lz = 2 * alat * np.linalg.norm(axes_1[2])
    mesh_dir = 'mesh-%.8f-%.8f' %(xshift, zshift) 
    if not os.path.isdir(mesh_dir):
        os.makedirs(mesh_dir)   
    
    #Get lammps units
    lammps_units = lmp.style.unit(potential.units)
    
    #Define lammps variables
    lammps_variables = {}
    
    lammps_variables['units'] =             potential.units
    lammps_variables['atom_style'] =        potential.atom_style
    lammps_variables['atomman_pair_info'] = potential.pair_info(symbols)
    lammps_variables['alat'] =              uc.get_in_units(alat,   lammps_units['length'])
    lammps_variables['xsize'] =             uc.get_in_units(lx,     lammps_units['length'])
    lammps_variables['zsize'] =             uc.get_in_units(lz,     lammps_units['length'])
    lammps_variables['xshift'] =            uc.get_in_units(xshift, lammps_units['length'])
    lammps_variables['zshift'] =            uc.get_in_units(zshift, lammps_units['length'])
    lammps_variables['x_axis_1'] =          str(axes_1[0]).strip('[] ')
    lammps_variables['y_axis_1'] =          str(axes_1[1]).strip('[] ')
    lammps_variables['z_axis_1'] =          str(axes_1[2]).strip('[] ')
    lammps_variables['x_axis_2'] =          str(axes_2[0]).strip('[] ')
    lammps_variables['y_axis_2'] =          str(axes_2[1]).strip('[] ')
    lammps_variables['z_axis_2'] =          str(axes_2[2]).strip('[] ')
    lammps_variables['mesh_dir'] =          'mesh-%.8f-%.8f' %(xshift, zshift) 
    
    #Fill in mod.template files
    with open('grain_boundary.template') as template_file:
        template = template_file.read()
    lammps_input = os.path.join(mesh_dir, 'grain_boundary.in')
    with open(lammps_input, 'w') as in_file:
        in_file.write(iprPy.tools.filltemplate(template, lammps_variables, '<', '>'))
        
    output = lmp.run(lammps_command, lammps_input, mpi_command)
    
    #Extract output values
    try:
        E_total = uc.set_in_units(output.finds('c_eatoms')[-1], lammps_units['energy'])
        natoms = output.finds('v_natoms')[-1]
    except:
        E_total = uc.set_in_units(output.finds('eatoms')[-1], lammps_units['energy'])
        natoms = output.finds('natoms')[-1]
        
    #Compute grain boundary energy
    E_gb = (E_total - E_coh*natoms) / (lx * lz)
    
    return E_gb

def read_input(f, UUID=None):
    """Reads the calc_*.in input commands for this calculation."""
    
    #Read input file in as dictionary
    input_dict = iprPy.tools.parseinput(f, allsingular=True)
    
    #set calculation UUID
    if UUID is not None: input_dict['calc_key'] = UUID
    else: input_dict['calc_key'] = input_dict.get('calc_key', str(uuid.uuid4()))
    
    #Verify required terms are defined
    assert 'lammps_command' in input_dict, 'lammps_command value not supplied'
    assert 'potential_file' in input_dict, 'potential_file value not supplied'
    assert 'symbols' in input_dict,        'symbols value not supplied'
    assert 'x_stepsize' in input_dict,     'x_stepsize value not supplied'
    assert 'z_stepsize' in input_dict,     'z_stepsize value not supplied'
    assert 'alat' in input_dict,           'alat value not supplied'
    assert 'E_coh' in input_dict,          'E_coh value not supplied'
    
    #Assign default values to undefined terms
    iprPy.input.units(input_dict)

    input_dict['mpi_command'] = input_dict.get('mpi_command', None)
    input_dict['potential_dir'] =  input_dict.get('potential_dir',  '')
    
    input_dict['symbols'] = input_dict['symbols'].split()
    
    iprPy.input.axes(input_dict, x_axis='x_axis_1', y_axis='y_axis_1', z_axis='z_axis_1')
    iprPy.input.axes(input_dict, x_axis='x_axis_2', y_axis='y_axis_2', z_axis='z_axis_2')
    
    input_dict['axes_1'] = np.array([input_dict['x_axis_1'], input_dict['y_axis_1'], input_dict['z_axis_1']])
    input_dict['axes_2'] = np.array([input_dict['x_axis_2'], input_dict['y_axis_2'], input_dict['z_axis_2']])
    input_dict['gb_angle'] = am.tools.vect_angle(input_dict['axes_1'][0], input_dict['axes_2'][0])
    
    #these are terms with units
    input_dict['x_stepsize'] = iprPy.input.value(input_dict, 'x_stepsize', default_unit=input_dict['length_unit'])
    input_dict['z_stepsize'] = iprPy.input.value(input_dict, 'z_stepsize', default_unit=input_dict['length_unit'])
    input_dict['alat'] =       iprPy.input.value(input_dict, 'alat',       default_unit=input_dict['length_unit'])
    input_dict['E_coh'] =      iprPy.input.value(input_dict, 'E_coh',      default_unit=input_dict['energy_unit'])
    
    return input_dict
     
def interpret_input(input_dict):
    with open(input_dict['potential_file']) as f:
        input_dict['potential'] = lmp.Potential(f, input_dict['potential_dir'])
        
    iprPy.input.system_family(input_dict)
    
    iprPy.input.ucell(input_dict)
    
    iprPy.input.initialsystem(input_dict)
    
def data_model(input_dict, results_dict=None):
    """Creates a DataModelDict containing the input and results data""" 
    
    #Create the root of the DataModelDict
    output = DM()
    output['calculation-grain-boundary-search'] = calc = DM()
    
    #Assign uuid
    calc['key'] = input_dict['calc_key']
    calc['calculation'] = DM()
    calc['calculation']['script'] = __calc_name__
    
    calc['calculation']['run-parameter'] = run_params = DM()
    
    run_params['grain-boundary-angle'] = input_dict['gb_angle']
    run_params['x-step-size'] = DM()
    run_params['x-step-size']['value'] = uc.get_in_units(input_dict['x_stepsize'], input_dict['length_unit'])
    run_params['x-step-size']['unit']  = input_dict['length_unit']
    run_params['z-step-size'] = DM()
    run_params['z-step-size']['value'] = uc.get_in_units(input_dict['z_stepsize'], input_dict['length_unit'])
    run_params['z-step-size']['unit']  = input_dict['length_unit']
    
    #Copy over potential data model info
    calc['potential'] = DM()
    calc['potential']['key'] = input_dict['potential'].key
    calc['potential']['id'] = input_dict['potential'].id
    
    #Save info on system file loaded
    calc['grain-1'] = DM()
    calc['grain-1']['crystallographic-axes'] = DM()
    calc['grain-1']['crystallographic-axes']['x-axis'] = input_dict['x_axis_1']
    calc['grain-1']['crystallographic-axes']['y-axis'] = input_dict['y_axis_1']
    calc['grain-1']['crystallographic-axes']['z-axis'] = input_dict['z_axis_1']
    
    calc['grain-2'] = DM()
    calc['grain-2']['crystallographic-axes'] = DM()
    calc['grain-2']['crystallographic-axes']['x-axis'] = input_dict['x_axis_2']
    calc['grain-2']['crystallographic-axes']['y-axis'] = input_dict['y_axis_2']
    calc['grain-2']['crystallographic-axes']['z-axis'] = input_dict['z_axis_2']
    
    if results_dict is None:
        calc['status'] = 'not calculated'
    else:
        #List energy for each position
        calc['energy-shift-relation'] = DM()
        calc['energy-shift-relation']['E_gb'] = DM()
        calc['energy-shift-relation']['E_gb']['value'] = list(uc.get_in_units(results_dict['E_gb'], 'J/m^2'))
        calc['energy-shift-relation']['E_gb']['unit'] =  'J/m^2'
        calc['energy-shift-relation']['xshift'] = DM()
        calc['energy-shift-relation']['xshift']['value'] = list(uc.get_in_units(results_dict['xshifts'], input_dict['length_unit']))
        calc['energy-shift-relation']['xshift']['unit'] =  input_dict['length_unit']
        calc['energy-shift-relation']['zshift'] = DM()
        calc['energy-shift-relation']['zshift']['value'] = list(uc.get_in_units(results_dict['zshifts'], input_dict['length_unit']))
        calc['energy-shift-relation']['zshift']['unit'] =  input_dict['length_unit']
        
        calc['lowest-energy'] = DM()
        calc['lowest-energy']['E_gb'] = DM()
        calc['lowest-energy']['E_gb']['value'] = uc.get_in_units(results_dict['min_E_gb'], 'J/m^2')
        calc['lowest-energy']['E_gb']['unit'] = 'J/m^2'

    return output

if __name__ == '__main__':
    pool = Pool()
    main(pool, *sys.argv[1:]) 