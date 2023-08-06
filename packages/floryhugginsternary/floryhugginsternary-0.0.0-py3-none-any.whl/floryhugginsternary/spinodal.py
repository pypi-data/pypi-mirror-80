import numpy as np

class Spinodal():

    """
    This class is used to determine the spinodal surface
    of a ternary (three component) system in the
    Flory-Huggins framework. Important to note that
    for the Flory-Huggins model, chi_12 degrees of freedom
    are quadratic, so only quadratic surfaces in chi_12
    can be modelled. The surfaces will be looked at in
    chi_12, phi_1, phi_2 space (holding chi_11 and chi_22
    constant).

    Attributes
    ----------
    chi_11 : float, optional
        The value of the chi_11 interaction parameter.
    chi_22 : float
        The value of the chi_22 interaction parameter.

    Methods
    -------
    convextest(self,phi_1,phi_2,chi_12)
        Determine whether a point in (chi_12,phi_1,phi_2)
        has a convex free energy or not.

    chi_12_spinodal(self,phi_1,phi_2,root='+')
        Find the value of chi_12 (if it exists) on the
        spinodal surface, given phi_1 and phi_2. The
        root parameter is used to select which root
        of the equation of the surface to select.

    rootfind_spinodal_eqn(self,phi_1,phi_2,chi_12)
        A nonlinear equation for the spinodal surface.
        Input this into e.g. scipy.optimize.root to
        determine a point on the spinodal surface for
        fixed phi_2 and chi_12. This method is only
        useful when chi_12 must be fixed AND exact values
        of the spinodal are required. Otherwise
        it is much easier to find the spinodal via
        the method chi_12_spinodal above, and then use
        something like plt.contour() to show the
        spinodal.

        
    """
    
    def __init__(self,chi_11=1,chi_22=1):
        """
        Initialise all attributes.

        Parameters
        ----------
        chi_11 : float, optional
            The value of the chi_11 interaction parameter.
        chi_22 : float, optional
            The value of the chi_22 interaction parameter.
        """


        self.chi_11 = chi_11
        self.chi_22 = chi_22

        return

        

    def convextest(self,phi_1,phi_2,chi_12):

        """
        Compute the determinant of the Hessian in phi_1,
        phi_2 space to see where the free energy is 
        convext or not.

        Parameters
        ----------
        phi_1 : float
            Volume fraction of component one.
        phi_2 : float
            Volume fraction of component two.
        chi_12 : float
            Value of chi_12 interaction parameter.

        Returns
        -------
        convexity : string
            convexity = 'convex' if the free energy
            is convex at the point (phi_1,phi_2,chi_12),
            convexity = 'concave' if concave, and
            convexity = 'saddle' if neither. If
            the volume fractions are outside of the
            domain of validity, then 'outofbounds'
            is returned.
        """

        if (phi_1 <= 0 or phi_2 <= 0
            or phi_1+phi_2 >= 1):
            return 'outofbounds'
        

        phi_s = (1-phi_1-phi_2)
        
        dxxf = ((1-phi_2-2*phi_1*phi_s*self.chi_11)
                /(phi_1*phi_s))
        
        dyyf = ((1-phi_1-2*phi_2*phi_s*self.chi_22)
                /(phi_2*phi_s))
        
        dxyf = (1-2*phi_s*chi_12)/phi_s
        
        D = dxxf*dyyf-dxyf*dxyf

        if D >0:
            if dxxf > 0:
                return 'convex'
            else:
                return 'concave'
        elif D<0:
            return 'saddle'
        else:
            return 'spinodal'

        return
    


    def chi_12_spinodal(self,phi_1,phi_2,root='+'):

        """
        Find the value of chi_12 (if it exists) on the
        spinodal surface, given phi_1 and phi_2. The
        root parameter is used to select which root
        of the equation of the surface to select.

        Parameters
        ----------
        phi_1 : float or np.array
            Volume fraction of component one.
        phi_2 : float or np.array
            Volume fraction of component two.
        root : string, optional
            Indicate which root of the spinodal surface
            (which is always quadratic) to plot.
            Anything other than root='+' will look
            for a negative chi_12 surface.

        Returns
        -------
        chi_12 : float or np.array
            Return the location of the spinodal surface
            for the values of phi_1 and phi_2 provided.
            An interesting case might be e.g. to use a
            np.meshgrid of phi_1 and phi_2 values, which
            should generate the spinodal surface for
            either chi_12>0 or chi_12<0 (for root='+'
            and root != '+', respectively).
            
        """

        phi_s = (1-phi_1-phi_2)

        D = (((1-phi_1)*(1-phi_2)
              -2*((1-phi_2)*phi_2*self.chi_22
                  +(1-phi_1)*phi_1*self.chi_11)
              *phi_s)/(phi_1*phi_2)
             + 4*self.chi_11*self.chi_22*phi_s**2)

        if root=='+':

            return 1./(2*phi_s)*(1+np.sqrt(D))

        else:

            return 1./(2*phi_s)*(1-np.sqrt(D))
        return

    def rootfind_spinodal_eqn(self,phi_1,phi_2,chi_12):
        """
        A nonlinear equation for the spinodal surface.
        Input this into e.g. scipy.optimize.root to
        determine a point on the spinodal surface for
        fixed phi_2 and chi_12. This method is only
        useful when chi_12 must be fixed AND exact values
        of the spinodal are required. Otherwise
        it is much easier to find the spinodal via
        the method chi_12_spinodal above, and then use
        something like plt.contour() to show the
        spinodal.

        Parameters
        ----------
        phi_1 : float
            Volume fraction of component one.
        phi_2 : float
            Volume fraction of component two.
        chi_12 : float
            Value of chi_12 parameter.

        
        Returns
        -------
        output : float
            value of the Hessian determinant multiplied
            by (1-phi_1-phi_2)**2*phi_1*phi_2. When this
            is zero, the point (phi_1,phi_2,chi_12) is
            on the spinodal surface.
        """
        phi_s = 1-phi_1-phi_2

        return ((1-phi_1)*(1-phi_2)-2*((1-phi_2)*phi_2*self.chi_22
                                       +(1-phi_1)*phi_1*self.chi_11
                                       -2*phi_1*phi_2*chi_12)*phi_s
                +4*(self.chi_22*self.chi_11-chi_12**2)
                *phi_1*phi_2*phi_s*phi_s-phi_1*phi_2)
    
