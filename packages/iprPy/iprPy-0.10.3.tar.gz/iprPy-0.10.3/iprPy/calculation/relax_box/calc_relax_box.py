#!/usr/bin/env python
# coding: utf-8

# Python script created by Lucas Hale

# Standard library imports
from pathlib import Path
import sys
import uuid
import shutil
import datetime
from copy import deepcopy

# http://www.numpy.org/
import numpy as np

# https://github.com/usnistgov/DataModelDict 
from DataModelDict import DataModelDict as DM

# https://github.com/usnistgov/atomman 
import atomman as am
import atomman.lammps as lmp
import atomman.unitconvert as uc

# https://github.com/usnistgov/iprPy
import iprPy

# Define calculation metadata
calculation_style = 'relax_box'
record_style = f'calculation_{calculation_style}'
script = Path(__file__).stem
pkg_name = f'iprPy.calculation.{calculation_style}.{script}'

def main(*args):
    """Main function  called when script is executed directly."""
    
    # Read input file in as dictionary
    with open(args[0]) as f:
        input_dict = iprPy.input.parse(f, allsingular=True)
    
    # Interpret and process input parameters
    process_input(input_dict, *args[1:])
    
    # Run relax_box to refine values
    results_dict = relax_box(input_dict['lammps_command'],
                             input_dict['initialsystem'],
                             input_dict['potential'],
                             mpi_command = input_dict['mpi_command'],
                             p_xx = input_dict['pressure_xx'],
                             p_yy = input_dict['pressure_yy'],
                             p_zz = input_dict['pressure_zz'],
                             p_xy = input_dict['pressure_xy'],
                             p_xz = input_dict['pressure_xz'],
                             p_yz = input_dict['pressure_yz'],
                             strainrange = input_dict['strainrange'])
    
    # Build and save data model of results
    record = iprPy.load_record(record_style)
    record.buildcontent(input_dict, results_dict)
    with open('results.json', 'w') as f:
        record.content.json(fp=f, indent=4)

