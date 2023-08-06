## Method and Theory

First, an initial system is generated.  This is accomplished using atomman.defect.StackingFault, which

1. Starts with a unit cell system.

2. Generates a transformed system by rotating the unit cell such that the new
   system's box vectors correspond to crystallographic directions, and filled
   in with atoms to remain a perfect bulk cell when the three boundaries are
   periodic.

3. All atoms are shifted by a fractional amount of the box vectors if needed.

4. A supercell system is constructed by combining multiple replicas of the
   transformed system.

5. The system is then cut by making one of the box boundaries non-periodic.  A limitation placed on the calculation is that the normal to the cut plane must correspond to one of the three Cartesian ($x$, $y$, or $z$) axes.  If true, then of the system's three box vectors ($\vec{a}$, $\vec{b}$, and $\vec{c}$), two will be parallel to the plane, and the third will not.  The non-parallel box vector is called the cutboxvector, and for LAMMPS compatible systems, the following conditions can be used to check the system's compatibility:

   - cutboxvector = 'c': all systems allowed.

   - cutboxvector = 'b': the system's yz tilt must be zero.

   - cutboxvector = 'a': the system's xy and xz tilts must be zero.

A LAMMPS simulation performs an energy/force minimization on the system where the atoms are confined to only relax along the Cartesian direction normal to the cut plane.

A mathematical fault plane parallel to the cut plane is defined in the middle of the system.  A generalized stacking fault system can then be created by shifting all atoms on one side of the fault plane by a vector, $\vec{s}$.  The shifted system is then relaxed using the same confined energy/force minimization used on the non-shifted system.  The generalized stacking fault energy, $\gamma$, can then be computed by comparing the total energy of the system, $E_{total}$, before and after $\vec{s}$ is applied

$$ \gamma(\vec{s}) = \frac{E_{total}(\vec{s}) - E_{total}(\vec{0})}{A},$$

where $A$ is the area of the fault plane, which can be computed using the two box vectors, $\vec{a_1}$ and $\vec{a_2}$, that are not the cutboxvector.

$$A = \left| \vec{a_1} \times \vec{a_2} \right|,$$

Additionally, the relaxation normal to the glide plane is characterized using the center of mass of the atoms above and below the cut plane.  Notably, the component of the center of mass normal to the glide/cut plane is calculated for the two halves of the the system, and the difference is computed

$$ \delta = \left<x\right>^{+} - \left<x\right>^{-}.$$

The relaxation normal is then taken as the change in the center of mass difference after the shift is applied.

$$ \Delta\delta = \delta(\vec{s}) - \delta(\vec{0}).$$
