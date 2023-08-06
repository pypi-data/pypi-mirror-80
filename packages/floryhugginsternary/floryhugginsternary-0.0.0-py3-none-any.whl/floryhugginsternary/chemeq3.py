import numpy as np

# equations of chemical equilibrium

class ChemEq3_6phase():
    """
    Base class for phase-coexistence in the Flory-Huggins
    (regular solution) model, when there are three
    components. Up to six phases are possible according
    to the Gibbs phase rule. However, in this six
    phase treatment, there are no free parameters
    (including the chi parameters!), so chemical
    equilibrium for six phases can only exist at a
    single point in 15-dimensional phi-chi space.

    It seems unlikely that one will be able to find
    this single point in the 15-dimensional space
    (if it even exists). Therefore, it is
    recommended to instead look at lower numbers of
    phases, e.g. ChemEq3_3phase and ChemEq3_2phase.
    

    Attributes
    ----------
    None

    Methods
    -------
    mu_0
        Chemical potential of the solvent.
    mu_1
        Chemical potential of the first solute.
    mu_2
        Chemical potential of the second solute.
    free_energy
        Free energy of the fully mixed ternary
        system.
    g_i_pq
        Difference in chemical potentials of the
        i^th component in phases p and q, i.e.
        g_i_pq = mu_i_q - mu_i_p.
    eqns
        Compute list of all chemical potential
        differences g_i_pq for the six different
        phases. Returns a list of length 15.
        This method would be used in a
        rootfinding algorithm to in attempting
        to determine chemical equilibrium for the
        six phases.
    """
    
    def mu_0(self,phi_1,phi_2,chi_12,chi_11,chi_22):

        return (np.log(1-phi_1-phi_2)
                +chi_11*phi_1**2+2*chi_12*phi_1*phi_2
                +chi_22*phi_2**2)

    def mu_1(self,phi_1,phi_2,chi_12,chi_11,chi_22):

        return (np.log(phi_1)
                +chi_11*phi_1**2+2*chi_12*phi_1*phi_2
                +chi_22*phi_2**2
                -2*(phi_1*chi_11+phi_2*chi_12))


                
    def mu_2(self,phi_1,phi_2,chi_12,chi_11,chi_22):

        return (np.log(phi_2)
                +chi_11*phi_1**2+2*chi_12*phi_1*phi_2
                +chi_22*phi_2**2
                -2*(phi_1*chi_12+phi_2*chi_22))


        
    def free_energy(self,phi_1,phi_2,chi_12,chi_11,chi_22):

        phi_0 = 1-phi_1-phi_2
        ans = phi_1*np.log(phi_1) + phi_2*np.log(phi_2)
        ans += phi_0*np.log(phi_0)
        ans += (phi_1*(1-phi_1)*chi_11-2*phi_1*phi_2*chi_12
                + phi_2*(1-phi_2)*chi_22)
        return ans

    
    def g_i_pq(self,i,p,q,phi_1s,phi_2s,chis):

        mus = [self.mu_0,self.mu_1,self.mu_2]

        return (mus[i](phi_1s[q],phi_2s[q],chis[0],
                       chis[1],chis[2])
                -mus[i](phi_1s[p],phi_2s[p],chis[0],
                        chis[1],chis[2]))


    def eqns(self,x):

        phi_1s = [x[0],x[2],x[4],x[6],x[8],x[10]]
        phi_2s = [x[1],x[3],x[5],x[7],x[9],x[11]]
        chis = [x[12],x[13],x[14]]
        
        outs = []
        for q in range(1,6):
            for i in range(3):
                outs.append(self.g_i_pq(i,0,q,phi_1s,
                                        phi_2s,chis))
    
        return outs