def relax_box(lammps_command, system, potential,
              mpi_command=None, strainrange=1e-6,
              p_xx=0.0, p_yy=0.0, p_zz=0.0, p_xy=0.0, p_xz=0.0, p_yz=0.0,
              tol=1e-10, diverge_scale=3.):
    """
    Quickly refines static orthorhombic system by evaluating the elastic
    constants and the virial pressure.
    
    Parameters
    ----------
    lammps_command :str
        Command for running LAMMPS.
    system : atomman.System
        The system to perform the calculation on.
    potential : atomman.lammps.Potential
        The LAMMPS implemented potential to use.
    mpi_command : str, optional
        The MPI command for running LAMMPS in parallel.  If not given, LAMMPS
        will run serially.
    strainrange : float, optional
        The small strain value to apply when calculating the elastic
        constants (default is 1e-6).
    p_xx : float, optional
        The value to relax the x tensile pressure component to (default is
        0.0).
    p_yy : float, optional
        The value to relax the y tensile pressure component to (default is
        0.0).
    p_zz : float, optional
        The value to relax the z tensile pressure component to (default is
        0.0).
    tol : float, optional
        The relative tolerance used to determine if the lattice constants have
        converged (default is 1e-10).
    diverge_scale : float, optional
        Factor to identify if the system's dimensions have diverged.  Divergence
        is identified if either any current box dimension is greater than the
        original dimension multiplied by diverge_scale, or if any current box
        dimension is less than the original dimension divided by diverge_scale.
        (Default is 3.0).
    
    Returns
    -------
    dict
        Dictionary of results consisting of keys:
        
        - **'a_lat'** (*float*) - The relaxed a lattice constant.
        - **'b_lat'** (*float*) - The relaxed b lattice constant.
        - **'c_lat'** (*float*) - The relaxed c lattice constant.
        - **'alpha_lat'** (*float*) - The alpha lattice angle.
        - **'beta_lat'** (*float*) - The beta lattice angle.
        - **'gamma_lat'** (*float*) - The gamma lattice angle.
        - **'E_coh'** (*float*) - The cohesive energy of the relaxed system.
        - **'stress'** (*numpy.array*) - The measured stress state of the
          relaxed system.
        - **'C_elastic'** (*atomman.ElasticConstants*) - The relaxed system's
          elastic constants.
        - **'system_relaxed'** (*atomman.System*) - The relaxed system.
    
    Raises
    ------
    RuntimeError
        If system diverges or no convergence reached after 100 cycles.
    """
    
    # Flag for if values have converged
    converged = False
    
    # Define current and old systems
    system_current = deepcopy(system)
    system_old = None
    
    system.dump('atom_dump', f='initial.dump')
    
    for cycle in range(100):
        
        # Run LAMMPS and evaluate results based on system_old
        results = calc_cij(lammps_command, system_current, potential,
                           mpi_command=mpi_command,
                           p_xx=p_xx, p_yy=p_yy, p_zz=p_zz,
                           strainrange=strainrange, cycle=cycle)
        system_new = results['system_new']
        
        # Compare new and current to test for convergence
        if np.allclose(system_new.box.vects,
                       system_current.box.vects,
                       rtol=tol, atol=0):
            converged = True
            break
        
        # Compare old and new to test for double-value convergence
        elif system_old is not None and np.allclose(system_new.box.vects,
                                                    system_old.box.vects,
                                                    rtol=tol, atol=0):
            # Update current to average of old and new
            system_current.box_set(a = (system_new.box.a+system_old.box.a) / 2.,
                                   b = (system_new.box.b+system_old.box.b) / 2.,
                                   c = (system_new.box.c+system_old.box.c) / 2.,
                                   scale=True)
            # Calculate Cij for the averaged system
            results = calc_cij(lammps_command, system_current, potential,
                               mpi_command=mpi_command,
                               p_xx=p_xx, p_yy=p_yy, p_zz=p_zz, 
                               strainrange=strainrange, cycle=cycle+1)
            system_new = results['system_new']
            converged = True
            break
        
        # Test for divergence
        elif system_new.box.a < system.box.a / diverge_scale:
            raise RuntimeError('Divergence of box dimensions')
        elif system_new.box.a > system.box.a * diverge_scale:
            raise RuntimeError('Divergence of box dimensions')
        elif system_new.box.b < system.box.b / diverge_scale:
            raise RuntimeError('Divergence of box dimensions')
        elif system_new.box.b > system.box.b * diverge_scale:
            raise RuntimeError('Divergence of box dimensions')
        elif system_new.box.c < system.box.c / diverge_scale:
            raise RuntimeError('Divergence of box dimensions')
        elif system_new.box.c > system.box.c * diverge_scale:
            raise RuntimeError('Divergence of box dimensions')
        elif results['E_coh'] == 0.0:
            raise RuntimeError('Divergence: cohesive energy is 0')
        
        # If not converged or diverged, current -> old and new -> current
        else:
            system_old, system_current = system_current, system_new
    
    # Return values when converged
    if converged:
        system_new.dump('atom_dump', f='final.dump')
        
        # Build results_dict
        results_dict = {}
        results_dict['dumpfile_initial'] = 'initial.dump'
        results_dict['symbols_initial'] = system.symbols
        results_dict['dumpfile_final'] = 'final.dump'
        results_dict['symbols_final'] = system.symbols
        
        results_dict['lx'] = system_new.box.lx
        results_dict['ly'] = system_new.box.ly
        results_dict['lz'] = system_new.box.lz
        results_dict['xy'] = system_new.box.xy
        results_dict['xz'] = system_new.box.xz
        results_dict['yz'] = system_new.box.yz
        
        results_dict['E_coh'] = results['E_coh']
        results_dict['measured_pxx'] = results['measured_pxx']
        results_dict['measured_pyy'] = results['measured_pyy']
        results_dict['measured_pzz'] = results['measured_pzz']
        results_dict['measured_pxy'] = results['measured_pxy']
        results_dict['measured_pxz'] = results['measured_pxz']
        results_dict['measured_pyz'] = results['measured_pyz']
        
        return results_dict
    else:
        raise RuntimeError('Failed to converge after 100 cycles')

