#!/usr/bin/env python
import os
import sys
import numpy as np
from copy import deepcopy

import iprPy

import atomman as am
import atomman.lammps as lmp
import atomman.unitconvert as uc

__calc_name__ = os.path.splitext(os.path.basename(__file__))[0]
assert __calc_name__[:5] == 'calc_', 'Calculation file name must start with "calc_"'
__calc_type__ = __calc_name__[5:]

def main(*args):    
    """Main function for running calculation"""

    #Read in parameters from input file
    with open(args[0]) as f:
        input_dict = iprPy.calculation_read_input(__calc_type__, f, *args[1:])
        
    #Read in potential
    potential = lmp.Potential(input_dict['potential'], input_dict['potential_dir'])            
    
    #Get axes info
    axes = np.array([input_dict['x-axis'], input_dict['y-axis'], input_dict['z-axis']])
    
    #Perform crss calculation
    results_dict = crss(input_dict['lammps_command'], input_dict['initial_system'], 
                        potential, input_dict['symbols'], input_dict['C'], 
                        mpi_command=input_dict['mpi_command'], 
                        chi=input_dict['chi_angle'], sigma=input_dict['sigma'], 
                        tau_1=input_dict['tau_1'], tau_2=input_dict['tau_2'], 
                        press=input_dict['press'], rss_steps=input_dict['rss_steps'],
                        axes=axes)
    
    #Save data model of results 
    results = iprPy.calculation_data_model(__calc_type__, input_dict, results_dict)
    with open('results.json', 'w') as f:
        results.json(fp=f, indent=4)    
        

def crss(lammps_command, system, potential, symbols, C, mpi_command=None, 
         chi=0.0, sigma=0.0, tau_1=0.0, tau_2=0.0, press=0.0, rss_steps=0,
         axes=None, etol=0.0, ftol=1e-6, maxiter=100000, maxeval=100000):
    """
    Performs a LAMMPS simulation for evaluating the critical resolved shear stress of 
    a dislocation monopole system for a given stress orientiation. The stress states 
    defined by  this calculation are for a dislocation with line direction parallel to 
    the z-axis, and primary slip plane in the xz-plane.
    
    Parameters:
    lammps_command -- command for running LAMMPS.
    system -- atomman.System to add the point defect to.
    potential -- atomman.lammps.Potential representation of a LAMMPS implemented potential.
    symbols -- list of element-model symbols for the Potential that correspond to system's atypes.
    C -- an atomman.ElasticConstants representation of the system's elastic 
         constants matrix.

    Keyword Parameters:
    mpi_command -- MPI command for running LAMMPS in parallel. Default value is None (serial run).  
    chi -- the angle (in degrees) between the most resolved shear stress plane 
           and the slip plane (i.e. xz-plane). Default value is 0.0.
    sigma -- the magnitude of the shear stress to apply along the most resolved 
             shear stress plane. Default value is 0.0.
    tau_1 -- the magnitude of one of the independent shear stresses perpendicular 
             to the most resolved shear stress plane. Default value is 0.0.
    tau_2 -- the magnitude of one of the independent shear stresses perpendicular 
             to the most resolved shear stress plane. Default value is 0.0.
    press -- the magnitude of the hydrostatic pressure. Default value is 0.0.
    number_of_steps -- number of times to apply the incremental delta_strain to the system. Default value is 0.   
    axes -- crystallographic axes/transformation cosines associated with the 
            system's orientation. If given, then C is transformed accordingly.   
    etol -- energy tolerance to use for the LAMMPS minimization. Default value is 0.0 (i.e. only uses ftol). 
    ftol -- force tolerance to use for the LAMMPS minimization. Default value is 1e-6.
    maxiter -- the maximum number of iterations for the LAMMPS minimization. Default value is 100000.
    maxeval -- the maximum number of evaluations for the LAMMPS minimization. Default value is 100000.   
    """ 
    #Convert stress state parameters to strain states
    strains = crss_strain_states(C, chi=chi, sigma=sigma, tau_1=tau_1, tau_2=tau_2, press=press, axes=axes)
    
    #Retrieve strain states
    delta_strain = strains['sigma_strain']
    initial_strain = strains['tau_strain']
    
    #Define hold_atypes as the upper half of atom types
    hold_atypes = range(system.natypes/2+1, system.natypes+1)
    
    #Strain the system
    results = strain_system(lammps_command, system, potential, symbols, mpi_command=mpi_command, 
                            delta_strain=delta_strain, initial_strain=initial_strain, 
                            hold_atypes=hold_atypes, number_of_steps=rss_steps,
                            etol=etol, ftol=ftol, maxiter=maxiter, maxeval=maxeval)
    
    #Compute the resolved shear stress as the magnitude of sigma each step
    results['rss'] = sigma * results['strain_step']
    
    #Identify potential relaxation events by looking at second derivative of potential energy 
    diff2 = np.diff(results['E_total'], n=2)
    results['relax_indices'] = np.where(diff2 < 0)[0] + 2
    
    #Return the results
    return results
    