class ChemEq3_3phase(ChemEq3_6phase):
    """
    Child class of ChemEq3_6phase. Does essentially
    the same thing as ChemEq3_6phase, except it only
    looks for coexistence of three phases. Therefore,
    there are fewer dimensions in phi-chi parameter
    space (9 instead of 15). By the Gibbs phase rule,
    three of these dimensions will be free parameters
    in three-phase coexistence. These three parameters
    will be selected to be the chi parameters (see
    the Attributes section below).

    Attributes
    ----------
    chi_12 : float
        The value of the chi_12 interaction parameter.
    chi_11 : float, optional
        The value of the chi_11 interaction parameter.
    chi_22 : float
        The value of the chi_22 interaction parameter.

    Rootfinding Methods
    -------------------

    rootfind_eqns(self,x)

        Computes the set of non-linear equations
        (all must be set equal to zero to solve) which
        are used both directly for rootfinding
        algorithms or indirectly in the definition
        of objective function (for minimisation). Pass
        this method to e.g. scipy.optimise.root to try 
        and find chemical equilibrium.

    rootfind_jacobian(self,x)
        Computes the Jacobian matrix of the rootfind_eqns
        method above. Pass this method (along with the
        rootfind_eqns method above) to e.g.
        scipy.optimise.root to try and find chemical
        equilibrium.

    Optimisation Methods
    --------------------
    objective(self,x)
        Defines and computes an objective function for
        an optimisation approach to determining chemical
        equilibrium. It computes the squared 2-norm of the
        6 equations of chemical equilibrium defined in
        rootfind_eqns above. Pass this method to e.g.
        scipy.optimise.minimise to try and find chemical
        equilibrium.

    obj_jac(self,x)
        Computes the Jacobian of the objective function.
        Pass this method (along with the objective method
        above) to e.g. scipy.optimise.minimise to try and
        find chemical equilibrium.

    obj_hess(self,x)
        Computes the 6x6 Hessian of the objective function.
        Pass this method (along with the objective method
        and the obj_jac method above) to e.g.
        scipy.optimise.minimise to try and find chemical
        equilibrium. WARNING: It seems like using this
        Hessian in any optimisation routine leads to
        only finding the trivial solution, regardless of
        initial condition. It might be due to a coding
        error or a convexity issue of the objective
        function (I have tested for the latter extensively
        using numerical derivatives and have yet to find
        a bug).

    Other Public Methods
    --------------------

    phis_to_x(self,phi_1A,phi_1B,phi_1C,
              phi_2A,phi_2B,phi_2C)
        Move phi values into a single numpy array, so
        that this array can be used in optimisation or
        root finding. It just returns the array x
        where
        
            x = np.array([phi_1A,phi_2A,phi_1B,
                          phi_2B,phi_1C,phi_2C])

    get_phi1s_phi2s(self,x)
        Convert the x array determined via either
        optimisation or root finding, back into
        an array of phi_1 values in the 3 phases
        and an array of phi_2 values in the 3 phases.
        It just returns the two lists
            phi_1s = [x[0],x[2],x[4]]
            phi_2s = [x[1],x[3],x[5]]

    free_energy(self,phi_1,phi_2)
        Free energy of the fully mixed ternary
        system.
    
    g_i_pq(self,i,p,q,phi_1s,phi_2s)
        Difference in chemical potentials of the
        i^th component in phases p and q, i.e.
        g_i_pq = mu_i_q - mu_i_p.

    dg_0_1(self,phi_1,phi_2)
        Computes the derivative of g_0^{(\alpha\beta)}
        with respect to phi_1^{(\beta)}

    dg_0_2(self,phi_1,phi_2)
        Computes the derivative of g_0^{(\alpha\beta)}
        with respect to phi_2^{(\beta)}    

    dg_1_1(self,phi_1,phi_2)
        Computes the derivative of g_1^{(\alpha\beta)}
        with respect to phi_1^{(\beta)}

    dg_1_2(self,phi_1,phi_2)
        Computes the derivative of g_1^{(\alpha\beta)}
        with respect to phi_2^{(\beta)}

    dg_2_1(self,phi_1,phi_2)
        Computes the derivative of g_2^{(\alpha\beta)}
        with respect to phi_1^{(\beta)}    

    dg_2_2(self,phi_1,phi_2)
        Computes the derivative of g_2^{(\alpha\beta)}
        with respect to phi_2^{(\beta)}

    ddg_0_11(self,phi_1,phi_2)
        Computes the second derivative of g_0^{(\alpha\beta)}
        with respect to phi_1^{(\beta)} and phi_1^{(\beta)}

    ddg_0_12(self,phi_1,phi_2)
        Computes the second derivative of g_0^{(\alpha\beta)}
        with respect to phi_1^{(\beta)} and phi_2^{(\beta)}
    
    ddg_0_22(self,phi_1,phi_2)
        Computes the second derivative of g_0^{(\alpha\beta)}
        with respect to phi_2^{(\beta)} and phi_2^{(\beta)}

    ddg_1_11(self,phi_1,phi_2)
        Computes the second derivative of g_1^{(\alpha\beta)}
        with respect to phi_1^{(\beta)} and phi_1^{(\beta)}

    ddg_1_12(self,phi_1,phi_2)
        Computes the second derivative of g_1^{(\alpha\beta)}
        with respect to phi_1^{(\beta)} and phi_2^{(\beta)}

    ddg_1_22(self,phi_1,phi_2)
        Computes the second derivative of g_1^{(\alpha\beta)}
        with respect to phi_2^{(\beta)} and phi_2^{(\beta)}

    ddg_2_11(self,phi_1,phi_2)
        Computes the second derivative of g_2^{(\alpha\beta)}
        with respect to phi_1^{(\beta)} and phi_1^{(\beta)}

    ddg_2_12(self,phi_1,phi_2)
        Computes the second derivative of g_2^{(\alpha\beta)}
        with respect to phi_1^{(\beta)} and phi_2^{(\beta)}

    ddg_2_22(self,phi_1,phi_2)
        Computes the second derivative of g_2^{(\alpha\beta)}
        with respect to phi_2^{(\beta)} and phi_2^{(\beta)}

    """

    def __init__(self,chi_12,chi_11=1,chi_22=1):
        """
        Initialise all attributes.

        Parameters
        ----------
        chi_12 : float
            The value of the chi_12 interaction parameter.
        chi_11 : float, optional
            The value of the chi_11 interaction parameter.
        chi_22 : float, optional
            The value of the chi_22 interaction parameter.
        """


        self.chi_11 = chi_11
        self.chi_22 = chi_22
        self.chi_12 = chi_12

        
        return

    def phis_to_x(self,phi_1A,phi_1B,phi_1C,
                  phi_2A,phi_2B,phi_2C):
        """
        Move phi values into a single numpy array, so
        that this array can be used in optimisation or
        root finding. 

        Parameters
        ----------
        phi_1A : float
            Volume fraction of component one in phase A.
        phi_1B : float
            Volume fraction of component one in phase B.
        phi_1C : float
            Volume fraction of component one in phase C.
        phi_2A : float
            Volume fraction of component two in phase A.
        phi_2B : float
            Volume fraction of component two in phase B.
        phi_2C : float
            Volume fraction of component two in phase C.

        Returns
        -------
        x : np.array of length 6
            x = np.array([phi_1A,phi_2A,phi_1B,
                          phi_2B,phi_1C,phi_2C])

        Notes
        -----
        All the volume fractions must be greater than
        zero, and for i = A,B,C must satisfy
        0 < phi_1i + phi_2i < 1.

        """


        x = np.array([phi_1A,phi_2A,phi_1B,phi_2B,
                      phi_1C,phi_2C])
        return x

    def get_phi1s_phi2s(self,x):

        """

        Convert the x array determined via either
        optimisation or root finding, back into
        an array of phi_1 values in the 3 phases
        and an array of phi_2 values in the 3 phases.

        Parameters
        ----------
        x : np.array of length 6
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_1A,phi_2A,phi_1B,
                          phi_2B,phi_1C,phi_2C])
        
        Returns
        -------
        phi_1s : list
            phi_1s = [x[0],x[2],x[4]]
        phi_2s : list
            phi_2s = [x[1],x[3],x[5]]
        """

        phi_1s = [x[0],x[2],x[4]]
        phi_2s = [x[1],x[3],x[5]]

        return phi_1s,phi_2s

    def free_energy(self,phi_1,phi_2):
        """
        Free energy of the fully mixed ternary
        system.

        Parameters
        ----------
        phi_1 : float or np.array
            Volume fraction of component one.
        phi_2 : float or np.array
            Volume fraction of component two.

        Returns
        -------
        fe : float or np.array
            Free energy of the fully mixed ternary
            system.
    
        """

        return super().free_energy(
            phi_1,phi_2,self.chi_12,self.chi_11,self.chi_22)
    
    def g_i_pq(self,i,p,q,phi_1s,phi_2s):
        """
        Difference in chemical potentials of the
        i^th component in phases p and q, i.e.
        g_i_pq = mu_i_q - mu_i_p.

        Parameters
        ----------
        i : int
            The chemical component index label (i=1,2,3).
        p : int
            A phase component index label (p=0,1,2 for
            phases A,B and C respectively).
        q : int
            A phase component index label (q=0,1,2 for
            phases A,B and C respectively).
        phi_1s : list of floats
            phi_1s = [phi_1A,phi_1B,phi_1C]
        phi_2s : list of floats
            phi_2s = [phi_2A,phi_2B,phi_2C]

        Returns
        -------
        g : float
            Difference in chemical potentials of the
            i^th component in phases p and q, i.e.
            g_i_pq = mu_i_q - mu_i_p.
        
        
        """
        
        chis = [self.chi_12,self.chi_11,self.chi_22]
        return super().g_i_pq(i,p,q,phi_1s,phi_2s,
                              chis)

    def rootfind_eqns(self,x):
        """
        Computes the set of non-linear equations
        (all must be set equal to zero to solve) which
        are used both directly for rootfinding
        algorithms or indirectly in the definition
        of objective function (for minimisation). Pass
        this method to e.g. scipy.optimise.root to try 
        and find chemical equilibrium.

        Parameters
        ----------
        x : np.array of length 6
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_1A,phi_2A,phi_1B,
                          phi_2B,phi_1C,phi_2C])

        Returns
        -------
        gs : list of floats
            List of all the equations of chemical
            equilibrium, in the order g0_AB, g1_AB,
            g2_AB, g0_AC, g1_AC, g2_AC.

        """

        phi_1s,phi_2s = self.get_phi1s_phi2s(x)
        
        outs = []
        
        for q in range(1,3):
            for i in range(3):
                outs.append(self.g_i_pq(i,0,q,phi_1s,
                                        phi_2s))
    
        return outs

    def dg_0_1(self,phi_1,phi_2):
        # derivative of g_0^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)}

        ans = -1/(1-phi_1-phi_2)

        ans += 2*self.chi_11*phi_1+2*self.chi_12*phi_2
    
        return ans

    def dg_0_2(self,phi_1,phi_2):
        # derivative of g_0^{(\alpha\beta)}
        # with respect to phi_2^{(\beta)}

        ans = -1/(1-phi_1-phi_2)

        ans += 2*self.chi_22*phi_2+2*self.chi_12*phi_1

        return ans


    
    def dg_1_1(self,phi_1,phi_2):
        # derivative of g_1^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)}

        ans = (1./phi_1 + 2*self.chi_11*phi_1
               +2*self.chi_12*phi_2-2*self.chi_11)

        return ans
            

        
    def dg_1_2(self,phi_1,phi_2):
        # derivative of g_1^{(\alpha\beta)}
        # with respect to phi_2^{(\beta)}

        ans = (2*self.chi_22*phi_2
               +2*self.chi_12*phi_1-2*self.chi_12)

        return ans


    def dg_2_1(self,phi_1,phi_2):
        # derivative of g_2^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)}

        ans = (2*self.chi_11*phi_1
               +2*self.chi_12*phi_2-2*self.chi_12)

        return ans
    

    def dg_2_2(self,phi_1,phi_2):
        # derivative of g_2^{(\alpha\beta)}
        # with respect to phi_2^{(\beta)}

        ans = (1./phi_2+2*self.chi_22*phi_2
               +2*self.chi_12*phi_1-2*self.chi_22)

        return ans

    def rootfind_jacobian(self,x):

        """
        Computes the Jacobian matrix of the rootfind_eqns
        method above. Pass this method (along with the
        rootfind_eqns method above) to e.g.
        scipy.optimise.root to try and find chemical
        equilibrium.

        Parameters
        ----------
        x : np.array of length 6
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_1A,phi_2A,phi_1B,
                          phi_2B,phi_1C,phi_2C])

        Returns
        -------
        J : 6x6 np.array
            Jacobian of the rootfind_eqns method, with
            rows in the order 0_AB, 1_AB,
            2_AB, 0_AC, 1_AC, 2_AC and columns in the
            order phi_1A,phi_2A,phi_1B,phi_2B,phi_1C,
            phi_2C.

        """
        
        phi_1s,phi_2s = self.get_phi1s_phi2s(x)

        J11 = -1*self.dg_0_1(phi_1s[0],phi_2s[0])
        J12 = -1*self.dg_0_2(phi_1s[0],phi_2s[0])
        J13 = self.dg_0_1(phi_1s[1],phi_2s[1])
        J14 = self.dg_0_2(phi_1s[1],phi_2s[1])

        J21 = -1*self.dg_1_1(phi_1s[0],phi_2s[0])
        J22 = -1*self.dg_1_2(phi_1s[0],phi_2s[0])
        J23 = self.dg_1_2(phi_1s[1],phi_2s[1])
        J24 = self.dg_1_2(phi_1s[1],phi_2s[1])

        J31 = -1*self.dg_2_1(phi_1s[0],phi_2s[0])
        J32 = -1*self.dg_2_2(phi_1s[0],phi_2s[0])
        J33 = self.dg_2_1(phi_1s[1],phi_2s[1])
        J34 = self.dg_2_2(phi_1s[1],phi_2s[1])

        J41 = J11
        J42 = J12
        J45 = self.dg_0_1(phi_1s[2],phi_2s[2])
        J46 = self.dg_0_2(phi_1s[2],phi_2s[2])

        J51 = J21
        J52 = J22
        J55 = self.dg_1_1(phi_1s[2],phi_2s[2])
        J56 = self.dg_1_2(phi_1s[2],phi_2s[2])

        J61 = J31
        J62 = J32
        J65 = self.dg_2_1(phi_1s[2],phi_2s[2])
        J66 = self.dg_2_2(phi_1s[2],phi_2s[2])

        return np.array([[J11,J12,J13,J14,0,0],
                         [J21,J22,J23,J24,0,0],
                         [J31,J32,J33,J34,0,0],
                         [J41,J42,0,0,J45,J46],
                         [J51,J52,0,0,J55,J56],
                         [J61,J62,0,0,J65,J66]])

    

    def objective(self,x):
        """
        Defines and computes an objective function for
        an optimisation approach to determining chemical
        equilibrium. It computes the squared 2-norm of the
        6 equations of chemical equilibrium defined in
        rootfind_eqns above. Pass this method to e.g.
        scipy.optimise.minimise to try and find chemical
        equilibrium.

        Parameters
        ----------
        x : np.array of length 6
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_1A,phi_2A,phi_1B,
                          phi_2B,phi_1C,phi_2C])

        Returns
        -------
        g : float
            Square of the 2-norm of the rootfind_eqns
            method defined above, evaluated at x.

        """

        outs = np.array(self.rootfind_eqns(x))
        out = np.dot(outs,outs)

        return out



    def obj_jac(self,x):
        """
        Computes the Jacobian of the objective function.
        Pass this method (along with the objective method
        above) to e.g. scipy.optimise.minimise to try and
        find chemical equilibrium.

        Parameters
        ----------
        x : np.array of length 6
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_1A,phi_2A,phi_1B,
                          phi_2B,phi_1C,phi_2C])

        Returns
        -------
        J : np.array of length 6
            Gradient of the objective function with
            respect to x.
        """

        # order of gradients is phi_1A,phi_2A,phi_1B,
        # phi_2B,phi_1C,phi_2c

        phi_1s,phi_2s = self.get_phi1s_phi2s(x)

        obj_vec = np.array(self.rootfind_eqns(x))


        j1 = -2*obj_vec[0]*self.dg_0_1(phi_1s[0],phi_2s[0])
        j1 += -2*obj_vec[1]*self.dg_1_1(phi_1s[0],phi_2s[0])
        j1 += -2*obj_vec[2]*self.dg_2_1(phi_1s[0],phi_2s[0])
        j1 += -2*obj_vec[3]*self.dg_0_1(phi_1s[0],phi_2s[0])
        j1 += -2*obj_vec[4]*self.dg_1_1(phi_1s[0],phi_2s[0])
        j1 += -2*obj_vec[5]*self.dg_2_1(phi_1s[0],phi_2s[0])

        j2 = -2*obj_vec[0]*self.dg_0_2(phi_1s[0],phi_2s[0])
        j2 += -2*obj_vec[1]*self.dg_1_2(phi_1s[0],phi_2s[0])
        j2 += -2*obj_vec[2]*self.dg_2_2(phi_1s[0],phi_2s[0])
        j2 += -2*obj_vec[3]*self.dg_0_2(phi_1s[0],phi_2s[0])
        j2 += -2*obj_vec[4]*self.dg_1_2(phi_1s[0],phi_2s[0])
        j2 += -2*obj_vec[5]*self.dg_2_2(phi_1s[0],phi_2s[0])

        j3 = 2*obj_vec[0]*self.dg_0_1(phi_1s[1],phi_2s[1])
        j3 += 2*obj_vec[1]*self.dg_1_1(phi_1s[1],phi_2s[1])
        j3 += 2*obj_vec[2]*self.dg_2_1(phi_1s[1],phi_2s[1])

        j4 = 2*obj_vec[0]*self.dg_0_2(phi_1s[1],phi_2s[1])
        j4 += 2*obj_vec[1]*self.dg_1_2(phi_1s[1],phi_2s[1])
        j4 += 2*obj_vec[2]*self.dg_2_2(phi_1s[1],phi_2s[1])

        j5 = 2*obj_vec[3]*self.dg_0_1(phi_1s[2],phi_2s[2])
        j5 += 2*obj_vec[4]*self.dg_1_1(phi_1s[2],phi_2s[2])
        j5 += 2*obj_vec[5]*self.dg_2_1(phi_1s[2],phi_2s[2])

        j6 = 2*obj_vec[3]*self.dg_0_2(phi_1s[2],phi_2s[2])
        j6 += 2*obj_vec[4]*self.dg_1_2(phi_1s[2],phi_2s[2])
        j6 += 2*obj_vec[5]*self.dg_2_2(phi_1s[2],phi_2s[2])

        return np.array([j1,j2,j3,j4,j5,j6])

        
    def ddg_0_11(self,phi_1,phi_2):
        # second derivative of g_0^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_1^{(\beta)}

        return -1/(1-phi_1-phi_2)**2+2*self.chi_11

    
    def ddg_0_12(self,phi_1,phi_2):
        # second derivative of g_0^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_2^{(\beta)}

        return -1/(1-phi_1-phi_2)**2+2*self.chi_12

    
    def ddg_0_22(self,phi_1,phi_2):
        # second derivative of g_0^{(\alpha\beta)}
        # with respect to phi_2^{(\beta)} and phi_2^{(\beta)}

        return -1/(1-phi_1-phi_2)**2+2*self.chi_22


    def ddg_1_11(self,phi_1,phi_2):
        # second derivative of g_1^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_1^{(\beta)}

        return -1/phi_1**2+2*self.chi_11
    

    def ddg_1_12(self,phi_1,phi_2):
        # second derivative of g_1^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_2^{(\beta)}

        return 2*self.chi_12
    

    def ddg_1_22(self,phi_1,phi_2):
        # second derivative of g_1^{(\alpha\beta)}
        # with respect to phi_2^{(\beta)} and phi_2^{(\beta)}

        return 2*self.chi_22
    

    def ddg_2_11(self,phi_1,phi_2):
        # second derivative of g_2^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_1^{(\beta)}

        return 2*self.chi_11

    
    def ddg_2_12(self,phi_1,phi_2):
        # second derivative of g_2^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_2^{(\beta)}

        return 2*self.chi_12
    

    def ddg_2_22(self,phi_1,phi_2):
        # second derivative of g_2^{(\alpha\beta)}
        # with respect to phi_2^{(\beta)} and phi_2^{(\beta)}

        return -1/phi_2**2+2*self.chi_22

    def obj_hess(self,x):
        """
        Computes the 6x6 Hessian of the objective function.
        Pass this method (along with the objective method
        and the obj_jac method above) to e.g.
        scipy.optimise.minimise to try and find chemical
        equilibrium. WARNING: It seems like using this
        Hessian in any optimisation routine leads to
        only finding the trivial solution, regardless of
        initial condition. It might be due to a coding
        error or a convexity issue of the objective
        function (I have tested for the latter extensively
        using numerical derivatives and have yet to find
        a bug).

        Parameters
        ----------
        x : np.array of length 6
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_1A,phi_2A,phi_1B,
                          phi_2B,phi_1C,phi_2C])

        Returns
        -------
        h : 6x6 np.array
            Hessian of the objective function with
            respect to x.

        """

        phi_1s,phi_2s = self.get_phi1s_phi2s(x)
        obj_vec = np.array(self.rootfind_eqns(x))
        H11 = 0
        H11 += 2*(self.dg_0_1(phi_1s[0],phi_2s[0]))**2
        H11 += 2*(self.dg_1_1(phi_1s[0],phi_2s[0]))**2
        H11 += 2*(self.dg_2_1(phi_1s[0],phi_2s[0]))**2
        H11 += 2*(self.dg_0_1(phi_1s[0],phi_2s[0]))**2
        H11 += 2*(self.dg_1_1(phi_1s[0],phi_2s[0]))**2
        H11 += 2*(self.dg_2_1(phi_1s[0],phi_2s[0]))**2

        H11 += -2*obj_vec[0]*self.ddg_0_11(phi_1s[0],phi_2s[0])
        H11 += -2*obj_vec[1]*self.ddg_1_11(phi_1s[0],phi_2s[0])
        H11 += -2*obj_vec[2]*self.ddg_2_11(phi_1s[0],phi_2s[0])
        H11 += -2*obj_vec[3]*self.ddg_0_11(phi_1s[0],phi_2s[0])
        H11 += -2*obj_vec[4]*self.ddg_1_11(phi_1s[0],phi_2s[0])
        H11 += -2*obj_vec[5]*self.ddg_2_11(phi_1s[0],phi_2s[0])

        H12 = 0

        H12 += (2*self.dg_0_1(phi_1s[0],phi_2s[0])
                *self.dg_0_2(phi_1s[0],phi_2s[0]))
        H12 += (2*self.dg_1_1(phi_1s[0],phi_2s[0])
                *self.dg_1_2(phi_1s[0],phi_2s[0]))
        H12 += (2*self.dg_2_1(phi_1s[0],phi_2s[0])
                *self.dg_2_2(phi_1s[0],phi_2s[0]))
        H12 += (2*self.dg_0_1(phi_1s[0],phi_2s[0])
                *self.dg_0_2(phi_1s[0],phi_2s[0]))
        H12 += (2*self.dg_1_1(phi_1s[0],phi_2s[0])
                *self.dg_1_2(phi_1s[0],phi_2s[0]))
        H12 += (2*self.dg_2_1(phi_1s[0],phi_2s[0])
                *self.dg_2_2(phi_1s[0],phi_2s[0]))

        H12 += -2*obj_vec[0]*self.ddg_0_12(phi_1s[0],phi_2s[0])
        H12 += -2*obj_vec[1]*self.ddg_1_12(phi_1s[0],phi_2s[0])
        H12 += -2*obj_vec[2]*self.ddg_2_12(phi_1s[0],phi_2s[0])
        H12 += -2*obj_vec[3]*self.ddg_0_12(phi_1s[0],phi_2s[0])
        H12 += -2*obj_vec[4]*self.ddg_1_12(phi_1s[0],phi_2s[0])
        H12 += -2*obj_vec[5]*self.ddg_2_12(phi_1s[0],phi_2s[0])

        H13 = 0

        H13 += (-2*self.dg_0_1(phi_1s[0],phi_2s[0])
               *self.dg_0_1(phi_1s[1],phi_2s[1]))
        H13 += (-2*self.dg_1_1(phi_1s[0],phi_2s[0])
                *self.dg_1_1(phi_1s[1],phi_2s[1]))
        H13 += (-2*self.dg_2_1(phi_1s[0],phi_2s[0])
                *self.dg_2_1(phi_1s[1],phi_2s[1]))

        H14 = 0
        H14 += (-2*self.dg_0_1(phi_1s[0],phi_2s[0])
               *self.dg_0_2(phi_1s[1],phi_2s[1]))
        H14 += (-2*self.dg_1_1(phi_1s[0],phi_2s[0])
                *self.dg_1_2(phi_1s[1],phi_2s[1]))
        H14 += (-2*self.dg_2_1(phi_1s[0],phi_2s[0])
                *self.dg_2_2(phi_1s[1],phi_2s[1]))
        
        H15 = 0
        H15 += (-2*self.dg_0_1(phi_1s[0],phi_2s[0])
               *self.dg_0_1(phi_1s[2],phi_2s[2]))
        H15 += (-2*self.dg_1_1(phi_1s[0],phi_2s[0])
                *self.dg_1_1(phi_1s[2],phi_2s[2]))
        H15 += (-2*self.dg_2_1(phi_1s[0],phi_2s[0])
                *self.dg_2_1(phi_1s[2],phi_2s[2]))

        H16 = 0
        H16 += (-2*self.dg_0_1(phi_1s[0],phi_2s[0])
               *self.dg_0_2(phi_1s[2],phi_2s[2]))
        H16 += (-2*self.dg_1_1(phi_1s[0],phi_2s[0])
                *self.dg_1_2(phi_1s[2],phi_2s[2]))
        H16 += (-2*self.dg_2_1(phi_1s[0],phi_2s[0])
                *self.dg_2_2(phi_1s[2],phi_2s[2]))
        
        H22 = 0
        H22 += 2*(self.dg_0_2(phi_1s[0],phi_2s[0]))**2
        H22 += 2*(self.dg_1_2(phi_1s[0],phi_2s[0]))**2
        H22 += 2*(self.dg_2_2(phi_1s[0],phi_2s[0]))**2
        H22 += 2*(self.dg_0_2(phi_1s[0],phi_2s[0]))**2
        H22 += 2*(self.dg_1_2(phi_1s[0],phi_2s[0]))**2
        H22 += 2*(self.dg_2_2(phi_1s[0],phi_2s[0]))**2
        H22 += -2*obj_vec[0]*self.ddg_0_22(phi_1s[0],phi_2s[0])
        H22 += -2*obj_vec[1]*self.ddg_1_22(phi_1s[0],phi_2s[0])
        H22 += -2*obj_vec[2]*self.ddg_2_22(phi_1s[0],phi_2s[0])
        H22 += -2*obj_vec[3]*self.ddg_0_22(phi_1s[0],phi_2s[0])
        H22 += -2*obj_vec[4]*self.ddg_1_22(phi_1s[0],phi_2s[0])
        H22 += -2*obj_vec[5]*self.ddg_2_22(phi_1s[0],phi_2s[0])
        
        H23 = 0

        H23 += (-2*self.dg_0_2(phi_1s[0],phi_2s[0])
               *self.dg_0_1(phi_1s[1],phi_2s[1]))
        H23 += (-2*self.dg_1_2(phi_1s[0],phi_2s[0])
                *self.dg_1_1(phi_1s[1],phi_2s[1]))
        H23 += (-2*self.dg_2_2(phi_1s[0],phi_2s[0])
                *self.dg_2_1(phi_1s[1],phi_2s[1]))
        

        H24 = 0
        H24 += (-2*self.dg_0_2(phi_1s[0],phi_2s[0])
               *self.dg_0_2(phi_1s[1],phi_2s[1]))
        H24 += (-2*self.dg_1_2(phi_1s[0],phi_2s[0])
                *self.dg_1_2(phi_1s[1],phi_2s[1]))
        H24 += (-2*self.dg_2_2(phi_1s[0],phi_2s[0])
                *self.dg_2_2(phi_1s[1],phi_2s[1]))
        
        H25 = 0
        H25 += (-2*self.dg_0_2(phi_1s[0],phi_2s[0])
               *self.dg_0_1(phi_1s[2],phi_2s[2]))
        H25 += (-2*self.dg_1_2(phi_1s[0],phi_2s[0])
                *self.dg_1_1(phi_1s[2],phi_2s[2]))
        H25 += (-2*self.dg_2_2(phi_1s[0],phi_2s[0])
                *self.dg_2_1(phi_1s[2],phi_2s[2]))

        H26 = 0
        H26 += (-2*self.dg_0_2(phi_1s[0],phi_2s[0])
               *self.dg_0_2(phi_1s[2],phi_2s[2]))
        H26 += (-2*self.dg_1_2(phi_1s[0],phi_2s[0])
                *self.dg_1_2(phi_1s[2],phi_2s[2]))
        H26 += (-2*self.dg_2_2(phi_1s[0],phi_2s[0])
                *self.dg_2_2(phi_1s[2],phi_2s[2]))

        
        H33 = 0
        H33 += 2*(self.dg_0_1(phi_1s[1],phi_2s[1]))**2
        H33 += 2*(self.dg_1_1(phi_1s[1],phi_2s[1]))**2
        H33 += 2*(self.dg_2_1(phi_1s[1],phi_2s[1]))**2
        H33 += 2*obj_vec[0]*self.ddg_0_11(phi_1s[1],phi_2s[1])
        H33 += 2*obj_vec[1]*self.ddg_1_11(phi_1s[1],phi_2s[1])
        H33 += 2*obj_vec[2]*self.ddg_2_11(phi_1s[1],phi_2s[1])


        H34 = 0

        H34 += (2*self.dg_0_1(phi_1s[1],phi_2s[1])
                *self.dg_0_2(phi_1s[1],phi_2s[1]))
        H34 += (2*self.dg_1_1(phi_1s[1],phi_2s[1])
                *self.dg_1_2(phi_1s[1],phi_2s[1]))
        H34 += (2*self.dg_2_1(phi_1s[1],phi_2s[1])
                *self.dg_2_2(phi_1s[1],phi_2s[1]))

        H34 += 2*obj_vec[0]*self.ddg_0_12(phi_1s[1],phi_2s[1])
        H34 += 2*obj_vec[1]*self.ddg_1_12(phi_1s[1],phi_2s[1])
        H34 += 2*obj_vec[2]*self.ddg_2_12(phi_1s[1],phi_2s[1])

        H35 = 0
        H36 = 0

        H44 = 0
        H44 += 2*(self.dg_0_2(phi_1s[1],phi_2s[1]))**2
        H44 += 2*(self.dg_1_2(phi_1s[1],phi_2s[1]))**2
        H44 += 2*(self.dg_2_2(phi_1s[1],phi_2s[1]))**2
        H44 += 2*obj_vec[0]*self.ddg_0_22(phi_1s[1],phi_2s[1])
        H44 += 2*obj_vec[1]*self.ddg_1_22(phi_1s[1],phi_2s[1])
        H44 += 2*obj_vec[2]*self.ddg_2_22(phi_1s[1],phi_2s[1])

        H45 = 0
        H46 = 0

        
        H55 = 0
        H55 += 2*(self.dg_0_1(phi_1s[2],phi_2s[2]))**2
        H55 += 2*(self.dg_1_1(phi_1s[2],phi_2s[2]))**2
        H55 += 2*(self.dg_2_1(phi_1s[2],phi_2s[2]))**2
        H55 += 2*obj_vec[3]*self.ddg_0_11(phi_1s[2],phi_2s[2])
        H55 += 2*obj_vec[4]*self.ddg_1_11(phi_1s[2],phi_2s[2])
        H55 += 2*obj_vec[5]*self.ddg_2_11(phi_1s[2],phi_2s[2])

        H56 = 0
        H56 += (2*self.dg_0_1(phi_1s[2],phi_2s[2])
                *self.dg_0_2(phi_1s[2],phi_2s[2]))
        H56 += (2*self.dg_1_1(phi_1s[2],phi_2s[2])
                *self.dg_1_2(phi_1s[2],phi_2s[2]))
        H56 += (2*self.dg_2_1(phi_1s[2],phi_2s[2])
                *self.dg_2_2(phi_1s[2],phi_2s[2]))

        H56 += 2*obj_vec[3]*self.ddg_0_12(phi_1s[2],phi_2s[2])
        H56 += 2*obj_vec[4]*self.ddg_1_12(phi_1s[2],phi_2s[2])
        H56 += 2*obj_vec[5]*self.ddg_2_12(phi_1s[2],phi_2s[2])

        H66 = 0
        H66 += 2*(self.dg_0_2(phi_1s[2],phi_2s[2]))**2
        H66 += 2*(self.dg_1_2(phi_1s[2],phi_2s[2]))**2
        H66 += 2*(self.dg_2_2(phi_1s[2],phi_2s[2]))**2
        H66 += 2*obj_vec[3]*self.ddg_0_22(phi_1s[2],phi_2s[2])
        H66 += 2*obj_vec[4]*self.ddg_1_22(phi_1s[2],phi_2s[2])
        H66 += 2*obj_vec[5]*self.ddg_2_22(phi_1s[2],phi_2s[2])

        return np.array([[H11,H12,H13,H14,H15,H16],
                         [H12,H22,H23,H24,H25,H26],
                         [H13,H23,H33,H34,H35,H36],
                         [H14,H24,H34,H44,H45,H46],
                         [H15,H25,H35,H45,H55,H56],
                         [H16,H26,H36,H46,H56,H66]])