def calc_cij(lammps_command, system, potential,
             mpi_command=None, p_xx=0.0, p_yy=0.0, p_zz=0.0,
             strainrange=1e-6, cycle=0):
    """
    Runs cij.in LAMMPS script to evaluate Cij, and E_coh of the current system,
    and define a new system with updated box dimensions to test.
    
    Parameters
    ----------
    lammps_command :str
        Command for running LAMMPS.
    system : atomman.System
        The system to perform the calculation on.
    potential : atomman.lammps.Potential
        The LAMMPS implemented potential to use.
    mpi_command : str, optional
        The MPI command for running LAMMPS in parallel.  If not given, LAMMPS
        will run serially.
    strainrange : float, optional
        The small strain value to apply when calculating the elastic
        constants (default is 1e-6).
    p_xx : float, optional
        The value to relax the x tensile pressure component to (default is
        0.0).
    p_yy : float, optional
        The value to relax the y tensile pressure component to (default is
        0.0).
    p_zz : float, optional
        The value to relax the z tensile pressure component to (default is
        0.0).
    cycle : int, optional
        Indicates the iteration cycle of quick_a_Cij().  This is used to
        uniquely save the LAMMPS input and output files.
    
    Returns
    -------
    dict
        Dictionary of results consisting of keys:
        
        - **'E_coh'** (*float*) - The cohesive energy of the supplied system.
        - **'stress'** (*numpy.array*) - The measured stress state of the
          supplied system.
        - **'C_elastic'** (*atomman.ElasticConstants*) - The supplied system's
          elastic constants.
        - **'system_new'** (*atomman.System*) - System with updated box
          dimensions.
    
    Raises
    ------
    RuntimeError
        If any of the new box dimensions are less than zero.
    """
    # Build filedict if function was called from iprPy
    try:
        assert __name__ == pkg_name
        calc = iprPy.load_calculation(calculation_style)
        filedict = calc.filedict
    except:
        filedict = {}

    # Get lammps units
    lammps_units = lmp.style.unit(potential.units)
    
    # Define lammps variables
    lammps_variables = {}
    system_info = system.dump('atom_data', f='init.dat',
                              potential=potential,
                              return_pair_info=True)
    lammps_variables['atomman_system_pair_info'] = system_info
    
    lammps_variables['delta'] = strainrange
    lammps_variables['steps'] = 2
    
    # Write lammps input script
    template_file = 'cij.template'
    lammps_script = 'cij.in'
    template = iprPy.tools.read_calc_file(template_file, filedict)
    with open(lammps_script, 'w') as f:
        f.write(iprPy.tools.filltemplate(template, lammps_variables,
                                         '<', '>'))
    
    # Run lammps
    output = lmp.run(lammps_command, lammps_script, mpi_command=mpi_command,
                     return_style='model')
    shutil.move('log.lammps', 'cij-'+str(cycle)+'-log.lammps')
    
    # Extract LAMMPS thermo data. Each term ranges i=0-12 where i=0 is undeformed
    # The remaining values are for -/+ strain pairs in the six unique directions
    lx = uc.set_in_units(np.array(output.finds('Lx')), lammps_units['length'])
    ly = uc.set_in_units(np.array(output.finds('Ly')), lammps_units['length'])
    lz = uc.set_in_units(np.array(output.finds('Lz')), lammps_units['length'])
    xy = uc.set_in_units(np.array(output.finds('Xy')), lammps_units['length'])
    xz = uc.set_in_units(np.array(output.finds('Xz')), lammps_units['length'])
    yz = uc.set_in_units(np.array(output.finds('Yz')), lammps_units['length'])
    
    pxx = uc.set_in_units(np.array(output.finds('Pxx')), lammps_units['pressure'])
    pyy = uc.set_in_units(np.array(output.finds('Pyy')), lammps_units['pressure'])
    pzz = uc.set_in_units(np.array(output.finds('Pzz')), lammps_units['pressure'])
    pxy = uc.set_in_units(np.array(output.finds('Pxy')), lammps_units['pressure'])
    pxz = uc.set_in_units(np.array(output.finds('Pxz')), lammps_units['pressure'])
    pyz = uc.set_in_units(np.array(output.finds('Pyz')), lammps_units['pressure'])
    
    pe = uc.set_in_units(np.array(output.finds('PotEng')) / system.natoms,
                         lammps_units['energy'])
    
    # Set the six non-zero strain values
    strains = np.array([ (lx[2] -  lx[1])  / lx[0],
                         (ly[4] -  ly[3])  / ly[0],
                         (lz[6] -  lz[5])  / lz[0],
                         (yz[8] -  yz[7])  / lz[0],
                         (xz[10] - xz[9])  / lz[0],
                         (xy[12] - xy[11]) / ly[0] ])
    
    # Calculate cij using stress changes associated with each non-zero strain
    cij = np.empty((6,6))
    for i in range(6):
        delta_stress = np.array([ pxx[2*i+1]-pxx[2*i+2],
                                  pyy[2*i+1]-pyy[2*i+2],
                                  pzz[2*i+1]-pzz[2*i+2],
                                  pyz[2*i+1]-pyz[2*i+2],
                                  pxz[2*i+1]-pxz[2*i+2],
                                  pxy[2*i+1]-pxy[2*i+2] ])
        
        cij[i] = delta_stress / strains[i] 
    
    for i in range(6):
        for j in range(i):
            cij[i,j] = cij[j,i] = (cij[i,j] + cij[j,i]) / 2
    
    C = am.ElasticConstants(Cij=cij)
    
    S = C.Sij
    
    # Extract the current stress state
    stress = -1 * np.array([[pxx[0], pxy[0], pxz[0]],
                            [pxy[0], pyy[0], pyz[0]],
                            [pxz[0], pyz[0], pzz[0]]])
    
    s_xx = stress[0,0] + p_xx
    s_yy = stress[1,1] + p_yy
    s_zz = stress[2,2] + p_zz
    
    new_a = system.box.a / (S[0,0]*s_xx + S[0,1]*s_yy + S[0,2]*s_zz + 1)
    new_b = system.box.b / (S[1,0]*s_xx + S[1,1]*s_yy + S[1,2]*s_zz + 1)
    new_c = system.box.c / (S[2,0]*s_xx + S[2,1]*s_yy + S[2,2]*s_zz + 1)
    
    if new_a <= 0 or new_b <= 0 or new_c <=0:
        raise RuntimeError('Divergence of box dimensions to <= 0')
    
    system_new = deepcopy(system)
    system_new.box_set(a=new_a, b=new_b, c=new_c, scale=True)
    
    results_dict = {}
    results_dict['E_coh'] = pe[0]
    results_dict['system_new'] = system_new
    results_dict['measured_pxx'] = pxx[0]
    results_dict['measured_pyy'] = pyy[0]
    results_dict['measured_pzz'] = pzz[0]
    results_dict['measured_pxy'] = pxy[0]
    results_dict['measured_pxz'] = pxz[0]
    results_dict['measured_pyz'] = pyz[0]
    return results_dict

