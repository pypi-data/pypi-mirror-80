## Method and Theory

### Stroh theory

A detailed description of the Stroh method to solve the Eshelby solution for an anisotropic straight dislocation can be found in the [atomman documentation](https://www.ctcms.nist.gov/potentials/atomman/).

### Orientation

One of the most important considerations in defining an atomistic system containing a dislocation monopole system is the system's orientation.  In particular, care is needed to properly align the system's Cartesian axes, $x, y, z$, the system's box vectors, $a, b, c$, and the Stroh solution's axes, $u, m, n$.

- In order for the dislocation to remain perfectly straight in the atomic system, the dislocation line, $u$, must correspond to one of the system's box vectors.  The resulting dislocation monopole system will be periodic along the box direction corresponding to $u$, and non-periodic in the other two box directions.

- The Stroh solution is invariant along the dislocation line direction, $u$, thereby the solution is 2 dimensional. $m$ and $n$ are the unit vectors for the 2D axis system used by the Stroh solution. As such, $u, m$ and $n$ are all normal to each other. The plane defined by the $um$ vectors is the dislocation's slip plane, i.e. $n$ is normal to the slip plane.

- For LAMMPS simulations, the system's box vectors are limited such that $a$ is parallel to the $x$-axis, and $b$ is in the $xy$-plane (i.e. has no $z$ component). Based on this and the previous two points, the most convenient, and therefore the default, orientation for a generic dislocation is to

  - Make $u$ and $a$ parallel, which also places $u$ parallel to the $x$-axis.

  - Select $b$ such that it is within the slip plane. As $u$ and $a$ must also be in the slip plane, the plane itself is defined by $a \times b$.
  
  - Given that neither $a$ nor $b$ have $z$ components, the normal to the slip plane will be perpendicular to $z$.  From this, it naturally follows that $m$ can be taken as parallel to the $y$-axis, and $n$ parallel to the $z$-axis.

### Calculation methodology

1. An initial system is generated based on the loaded system and *uvw*, *atomshift*, and *sizemults* input parameters.  This initial system is saved as base.dump.

2. The atomman.defect.Stroh class is used to obtain the dislocation solution based on the defined $m$ and $n$ vectors, $C_{ij}$, and the dislocation's Burgers vector, $b_i$.

3. The dislocation is inserted into the system by displacing all atoms according to the Stroh solution's displacements.  The dislocation line is placed parallel to the specified *dislocation_lineboxvector* and includes the Cartesian point (0, 0, 0).

4. The box dimension parallel to the dislocation line is kept periodic, and the other two box directions are made non-periodic. A boundary region is defined that is at least *bwidth* thick at the edges of the two non-periodic directions, such that the shape of the active region corresponds to the *bshape* parameter. Atoms in the boundary region are identified by altering their integer atomic types.

5. The dislocation is relaxed by performing a LAMMPS simulation.  The atoms in the active region are allowed to relax either with nvt integration followed by an energy/force minimization, or with just an energy/force minimization.  The atoms in the boundary region are held fixed at the elastic solution.  The resulting relaxed system is saved as disl.dump.

6. Parameters associated with the Stroh solution are saved to the results record.