def crss_strain_states(C, chi=0.0, sigma=0.0, tau_1=0.0, tau_2=0.0, press=0.0, axes=None):
    """
    Computes the strain states associated with commonly applied stress states for 
    evaluating the critically resolved shear stress. The stress states defined by  
    this calculation are for a dislocation with line direction parallel to the 
    z-axis, and a primary xz-slip plane.
    
    Parameters:
    C -- an atomman.ElasticConstants representation of the system's elastic 
         constants matrix.

    Keyword Parameters:
    chi -- the angle (in degrees) between the most resolved shear stress plane 
           and the slip plane (i.e. xz-plane). Default value is 0.0.
    sigma -- the magnitude of the shear stress to apply along the most resolved 
             shear stress plane. Default value is 0.0.
    tau_1 -- the magnitude of one of the independent shear stresses perpendicular 
             to the most resolved shear stress plane. Default value is 0.0.
    tau_2 -- the magnitude of one of the independent shear stresses perpendicular 
             to the most resolved shear stress plane. Default value is 0.0.
    press -- the magnitude of the hydrostatic pressure. Default value is 0.0.
    axes -- crystallographic axes/transformation cosines associated with the 
            system's orientation. If given, then C is transformed accordingly.
    """
    
    if axes is not None:
        C = C.transform(axes)
    
    #Define stress states
    sigma = np.array([[   0.0,   0.0,   0.0],
                      [   0.0,   0.0, sigma],
                      [   0.0, sigma,   0.0]])

    tau_1 = np.array([[-tau_1,   0.0,   0.0],
                      [   0.0, tau_1,   0.0],
                      [   0.0,   0.0,   0.0]])
            
    tau_2 = np.array([[   0.0,   0.0,   0.0],
                      [   0.0, tau_2,   0.0],
                      [   0.0,   0.0,-tau_2]])
                
    press = np.array([[-press,   0.0,   0.0],
                      [   0.0,-press,   0.0],
                      [   0.0,   0.0,-press]])
                    
    #Sum up the tau initial terms
    tau = tau_1 + tau_2 + press            
                    
    #Convert chi to radians
    chi = chi/180. * np.pi

    #Rotate stress arrays by chi
    T = np.array([[ np.cos(chi), np.sin(chi), 0.0],
                  [-np.sin(chi), np.cos(chi), 0.0],
                  [         0.0,         0.0, 1.0]])
    sigma = np.einsum('il,jm,lm->ij', T, T, sigma)
    tau =   np.einsum('il,jm,lm->ij', T, T, tau)

    #Convert to Voigt form
    sigma6 = np.array([sigma[0,0], sigma[1,1], sigma[2,2], 
                       sigma[1,2], sigma[0,2], sigma[0,1]])
    tau6 = np.array([tau[0,0], tau[1,1], tau[2,2], 
                     tau[1,2], tau[0,2], tau[0,1]])

    #Solve for elastic states
    sigma_strain6 = C.Sij.dot(sigma6)
    tau_strain6 = C.Sij.dot(tau6)
    
    return {'sigma_strain': sigma_strain6, 'tau_strain': tau_strain6}