def process_input(input_dict, UUID=None, build=True):
    """
    Processes str input parameters, assigns default values if needed, and
    generates new, more complex terms as used by the calculation.
    
    Parameters
    ----------
    input_dict :  dict
        Dictionary containing the calculation input parameters with string
        values.  The allowed keys depends on the calculation style.
    UUID : str, optional
        Unique identifier to use for the calculation instance.  If not 
        given and a 'UUID' key is not in input_dict, then a random UUID4 
        hash tag will be assigned.
    build : bool, optional
        Indicates if all complex terms are to be built.  A value of False
        allows for default values to be assigned even if some inputs 
        required by the calculation are incomplete.  (Default is True.)
    """
    # Set script's name
    input_dict['script'] = script
    
    # Set calculation UUID
    if UUID is not None:
        input_dict['calc_key'] = UUID
    else:
        input_dict['calc_key'] = input_dict.get('calc_key', str(uuid.uuid4()))
    
    # Set default input/output units
    iprPy.input.subset('units').interpret(input_dict)
    
    # These are calculation-specific default strings
    input_dict['sizemults'] = input_dict.get('sizemults', '1 1 1')
    
    # These are calculation-specific default booleans
    # None for this calculation
    
    # These are calculation-specific default integers
    # None for this calculation
    
    # These are calculation-specific default unitless floats
    input_dict['strainrange'] = float(input_dict.get('strainrange', 1e-6))
    input_dict['temperature'] = 0.0
    
    # These are calculation-specific default floats with units
    input_dict['pressure_xx'] = iprPy.input.value(input_dict, 'pressure_xx',
                                    default_unit=input_dict['pressure_unit'],
                                    default_term='0.0 GPa')
    input_dict['pressure_yy'] = iprPy.input.value(input_dict, 'pressure_yy',
                                    default_unit=input_dict['pressure_unit'],
                                    default_term='0.0 GPa')
    input_dict['pressure_zz'] = iprPy.input.value(input_dict, 'pressure_zz',
                                    default_unit=input_dict['pressure_unit'],
                                    default_term='0.0 GPa')
    input_dict['pressure_xy'] = iprPy.input.value(input_dict, 'pressure_xy',
                                    default_unit=input_dict['pressure_unit'],
                                    default_term='0.0 GPa')
    input_dict['pressure_xz'] = iprPy.input.value(input_dict, 'pressure_xz',
                                    default_unit=input_dict['pressure_unit'],
                                    default_term='0.0 GPa')
    input_dict['pressure_yz'] = iprPy.input.value(input_dict, 'pressure_yz',
                                    default_unit=input_dict['pressure_unit'],
                                    default_term='0.0 GPa')
    
    # Check lammps_command and mpi_command
    iprPy.input.subset('lammps_commands').interpret(input_dict)
    
    # Load potential
    iprPy.input.subset('lammps_potential').interpret(input_dict)
    
    # Load system
    iprPy.input.subset('atomman_systemload').interpret(input_dict, build=build)
    
    # Construct initialsystem by manipulating ucell system
    iprPy.input.subset('atomman_systemmanipulate').interpret(input_dict, build=build)
        
if __name__ == '__main__':
    main(*sys.argv[1:])