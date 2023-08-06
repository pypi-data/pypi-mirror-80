import numpy as np
from scipy.optimize import minimize as scimin
from scipy.stats import chi2
from scipy.special import gamma
from numpy.random import default_rng
from operator import truediv


class Hyper_Ellipse():
    "Ref: Improving the Uncertainty Quantifcation of Sliced Normal Distributions by Scaling the Covariance Matrix Colbert et al 2020"
    def __init__(self, Data = None):
        self.Data = Data
        if not self.Data is None:
            self.Fit_Hyper_Ellipse()

    def Fit_Hyper_Ellipse(self, Data = None):
        """ Calculates hyper-ellipse parameters following following "Improving the Uncertainty Quantifcation of Sliced Normal Distributions by Scaling the Covariance Matrix" Colbert et al 2020 Appendix A. """
        if not Data is None:
            self.Data = Data
        mu = np.array(list(mapmean(self.Data)))
        Sigma = Nearest_PSD(np.cov(self.Data.T, ddof = 0))
        L = np.linalg.cholesky(Sigma)
        TempQ = np.linalg.solve(Sigma,mu.T)
        Q0 = Nearest_PSD(np.vstack((np.hstack((mu@TempQ, -(TempQ))),np.vstack((-TempQ, np.linalg.solve(L,np.linalg.solve(L.T,np.eye(np.shape(L)[0]))))).T)))
        Q0 = np.linalg.cholesky(Q0)
        HE_Q = scimin(self.HE_objfun, Q0).x
        l = int(len(HE_Q)**0.5)
        HE_Q = np.reshape(HE_Q,(l,l))
        self.Q = HE_Q@HE_Q.T

        self.P_Matrix = self.Q[1:,1:]
        self.Chol_P_Matrix = np.linalg.cholesky(Nearest_PSD(self.P_Matrix))
        self.Sigma = np.linalg.solve(self.Chol_P_Matrix, np.linalg.solve(self.Chol_P_Matrix.T, np.eye(np.shape(self.Chol_P_Matrix)[0])))
        self.mu = np.linalg.solve(-self.P_Matrix, self.Q[1:, 0])
        self.Beta = self.FBeta(self.Q)
        self.Dims = np.shape(self.Data)[1]
        DMu = self.Data[np.argmax(np.linalg.norm(self.Data-self.mu, axis=1)),:] - self.mu
        self.Threshold = np.min(np.sum(DMu.T*(np.linalg.solve(self.Sigma, DMu.T)),0))*3
        self.Volume = (np.pi**(self.Dims/2)/gamma(1+self.Dims/2))*(np.linalg.det(self.Sigma)**0.5)*(self.Threshold**(self.Dims/2))

    def HE_objfun(self, Q):
        l = int(len(Q)**0.5)
        Q = np.reshape(Q,(l,l))
        Q = Q@Q.T
        return -((2*np.sum(np.log(np.diag(np.linalg.cholesky(Nearest_PSD(Q[1:,1:]))))))+self.FBeta(Q))

    def FBeta(self, Q):
        Beta = 1
        Beta = np.min(np.sum(-np.column_stack([np.ones(np.shape(self.Data)[0]),self.Data]).T*(Q@np.column_stack([np.ones(np.shape(self.Data)[0]),self.Data]).T)/2, 0))
        return Beta

    def Sample(self, No_Samples = None):
        return Dezert_Musso(self.Threshold, self.Sigma, self.mu, No_Samples)

def Dezert_Musso(Threshold,Sigma,mu,No_Samples):
    rng = default_rng()
    Dims = np.shape(Sigma)[0]

    HSphere = rng.standard_normal(size=(No_Samples, Dims))
    HSphere = HSphere.T/np.sqrt(np.sum(HSphere**2,1))

    Counter = rng.random(size=No_Samples)**(1/Dims)
    unif_sph = Counter*HSphere
    Chol_S = np.linalg.cholesky(Sigma)
    unif_ell = Chol_S.T @ unif_sph
    return (unif_ell*np.sqrt(Threshold)+np.array([mu]).T).T

def Nearest_PSD(Mat):
    try:
        np.linalg.cholesky(Mat)
        return Mat
    except np.linalg.LinAlgError:
        Symm = (Mat + Mat.T)/2
        [_, S, V] = np.linalg.svd(Symm)
        SymmPF = np.dot(V,np.dot(S,V.T))
        MatStar = (Mat + SymmPF)/2
        MatStar = (MatStar + MatStar.T)/2
        k = 0
        while True:
            try:
                np.linalg.cholesky(MatStar)
                break
            except np.linalg.LinAlgError:
                k += 1
                EMin = np.min(np.real(np.linalg.eig(MatStar)[0]))
                MatStar += (-EMin * k ** 2 + np.spacing(1)) * np.eye(np.shape(MatStar)[0])
        return MatStar

def mapmean(Data):
    return map(truediv, map(sum, zip(*Data)), [len(Data)]*len(Data[0]))