def strain_system(lammps_command, system, potential, symbols, mpi_command=None, 
                  delta_strain=np.zeros(6), initial_strain=np.zeros(6), 
                  hold_atypes=[], number_of_steps=0,
                  etol=0.0, ftol=1e-5, maxiter=10000, maxeval=100000):
    """
    Applies strains to an atomic system in LAMMPS and relaxes the energy.
    
    Arguments:
    lammps_command -- command for running LAMMPS.
    system -- atomman.System to add the point defect to.
    potential -- atomman.lammps.Potential representation of a LAMMPS implemented potential.
    symbols -- list of element-model symbols for the Potential that correspond to system's atypes.
    
    Keyword Arguments:
    mpi_command -- MPI command for running LAMMPS in parallel. Default value is None (serial run).  
    delta_strain -- strain state in 6 term Voigt to apply incrementally. Default value is all zeros.
    initial_strain -- strain state in 6 term Voigt to apply to the system prior to the incremental delta_strain. 
                      Default value is all zeros.
    number_of_steps -- number of times to apply the incremental delta_strain to the system. Default value is 0.    
    hold_atypes -- list of atom types that should be held fixed (not allowed to relax). Default value is [].    
    etol -- energy tolerance to use for the LAMMPS minimization. Default value is 0.0 (i.e. only uses ftol). 
    ftol -- force tolerance to use for the LAMMPS minimization. Default value is 1e-6.
    maxiter -- the maximum number of iterations for the LAMMPS minimization. Default value is 100000.
    maxeval -- the maximum number of evaluations for the LAMMPS minimization. Default value is 100000.    
    """    
    
    if am.tools.is_int(hold_atypes):
        hold_atypes = np.array([hold_atypes])
    else:
        hold_atypes = np.asarray(hold_atypes)
    
    if len(hold_atypes) == 0:
        hold_info = ''
    else:
        move_atypes = np.setdiff1d(np.arange(1, system.natypes+1), hold_atypes)
        hold_info = '\n'.join(['', '#Fix boundary region atoms',
                               'group           move type ' + ' '.join(np.char.mod('%d', move_atypes)),
                               'group           hold subtract all move',
                               'fix             nomove hold setforce 0.0 0.0 0.0', ''])

    #Get lammps units
    lammps_units = lmp.style.unit(potential.units)

    #Read LAMMPS input template
    with open('strain_system.template') as f:
        template = f.read()
    
    #Define lammps variables
    lammps_variables = {}
    lammps_variables['atomman_system_info'] = lmp.atom_data.dump(system, 'initial.dat', 
                                                                 units=potential.units, 
                                                                 atom_style=potential.atom_style)
    lammps_variables['atomman_pair_info'] =   potential.pair_info(symbols)
    lammps_variables['hold_info'] =           hold_info
    lammps_variables['energy_tolerance'] =    etol
    lammps_variables['force_tolerance'] =     uc.get_in_units(ftol, lammps_units['force'])
    lammps_variables['maximum_iterations'] =  maxiter
    lammps_variables['maximum_evaluations'] = maxeval
    lammps_variables['number_of_steps'] =     number_of_steps + 1   
    lammps_variables['delta_strain_xx'] =     delta_strain[0]
    lammps_variables['delta_strain_yy'] =     delta_strain[1]
    lammps_variables['delta_strain_zz'] =     delta_strain[2]
    lammps_variables['delta_strain_xy'] =     delta_strain[5]
    lammps_variables['delta_strain_xz'] =     delta_strain[4]
    lammps_variables['delta_strain_yz'] =     delta_strain[3]
    lammps_variables['initial_strain_xx'] =   initial_strain[0]
    lammps_variables['initial_strain_yy'] =   initial_strain[1]
    lammps_variables['initial_strain_zz'] =   initial_strain[2]
    lammps_variables['initial_strain_xy'] =   initial_strain[5]
    lammps_variables['initial_strain_xz'] =   initial_strain[4]
    lammps_variables['initial_strain_yz'] =   initial_strain[3]
    
    #Write lammps input script
    with open('strain_system.in', 'w') as f:
        f.write('\n'.join(iprPy.tools.fill_template(template, lammps_variables, '<', '>')))

    #run lammps to relax perfect.dat
    output = lmp.run(lammps_command, 'strain_system.in', mpi_command)
    
    #Extract LAMMPS thermo data.
    lammps_step = np.asarray(output.finds('Step'), dtype=int)[1::2]
    E_total =     uc.set_in_units(output.finds('PotEng'), lammps_units['energy']  )[1::2]
    p_xx =        uc.set_in_units(output.finds('Pxx'),    lammps_units['pressure'])[1::2]
    p_yy =        uc.set_in_units(output.finds('Pyy'),    lammps_units['pressure'])[1::2]
    p_zz =        uc.set_in_units(output.finds('Pzz'),    lammps_units['pressure'])[1::2]
    p_xy =        uc.set_in_units(output.finds('Pxy'),    lammps_units['pressure'])[1::2]
    p_xz =        uc.set_in_units(output.finds('Pxz'),    lammps_units['pressure'])[1::2]
    p_yz =        uc.set_in_units(output.finds('Pyz'),    lammps_units['pressure'])[1::2]
    strain_step = np.asarray(output.finds('s_step'), dtype=int)[1::2]
    
    return {'lammps_step':lammps_step, 'E_total':E_total, 'p_xx':p_xx, 'p_yy':p_yy, 'p_zz':p_zz, 
            'p_xy':p_xy, 'p_xz':p_xz, 'p_yz':p_yz, 'strain_step':strain_step}

if __name__ == '__main__':
    main(*sys.argv[1:])              