class ChemEq3_initialise(ChemEq3_6phase):

    """
    Class which attempts to find a common tangent (line)
    construction along a 1D curve in phi_1, phi_2 space.

    The default behaviour (and what is useful for the
    symmetric case of chi_11 = chi_11) is when the function
    is lambda x: x so that the common tangent line is
    along phi_1 = phi_2.

    The motivation for this class is that finding the
    common tangent line should help with an initial guess
    for finding the more generic common tangent plane in
    (2D) phi_1 phi_2 space.

    Attributes
    ----------
    chi_12 : float
        The value of the chi_12 interaction parameter.
    chi_11 : float, optional
        The value of the chi_11 interaction parameter.
    chi_22 : float
        The value of the chi_22 interaction parameter.
    func : callable, optional
        The function which maps phi_1 to phi_2 along
        a curve.

        '' func(x,*args) -> float or np.array ''
    dfunc : callable, optional
        The derivative of func.

        '' dfunc(x,*args) -> float or np.array ''

    args : tuple, optional
        Extra arguments which are to be passed to
        func and dfunc.

    Public Methods
    --------------

    free_energy
        Computes the free energy along the 1D curve
        in phi_1 phi_2 space.

    free_energy_slope
        Computes the derivative of the free energy
        along the 1D curve in phi_1 phi_2 space.

    commontangent_eqns
        Computes two non-linear equations, which
        when equal to zero indicate that a common
        tangent construction has been successfully
        found. Use a root-finding algorithm on this
        function in order to successfully find the
        common tangent construction.
    """
    
    def __init__(self,chi_12,chi_11=1,chi_22=1,
                 func=lambda x: x,
                 dfunc=lambda x: 1*np.ones_like(x),
                 args=()):

        """
        Initialise all attributes.

        Parameters
        ----------
        chi_12 : float
            The value of the chi_12 interaction parameter.
        chi_11 : float, optional
            The value of the chi_11 interaction parameter.
        chi_22 : float, optional
            The value of the chi_22 interaction parameter.
        func : callable, optional
            The function which maps phi_1 to phi_2 along
            a curve.

            '' func(x,*args) -> float or np.array ''

        dfunc : callable, optional
            The derivative of func.

            '' dfunc(x,*args) -> float or np.array ''

        args : tuple, optional
            Extra arguments which are to be passed to
            func and dfunc.
        """
        
        self.chi_12 = chi_12
        self.chi_11 = chi_11
        self.chi_22 = chi_22
        self.func = func
        self.dfunc = dfunc
        self.args = args

        return
    
    def _freeenergy(self,phi_1,phi_2):
        """
        Convenience function to avoid having to
        pass all the chi parameters to the free
        energy explicitly.

        Parameters
        ----------
        phi_1 : float or np.array
            Volume fraction of component 1. Must
            satisfy the bounds 0 < phi_1 < 1.
        phi_2 : float or np.array
            Volume fraction of component 2. Must
            satisfy the bounds
            0 < phi_1 + phi_2 < 1.


        Returns
        -------
        fe : float or np.array
            Free energy of a fully mixed,
            ternary system where the solutes
            have volume fractions phi_1 and phi_2.
        """

        return super().free_energy(phi_1,phi_2,self.chi_12,
                                   self.chi_11,self.chi_22)

    def free_energy(self,x):
        """
        Compute the free energy along a 1D curve
        in phi_1 phi_2 space.

        Parameters
        ----------
        x : float or np.array
            Value of one of independent variable
            (usually phi_1).

        Returns
        -------
        f : float or np.array
            Value of the free energy along the curve
            (x,y(x)) in phi_1 phi_2 space.
        """

        y = self.func(x,*self.args)
        
        return self._freeenergy(x,y)

    
    def free_energy_slope(self,x):
        """
        Compute the free energy derivative along
        a 1D curve in phi_1 phi_2 space.

        Parameters
        ----------
        x : float or np.array
            Value of one of independent variable
            (usually phi_1).

        Returns
        -------
        dfdx : float or np.array
            Value of the free energy derivative along
            the curve (x,y(x)) in phi_1 phi_2 space.
        """
        
        y = self.func(x,*self.args)
        dy = self.dfunc(x,*self.args)
        s = 1-x-y

        return (np.log(x)+np.log(y)*dy
                -np.log(s)*(1+dy)
                +self.chi_11*(1-2*x)
                +self.chi_22*(1-2*y)*dy
                -2*self.chi_12*y
                -2*self.chi_12*x*dy)

    def commontangent_eqns(self,phis):
        """
        Computes two non-linear equations, which
        when equal to zero indicate that a common
        tangent construction has been successfully
        found. Use a root-finding algorithm on this
        function in order to successfully find the
        common tangent construction.

        Parameters
        ----------
        phis : list or array with 2 components
            phi_1 coordinates (typically a guess
            for the two points where the common
            tangent intersects the free energy).

        Returns
        -------
        gs : list of length 2
            The two non-linear equations which,
            when set to zero, yield the common
            tangent construction.
        """

        derivA = self.free_energy_slope(phis[0])
        derivB = self.free_energy_slope(phis[1])

        return [derivB-derivA,
                -1*derivB*phis[1]+self.free_energy(phis[1])
                +derivA*phis[0]-self.free_energy(phis[0])]
    
