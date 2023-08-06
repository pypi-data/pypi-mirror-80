## Input script parameters

This is a list of the input parameter names recognized by the calculation script.

### Command lines for LAMMPS and MPI

Provides the external commands for running LAMMPS and MPI.

- __lammps_command__: the path to the executable for running LAMMPS on your system.  Don't include command line options.

- __mpi_command__: the path to the MPI executable and any command line options to use for calling LAMMPS to run in parallel on your system. Default value is None (run LAMMPS as a serial process).

### Potential definition and directory containing associated files

Provides the information associated with an interatomic potential implemented for LAMMPS.

- __potential_file__: the path to the potential_LAMMPS data model used by atomman to generate the proper LAMMPS commands for an interatomic potential.

- __potential_dir__: the path to the directory containing any potential artifacts (eg. eam.alloy setfl files) that are used. If not given, then any required files are expected to be in the working directory where the calculation is executed.

### Initial system configuration to load

Provides the information associated with loading an atomic configuration.

- __load_file__: the path to the initial configuration file being read in.

- __load_style__: the style/format for the load_file.  The style can be any file type supported by atomman.load()

- __load_options__: a list of key-value pairs for the optional style-dependent arguments used by atomman.load().

- __family__: specifies the configuration family to associate with the loaded file.  This is typically a crystal structure/prototype identifier that helps with linking calculations on the same material together.  If not given and the load_style is system_model, then the family will be taken from the file if included.  Otherwise, the family will be taken as load_file stripped of path and extension.

- __symbols__: a space-delimited list of the potential's atom-model symbols to associate with the loaded system's atom types.  Required if load_file does not contain this information.

- __box_parameters__: allows for the specification of new box parameters to scale the loaded configuration by.  This is useful for running calculations based on prototype configurations that do not contain material-specific dimensions.  Can be given either as a list of three or six numbers, with an optional unit of length at the end.  If the unit of length is not given, the specified length_unit (below) will be used.

  - a b c (unit): for orthogonal boxes.

  - a b c alpha beta gamma (unit): for triclinic boxes.  The angles are taken in degrees.

### System manipulations

Performs simple manipulations on the loaded initial system.

- __a_uvw, b_uvw, c_uvw__: are crystallographic Miller vectors to rotate the system by such that the rotated system's a, b, c box vectors correspond to the specified Miller vectors of the loaded configuration.  Using crystallographic vectors for rotating ensures that if the initial configuration is periodic in all three directions, the resulting rotated configuration can be as well with no boundary incompatibilities.  Default values are '1 0 0', '0 1 0', and '0 0 1', respectively (i.e. no rotation).

- __atomshift__: a vector positional shift to apply to all atoms.  The shift is relative to the size of the system after rotating, but before sizemults have been applied.  This allows for the same relative shift regardless of box_parameters and sizemults.  Default value is '0.0 0.0 0.0' (i.e. no shift).

- __sizemults__: multiplication parameters for making a supercell of the loaded system.  This may either be a list of three or six integer numbers.  Default value is '3 3 3'.

  - ma mb mc: multipliers for each box axis.  Values can be positive or negative indicating the direction relative to the original box's origin for shifting/multiplying the system.  

  - na pa nb pb nc pc: negative, positive multiplier pairs for each box axis.  The n terms must be less than or equal to zero, and the p terms greater than or equal to zero.  This allows for expanding the system in both directions relative to the original box's origin.

### Defect Parameters

Defines the defect system to construct and analyze.

- __pointdefect_file__: the path to a point_defect record file that contains a set of input parameters associated with a specific point defect or set of point defects. In particular, the point_defect record contains values for the pointdefect_type, pointdefect_atype, pointdefect_pos, pointdefect_dumbbell_vect, and pointdefect_scale parameters. As such, those parameters cannot be specified separately if pointdefect_model is given.
  
- __pointdefect_type__: indicates which type of point defect to generate.

  - 'v' or 'vacancy': generate a vacancy.

  - 'i' or 'interstitial': generate a position-based interstitial.

  - 's' or 'substitutional': generate a substitutional.

  - 'd', 'db' or 'dumbbell': generate a dumbbell interstitial.

- __pointdefect_atype__: indicates the integer atom type to assign to an interstitial, substitutional, or dumbbell interstitial atom.

- __pointdefect_pos__: indicates the position where the point defect is to be placed. For the interstitial type, this cannot correspond to a current atom's position. For the other styles, this must correspond to a current atom's position.

- __pointdefect_dumbbell_vect__: specifies the dumbbell vector to use for a dumbbell interstitial. The atom defined by pointdefect_pos is shifted by -pointdefect_dumbbell_vect, and the inserted interstitial atom is placed at pointdefect_pos + pointdefect_dumbbell_vect.

- __pointdefect_scale__: Boolean indicating if pointdefect_pos and pointdefect_dumbbell_vect are taken as absolute Cartesian vectors, or taken as scaled values relative to the loaded system. Default value is False.

### Units for input/output values

Specifies the units for various physical quantities to use when saving values to the results record file. Also used as the default units for parameters in this input parameter file.

- __length_unit__: defines the unit of length for results, and input parameters if not directly specified.  Default value is 'angstrom'.

- __energy_unit__: defines the unit of energy for results, and input parameters if not directly specified.  Default value is 'eV'.

- __pressure_unit__: defines the unit of pressure for results, and input parameters if not directly specified.  Default value is 'GPa'.

- __force_unit__: defines the unit of pressure for results, and input parameters if not directly specified.  Default value is 'eV/angstrom'.

### Run parameters

Provides parameters specific to the calculation at hand.

- __energytolerance__: specifies the energy tolerance to use for the minimization.  This value is unitless and corresponds to the etol term for the [LAMMPS minimize command.](http://lammps.sandia.gov/doc/minimize.html)  Default value is 0.

- __forcetolerance__: specifies the force tolerance to use for the minimization.  This value is in force units and corresponds to the ftol term for the [LAMMPS minimize command.](http://lammps.sandia.gov/doc/minimize.html)  Default value is '1.0e-10 eV/angstrom'.

- __maxiterations__: specifies the maximum number of iterations to use for the minimization. This value corresponds to the maxiter term for the [LAMMPS minimize command.](http://lammps.sandia.gov/doc/minimize.html)  Default value is 1000.

- __maxevaluations__: specifies the maximum number of iterations to use for the minimization. This value corresponds to the maxeval term for the [LAMMPS minimize command.](http://lammps.sandia.gov/doc/minimize.html)  Default value is 10000.

- __maxatommotion__: specifies the maximum distance that any atom can move during a minimization iteration. This value is in units length and corresponds to the dmax term for the [LAMMPS min_modify command.](http://lammps.sandia.gov/doc/min_modify.html)  Default value is '0.01 angstrom'.