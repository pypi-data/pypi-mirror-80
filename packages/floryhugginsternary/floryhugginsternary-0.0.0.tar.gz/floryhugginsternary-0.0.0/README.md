# samternary

`floryhugginsternary` aids users in predicting phase diagrams for three component mixtures of small molecules. It does this by providing the equations of chemical equilibrium (i.e. equal chemical potentials) in a form which is fairly straightforward to implement into a numerical solver (e.g. scipy.optimize.root or similar).

For example, if I wanted to determine the binodal and spinodal lines of a three component mixture with two phases when the volume fraction of component one in phase A (phi_1A in the code below) is 0.07, with flory huggins parameters chi_11 = 1, chi_22 = 1, and chi_12 = 4, I would write

`from floryhugginsternary.chemeq3 import ChemEq3_2phase`

`from scipy.optimize import root`

`ce = ChemEq3_2phase(phi_1A= 0.07,chi_12=3,chi_11=1,chi_22=-1)`

`phi_1B,phi_2A,phi_2B = 0.42,0.07,0.42 # a (good) guess for phi_2A, phi_1B, phi_2B`

`x0 = ce.phis_to_x(phi_1B,phi_2A,phi_2B)`

`solution = scipy.optimize.root(ce.rootfind_eqns,x0,jac=ch.rootfind_jacobian)`

`phi_1s,phi_2s = ce.get_phi1s_phi2s(solution.x) # get the volume fractions at phase coexistence`

`phi_1A,phi_1B = phi_1s[0],phi_1s[1]`

`phi_2A,phi_2B = phi_2s[0],phi_2s[1]`


which would, if a solution existed, return the volume fractions of the two different phases for both components A and B (otherwise it would just return the trivial solution of component one being equal in both phases and component two being equal in both phases).


See the examples folder for a list of examples on how to use this package. Here is an example picture of a binodal curve at chi_12 = 4, chi_11 = chi_22 = 1, with tie-lines. Also shown is the spinodal curve. This picture was computed using this package along with matplotlib and scipy.optimize.

![Binodal and spinodal curves at chi_12 = 4, chi_11 = chi_22 = 1.](/examples/example_chi_12_is4_chi_11ischi_22is1.png)