class ChemEq3_2phase(ChemEq3_3phase):


    """
    Child class of ChemEq3_6phase. Does essentially
    the same thing as ChemEq3_6phase, except it only
    looks for coexistence of two phases. Therefore,
    there are fewer dimensions in phi-chi parameter
    space (6 instead of 15). By the Gibbs phase rule,
    four of these dimensions will be free parameters
    in three-phase coexistence. These four parameters
    will be selected to be the chi parameters and
    the phi_1A volume fraction (see
    the Attributes section below).

    Attributes
    ----------
    phi_1A : float
        Volume fraction of component 1, in phase A.
        Must satisfy 0 < phi_1A < 1.
    chi_12 : float
        The value of the chi_12 interaction parameter.
    chi_11 : float, optional
        The value of the chi_11 interaction parameter.
    chi_22 : float
        The value of the chi_22 interaction parameter.

    Rootfinding Methods
    -------------------

    rootfind_eqns(self,x)

        Computes the set of non-linear equations
        (all must be set equal to zero to solve) which
        are used both directly for rootfinding
        algorithms or indirectly in the definition
        of objective function (for minimisation). Pass
        this method to e.g. scipy.optimise.root to try 
        and find chemical equilibrium.

    rootfind_jacobian(self,x)
        Computes the Jacobian matrix of the rootfind_eqns
        method above. Pass this method (along with the
        rootfind_eqns method above) to e.g.
        scipy.optimise.root to try and find chemical
        equilibrium.

    Optimisation Methods
    --------------------
    objective(self,x)
        Defines and computes an objective function for
        an optimisation approach to determining chemical
        equilibrium. It computes the squared 2-norm of the
        3 equations of chemical equilibrium defined in
        rootfind_eqns above. Pass this method to e.g.
        scipy.optimise.minimise to try and find chemical
        equilibrium.

    obj_jac(self,x)
        Computes the Jacobian of the objective function.
        Pass this method (along with the objective method
        above) to e.g. scipy.optimise.minimise to try and
        find chemical equilibrium.

    obj_hess(self,x)
        Computes the 3x3 Hessian of the objective function.
        Pass this method (along with the objective method
        and the obj_jac method above) to e.g.
        scipy.optimise.minimise to try and find chemical
        equilibrium. WARNING: It seems like using this
        Hessian in any optimisation routine leads to
        only finding the trivial solution, regardless of
        initial condition. It might be due to a coding
        error or a convexity issue of the objective
        function (I have tested for the latter extensively
        using numerical derivatives and have yet to find
        a bug).

    Other Public Methods
    --------------------

    phis_to_x(self,phi_1B,phi_2A,phi_2B)
        Move phi values into a single numpy array, so
        that this array can be used in optimisation or
        root finding. It just returns the array x
        where
        
            x = np.array([phi_1A,phi_2A,phi_1B,
                          phi_2B,phi_1C,phi_2C])

    get_phi1s_phi2s(self,x)
        Convert the x array determined via either
        optimisation or root finding, back into
        an array of phi_1 values in the 2 phases
        and an array of phi_2 values in the 2 phases.
        It just returns the two lists
            phi_1s = [self.phi_1A,x[1]]
            phi_2s = [x[0],x[2]]


    """
    
    def __init__(self,phi_1A,chi_12,chi_11=1,chi_22=1,
                 largenumber = 1e20,check_bounds = True):

        """
        Initialise all attributes.

        Parameters
        ----------
        phi_1A : float
            The volume fraction of component 1 in the A
            phase.
        chi_12 : float
            The value of the chi_12 interaction parameter.
        chi_11 : float, optional
            The value of the chi_11 interaction parameter.
        chi_22 : float, optional
            The value of the chi_22 interaction parameter.
        largenumber : float, optional
            A large number to return if the volume
            fractions do not obey the volume constraints.
        check_bounds : boolean, optional
            Replaces nans (from volume constraints being
            broken) in rootfind_eqns method with
            largenumber defined above.
        """

        self.phi_1A = phi_1A
        self.chi_12 = chi_12
        self.chi_11 = chi_11
        self.chi_22 = chi_22
        self.largenumber=largenumber
        self.check_bounds = check_bounds
        
        return

    def phis_to_x(self,phi_1B,phi_2A,phi_2B):
        """
        Move phi values into a single numpy array, so
        that this array can be used in optimisation or
        root finding. 

        Parameters
        ----------
        phi_1B : float
            Volume fraction of component one in phase B.
        phi_2A : float
            Volume fraction of component two in phase A.
        phi_2B : float
            Volume fraction of component two in phase B.

        Returns
        -------
        x : np.array of length 3
            x = np.array([phi_2A,phi_1B,phi_2B])

        Notes
        -----
        All the volume fractions must be greater than
        zero, and for i = A,B must satisfy
        0 < phi_1i + phi_2i < 1.

        """

        x = np.array([phi_2A,phi_1B,phi_2B])
        return x

    def get_phi1s_phi2s(self,x):

        """

        Convert the x array determined via either
        optimisation or root finding, back into
        an array of phi_1 values in the 2 phases
        and an array of phi_2 values in the 2 phases.

        Parameters
        ----------
        x : np.array of length 3
            Array with values of the volume fractions
            in the two phases, i.e.

            x = np.array([phi_2A,phi_1B,phi_2B])
        
        Returns
        -------
        phi_1s : list
            phi_1s = [self.phi_1A,x[1]]
        phi_2s : list
            phi_2s = [x[0],x[2]]
        """

        
        phi_1s = [self.phi_1A,x[1]]
        phi_2s = [x[0],x[2]]

        return phi_1s,phi_2s


    def _bounds_checker(self,phi_1B,phi_2A,phi_2B):
        # return True if volume constraints are broken
        if (phi_1B<=0 or phi_2A<= 0 or phi_2B<= 0
            or phi_1B>= 1 or phi_2A >= 1 or phi_2B >= 1
            or phi_1B+phi_2B > 1 or self.phi_1A+phi_2A > 1):
            return True
        else:
            return False
        return
    
    
    def rootfind_eqns(self,x):
        """
        Computes the set of non-linear equations
        (all must be set equal to zero to solve) which
        are used both directly for rootfinding
        algorithms or indirectly in the definition
        of objective function (for minimisation). Pass
        this method to e.g. scipy.optimise.root to try 
        and find chemical equilibrium.

        Parameters
        ----------
        x : np.array of length 3
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_2A,phi_1B,phi_2B])


        Returns
        -------
        gs : list of floats
            List of all the equations of chemical
            equilibrium, in the order g0_AB, g1_AB,
            g2_AB.

        """


        phi_1s,phi_2s = self.get_phi1s_phi2s(x)
        
        outs = []

        if (self.check_bounds and
            self._bounds_checker(phi_1s[1],phi_2s[0],
                                 phi_2s[1])):
                outs = [self.largenumber,self.largenumber,
                        self.largenumber]
        else:
            for i in range(3):
                outs.append(self.g_i_pq(i,0,1,phi_1s,
                                        phi_2s))
    
        return outs


    def rootfind_jacobian(self,x):
        """
        Computes the Jacobian matrix of the rootfind_eqns
        method above. Pass this method (along with the
        rootfind_eqns method above) to e.g.
        scipy.optimise.root to try and find chemical
        equilibrium.

        Parameters
        ----------
        x : np.array of length 6
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_2A,phi_1B,phi_2B])

        Returns
        -------
        J : 3x3 np.array
            Jacobian of the rootfind_eqns method, with
            rows in the order 0_AB, 1_AB,
            2_AB and columns in the
            order phi_2A, phi_1B, phi_2B.

        """

        
        phi_1s,phi_2s = self.get_phi1s_phi2s(x)

        J11 = -1*self.dg_0_2(phi_1s[0],phi_2s[0])
        J12 = self.dg_0_1(phi_1s[1],phi_2s[1])
        J13 = self.dg_0_2(phi_1s[1],phi_2s[1])

        J21 = -1*self.dg_1_2(phi_1s[0],phi_2s[0])
        J22 = self.dg_1_2(phi_1s[1],phi_2s[1])
        J23 = self.dg_1_2(phi_1s[1],phi_2s[1])

        J31 = -1*self.dg_2_2(phi_1s[0],phi_2s[0])
        J32 = self.dg_2_1(phi_1s[1],phi_2s[1])
        J33 = self.dg_2_2(phi_1s[1],phi_2s[1])

        return np.array([[J11,J12,J13],
                         [J21,J22,J23],
                         [J31,J32,J33]])


    def objective(self,x):
        """
        Defines and computes an objective function for
        an optimisation approach to determining chemical
        equilibrium. It computes the squared 2-norm of the
        3 equations of chemical equilibrium defined in
        rootfind_eqns above. Pass this method to e.g.
        scipy.optimise.minimise to try and find chemical
        equilibrium.

        Parameters
        ----------
        x : np.array of length 3
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_2A,phi_1B,phi_2B])

        Returns
        -------
        g : float
            Square of the 2-norm of the rootfind_eqns
            method defined above, evaluated at x.

        """

        outs = self.rootfind_eqns(x)
        out = outs[0]*outs[0] + outs[1]*outs[1] + outs[2]*outs[2]

        return out

    def obj_jac(self,x):
        """
        Computes the Jacobian of the objective function.
        Pass this method (along with the objective method
        above) to e.g. scipy.optimise.minimise to try and
        find chemical equilibrium.

        Parameters
        ----------
        x : np.array of length 3
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_2A,phi_1B,phi_2B])

        Returns
        -------
        J : np.array of length 3
            Gradient of the objective function with
            respect to x.
        """

        # order of gradients is phi_1A,phi_2A,phi_1B,
        # phi_2B,phi_1C,phi_2c

        phi_1s,phi_2s = self.get_phi1s_phi2s(x)

        obj_vec = np.array(self.rootfind_eqns(x))


        j1 = -2*obj_vec[0]*self.dg_0_2(phi_1s[0],phi_2s[0])
        j1 += -2*obj_vec[1]*self.dg_1_2(phi_1s[0],phi_2s[0])
        j1 += -2*obj_vec[2]*self.dg_2_2(phi_1s[0],phi_2s[0])

        j2 = 2*obj_vec[0]*self.dg_0_1(phi_1s[1],phi_2s[1])
        j2 += 2*obj_vec[1]*self.dg_1_1(phi_1s[1],phi_2s[1])
        j2 += 2*obj_vec[2]*self.dg_2_1(phi_1s[1],phi_2s[1])

        j3 = 2*obj_vec[0]*self.dg_0_2(phi_1s[1],phi_2s[1])
        j3 += 2*obj_vec[1]*self.dg_1_2(phi_1s[1],phi_2s[1])
        j3 += 2*obj_vec[2]*self.dg_2_2(phi_1s[1],phi_2s[1])

        return np.array([j1,j2,j3])

    
    def obj_hess(self,x):
        """
        Computes the 3x3 Hessian of the objective function.
        Pass this method (along with the objective method
        and the obj_jac method above) to e.g.
        scipy.optimise.minimise to try and find chemical
        equilibrium. WARNING: It seems like using this
        Hessian in any optimisation routine leads to
        only finding the trivial solution, regardless of
        initial condition. It might be due to a coding
        error or a convexity issue of the objective
        function (I have tested for the latter extensively
        using numerical derivatives and have yet to find
        a bug).

        Parameters
        ----------
        x : np.array of length 3
            Array with values of the volume fractions
            in the three phases, i.e.

            x = np.array([phi_2A,phi_1B,phi_2B])

        Returns
        -------
        h : 3x3 np.array
            Hessian of the objective function with
            respect to x.

        """
        

        phi_1s,phi_2s = self.get_phi1s_phi2s(x)
        obj_vec = np.array(self.rootfind_eqns(x))

        H11 = 0
        H11 += 2*(self.dg_0_2(phi_1s[0],phi_2s[0]))**2
        H11 += 2*(self.dg_1_2(phi_1s[0],phi_2s[0]))**2
        H11 += 2*(self.dg_2_2(phi_1s[0],phi_2s[0]))**2
        H11 += -2*obj_vec[0]*self.ddg_0_22(phi_1s[0],phi_2s[0])
        H11 += -2*obj_vec[1]*self.ddg_1_22(phi_1s[0],phi_2s[0])
        H11 += -2*obj_vec[2]*self.ddg_2_22(phi_1s[0],phi_2s[0])
        
        H12 = 0

        H12 += (-2*self.dg_0_2(phi_1s[0],phi_2s[0])
               *self.dg_0_1(phi_1s[1],phi_2s[1]))
        H12 += (-2*self.dg_1_2(phi_1s[0],phi_2s[0])
                *self.dg_1_1(phi_1s[1],phi_2s[1]))
        H12 += (-2*self.dg_2_2(phi_1s[0],phi_2s[0])
                *self.dg_2_1(phi_1s[1],phi_2s[1]))
        

        H13 = 0
        H13 += (-2*self.dg_0_2(phi_1s[0],phi_2s[0])
               *self.dg_0_2(phi_1s[1],phi_2s[1]))
        H13 += (-2*self.dg_1_2(phi_1s[0],phi_2s[0])
                *self.dg_1_2(phi_1s[1],phi_2s[1]))
        H13 += (-2*self.dg_2_2(phi_1s[0],phi_2s[0])
                *self.dg_2_2(phi_1s[1],phi_2s[1]))
        
        
        H22 = 0
        H22 += 2*(self.dg_0_1(phi_1s[1],phi_2s[1]))**2
        H22 += 2*(self.dg_1_1(phi_1s[1],phi_2s[1]))**2
        H22 += 2*(self.dg_2_1(phi_1s[1],phi_2s[1]))**2
        H22 += 2*obj_vec[0]*self.ddg_0_11(phi_1s[1],phi_2s[1])
        H22 += 2*obj_vec[1]*self.ddg_1_11(phi_1s[1],phi_2s[1])
        H22 += 2*obj_vec[2]*self.ddg_2_11(phi_1s[1],phi_2s[1])


        H23 = 0

        H23 += (2*self.dg_0_1(phi_1s[1],phi_2s[1])
                *self.dg_0_2(phi_1s[1],phi_2s[1]))
        H23 += (2*self.dg_1_1(phi_1s[1],phi_2s[1])
                *self.dg_1_2(phi_1s[1],phi_2s[1]))
        H23 += (2*self.dg_2_1(phi_1s[1],phi_2s[1])
                *self.dg_2_2(phi_1s[1],phi_2s[1]))

        H23 += 2*obj_vec[0]*self.ddg_0_12(phi_1s[1],phi_2s[1])
        H23 += 2*obj_vec[1]*self.ddg_1_12(phi_1s[1],phi_2s[1])
        H23 += 2*obj_vec[2]*self.ddg_2_12(phi_1s[1],phi_2s[1])


        H33 = 0
        H33 += 2*(self.dg_0_2(phi_1s[1],phi_2s[1]))**2
        H33 += 2*(self.dg_1_2(phi_1s[1],phi_2s[1]))**2
        H33 += 2*(self.dg_2_2(phi_1s[1],phi_2s[1]))**2
        H33 += 2*obj_vec[0]*self.ddg_0_22(phi_1s[1],phi_2s[1])
        H33 += 2*obj_vec[1]*self.ddg_1_22(phi_1s[1],phi_2s[1])
        H33 += 2*obj_vec[2]*self.ddg_2_22(phi_1s[1],phi_2s[1])

        return np.array([[H11,H12,H13],
                         [H12,H22,H23],
                         [H13,H23,H33]])


    

