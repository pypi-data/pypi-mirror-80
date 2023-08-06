import numpy as np

def chi_spinodal(phi):

    return 1./(2*phi*(1-phi))

class ChemEq2():

    def __init__(self,chi=1):

        self.chi = chi

        return

    def eqns(self,x):

        return [np.log((1-x[0])/(1-x[1]))
                +self.chi*(x[0]**2-x[1]**2),
                np.log(x[0]/x[1])
                +self.chi*((1-x[0])**2-(1-x[1])**2)]


    def jacobian(self,x):

        return np.array([[-1./(1-x[0])+2*self.chi*x[0],
                      1./(1-x[1])-2*self.chi*x[1]],
                     [1./x[0]-2*self.chi*(1-x[0]),
                      -1./x[1]+2*self.chi*(1-x[1])]])