if __name__ == "__main__":

    # test derivative functions

    import matplotlib.pyplot as plt


    test_gs = False
    test_objective = True
    if test_gs == True:
        ch = ChemEq3_3phase(chi_12=4,chi_11=2,chi_22=1)
        
        # starting with phi_1A varying!

        xs = np.linspace(0.05,0.5,num=99,endpoint=False)
        ys = np.linspace(0.05,0.5,num=99,endpoint=False)

        phi_1B = 0.1
        phi_2B = 0.6


        XX,YY = np.meshgrid(xs,ys)

        phi_1s = [XX,phi_1B]
        phi_2s = [YY,phi_2B]

        # test derivative of g_0^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and
        # phi_2^{(\beta)}

        # first derivatives

        g_0_01 = ch.g_i_pq(0,0,1,phi_1s,phi_2s)

        analytic_xs = -1*ch.dg_0_1(XX,YY)
        analytic_ys = -1*ch.dg_0_2(XX,YY)
        dgys, dgxs = np.gradient(g_0_01,ys,xs)

        plt.plot(xs,dgxs[4,:],'ro')
        plt.plot(xs,analytic_xs[4,:],'k-')
        plt.show()

        plt.plot(ys,dgys[:,10],'ro')
        plt.plot(ys,analytic_ys[:,10],'k-')
        plt.show()

        # second derivative of g_0^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_1^{(\beta)}    
        print('second derivs g_0')


        analytic_xsxs = -1*ch.ddg_0_11(XX,YY)
        analytic_xsys = -1*ch.ddg_0_12(XX,YY)
        analytic_ysys = -1*ch.ddg_0_22(XX,YY)
        ddgyxs, ddgxxs = np.gradient(dgxs,ys,xs)
        ddgyys, ddgxys = np.gradient(dgys,ys,xs)

        plt.plot(xs,ddgxxs[4,:],'ro')
        plt.plot(xs,analytic_xsxs[4,:],'k-')
        plt.show()

        plt.plot(xs,ddgyxs[4,:],'ro')
        plt.plot(xs,analytic_xsys[4,:],'k-')
        plt.show()

        plt.plot(ys,ddgyys[:,10],'ro')
        plt.plot(ys,analytic_ysys[:,10],'k-')
        plt.show()

        plt.plot(ys,ddgxys[:,10],'ro')
        plt.plot(ys,analytic_xsys[:,10],'k-')
        plt.show()


        # test derivative of g_1^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and
        # phi_2^{(\beta)}

        g_1_01 = ch.g_i_pq(1,0,1,phi_1s,phi_2s)

        analytic_xs = -1*ch.dg_1_1(XX,YY)
        analytic_ys = -1*ch.dg_1_2(XX,YY)
        dgys, dgxs = np.gradient(g_1_01,ys,xs)

        plt.plot(xs,dgxs[4,:],'ro')
        plt.plot(xs,analytic_xs[4,:],'k-')
        plt.show()

        plt.plot(ys,dgys[:,10],'ro')
        plt.plot(ys,analytic_ys[:,10],'k-')
        plt.show()


        # second derivative of g_1^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_1^{(\beta)}    

        print('second derivs g_1')
        analytic_xsxs = -1*ch.ddg_1_11(XX,YY)
        analytic_xsys = -1*ch.ddg_1_12(XX,YY)
        analytic_ysys = -1*ch.ddg_1_22(XX,YY)
        ddgyxs, ddgxxs = np.gradient(dgxs,ys,xs)
        ddgyys, ddgxys = np.gradient(dgys,ys,xs)

        plt.plot(xs,ddgxxs[4,:],'ro')
        plt.plot(xs,analytic_xsxs[4,:],'k-')
        plt.show()

        plt.plot(xs,ddgyxs[4,:],'ro')
        plt.plot(xs,analytic_xsys*np.ones_like(xs),'k-')
        plt.show()

        plt.plot(ys,ddgyys[:,10],'ro')
        plt.plot(ys,analytic_ysys*np.ones_like(ys),'k-')
        plt.show()

        plt.plot(ys,ddgxys[:,10],'ro')
        plt.plot(ys,analytic_xsys*np.ones_like(ys),'k-')
        plt.show()


        # test derivative of g_2^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and
        # phi_2^{(\beta)}

        g_2_01 = ch.g_i_pq(2,0,1,phi_1s,phi_2s)

        analytic_xs = -1*ch.dg_2_1(XX,YY)
        analytic_ys = -1*ch.dg_2_2(XX,YY)
        dgys, dgxs = np.gradient(g_2_01,ys,xs)

        plt.plot(xs,dgxs[4,:],'ro')
        plt.plot(xs,analytic_xs[4,:],'k-')
        plt.show()

        plt.plot(ys,dgys[:,10],'ro')
        plt.plot(ys,analytic_ys[:,10],'k-')
        plt.show()

        # second derivative of g_1^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_1^{(\beta)}    

        print('second derivs g_2')
        analytic_xsxs = -1*ch.ddg_2_11(XX,YY)
        analytic_xsys = -1*ch.ddg_2_12(XX,YY)
        analytic_ysys = -1*ch.ddg_2_22(XX,YY)
        ddgyxs, ddgxxs = np.gradient(dgxs,ys,xs)
        ddgyys, ddgxys = np.gradient(dgys,ys,xs)

        plt.plot(xs,ddgxxs[4,:],'ro')
        plt.plot(xs,analytic_xsxs*np.ones_like(xs),'k-')
        plt.show()

        plt.plot(xs,ddgyxs[4,:],'ro')
        plt.plot(xs,analytic_xsys*np.ones_like(xs),'k-')
        plt.show()

        plt.plot(ys,ddgyys[:,10],'ro')
        plt.plot(ys,analytic_ysys[:,10],'k-')
        plt.show()

        plt.plot(ys,ddgxys[:,10],'ro')
        plt.plot(ys,analytic_xsys*np.ones_like(ys),'k-')
        plt.show()

    #==========================================================#
    #                                                          #
    #    now checking objective hessian for chemeq3_2phase     #
    #                                                          #
    #==========================================================#


    if test_objective == True:
        phi_1A = 0.2    
        ch = ChemEq3_2phase(phi_1A = phi_1A,
                            chi_12=7,chi_11=-1,chi_22=3,
                            check_bounds=False)


        xs = np.linspace(0.05,0.8,num=99,endpoint=False)
        ys = np.linspace(0.05,0.5,num=99,endpoint=False)
        zs = np.linspace(0.05,0.5,num=99,endpoint=False)

        # need three combinations of the three variables
        # to look at hessian

        # start with phi_2A and phi_1B
        XX,YY = np.meshgrid(xs,ys)
        phi_2B = zs[5]

        x = [XX,YY,phi_2B]

        obj = ch.objective(x)

        jac= ch.obj_jac(x)
        hess = ch.obj_hess(x)
        
        #test derivatives of obj with respect to phi_2A
        # and phi_1B
        # first derivatives

        analytic_xs = jac[0]

        analytic_ys = jac[1]
        dgys, dgxs = np.gradient(obj,ys,xs)

        plt.plot(xs,dgxs[4,:],'ro')
        plt.plot(xs,analytic_xs[4,:],'k-')
        plt.show()

        plt.plot(ys,dgys[:,10],'ro')
        plt.plot(ys,analytic_ys[:,10],'k-')
        plt.show()

        # second derivative of g_0^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_1^{(\beta)}    



        analytic_xsxs = hess[0,0]
        analytic_xsys = hess[0,1]
        analytic_ysys = hess[1,1]
        ddgyxs, ddgxxs = np.gradient(dgxs,ys,xs)
        ddgyys, ddgxys = np.gradient(dgys,ys,xs)

        plt.plot(xs,ddgxxs[4,:],'ro')
        plt.plot(xs,analytic_xsxs[4,:],'k-')
        plt.show()

        plt.plot(xs,ddgyxs[4,:],'ro')
        plt.plot(xs,analytic_xsys[4,:],'k-')
        plt.show()

        plt.plot(ys,ddgyys[:,10],'ro')
        plt.plot(ys,analytic_ysys[:,10],'k-')
        plt.show()

        plt.plot(ys,ddgxys[:,10],'ro')
        plt.plot(ys,analytic_xsys[:,10],'k-')
        plt.show()
        
        # next check  phi_2A and phi_2B
        XX,ZZ = np.meshgrid(xs,zs)
        phi_1B = ys[5]

        x = [XX,phi_1B,ZZ]

        obj = ch.objective(x)

        jac= ch.obj_jac(x)
        hess = ch.obj_hess(x)
        
        #test derivatives of obj with respect to phi_2A
        # and phi_2B
        # first derivatives

        analytic_xs = jac[0]

        analytic_zs = jac[2]
        dgzs, dgxs = np.gradient(obj,zs,xs)

        plt.plot(xs,dgxs[4,:],'ro')
        plt.plot(xs,analytic_xs[4,:],'k-')
        plt.show()

        plt.plot(zs,dgzs[:,10],'ro')
        plt.plot(zs,analytic_zs[:,10],'k-')
        plt.show()

        # second derivative of g_0^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_1^{(\beta)}    


        analytic_xsxs = hess[0,0]
        analytic_xszs = hess[0,2]
        analytic_zszs = hess[2,2]
        ddgyxs, ddgxxs = np.gradient(dgxs,zs,xs)
        ddgyzs, ddgxzs = np.gradient(dgzs,zs,xs)

        plt.plot(xs,ddgxxs[4,:],'ro')
        plt.plot(xs,analytic_xsxs[4,:],'k-')
        plt.show()

        plt.plot(xs,ddgyxs[4,:],'ro')
        plt.plot(xs,analytic_xszs[4,:],'k-')
        plt.show()

        plt.plot(zs,ddgyzs[:,10],'ro')
        plt.plot(zs,analytic_zszs[:,10],'k-')
        plt.show()

        plt.plot(zs,ddgxzs[:,10],'ro')
        plt.plot(zs,analytic_xszs[:,10],'k-')
        plt.show()

                
        # finally check phi_1B and phi_2B
        YY,ZZ = np.meshgrid(ys,zs)
        phi_2A = xs[5]

        x = [phi_2A,YY,ZZ]

        obj = ch.objective(x)

        jac= ch.obj_jac(x)
        hess = ch.obj_hess(x)
        
        #test derivatives of obj with respect to phi_2A
        # and phi_2B
        # first derivatives

        analytic_ys = jac[1]

        analytic_zs = jac[2]
        dgzs, dgys = np.gradient(obj,zs,ys)

        plt.plot(ys,dgys[4,:],'ro')
        plt.plot(ys,analytic_ys[4,:],'k-')
        plt.show()

        plt.plot(zs,dgzs[:,10],'ro')
        plt.plot(zs,analytic_zs[:,10],'k-')
        plt.show()

        # second derivative of g_0^{(\alpha\beta)}
        # with respect to phi_1^{(\beta)} and phi_1^{(\beta)}    


        analytic_ysys = hess[1,1]
        analytic_yszs = hess[1,2]
        analytic_zszs = hess[2,2]
        ddgyys, ddgxys = np.gradient(dgys,zs,ys)
        ddgyzs, ddgxzs = np.gradient(dgzs,zs,ys)

        plt.plot(ys,ddgxys[4,:],'ro')
        plt.plot(ys,analytic_ysys[4,:],'k-')
        plt.show()

        plt.plot(ys,ddgyys[4,:],'ro')
        plt.plot(ys,analytic_yszs[4,:],'k-')
        plt.show()

        plt.plot(zs,ddgyzs[:,10],'ro')
        plt.plot(zs,analytic_zszs[:,10],'k-')
        plt.show()

        plt.plot(zs,ddgxzs[:,10],'ro')
        plt.plot(zs,analytic_yszs[:,10],'k-')
        plt.show()
