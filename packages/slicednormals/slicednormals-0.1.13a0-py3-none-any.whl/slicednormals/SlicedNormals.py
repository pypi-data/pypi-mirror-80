import numpy as np
from itertools import combinations_with_replacement as cwr
from itertools import chain
from scipy.optimize import minimize as scimin
from scipy.stats import chi2 as chi2
from slicednormals import HyperEllipse as HE
from functools import reduce
from operator import mul, truediv, sub, neg

class SNDist():
    "Ref: Improving the Uncertainty Quantifcation of Sliced Normal Distributions by Scaling the Covariance Matrix Colbert et al 2020"
    def __init__(self, Data, DoF):
        self.Data = Data
        self.DoF = DoF
        self.mu = None
        self.Sigma = None
    
    def SN_Phi(self, Data):
        # Unnormalised log-likelihood
        Z_Data = ZExpand(Data, self.DoF)
        return map(Phi, Z_Data - self.mu, [self.Sigma]*len(Data))
    
class Basic_SN(SNDist):
    def __init__(self, Data, DoF):
        super().__init__(Data, DoF)
        self.Z_Data = np.array([*ZExpand(self.Data, self.DoF)])
        self.mu = np.mean(self.Z_Data, 0)
        self.Sigma = Nearest_PSD(np.cov(self.Z_Data, ddof = 0, rowvar = False))
    
class Scaled_SN(Basic_SN):
    def __init__(self, Data, DoF, No_Supp_Samples, Retain_Supp_Samples = False):
        super().__init__(Data, DoF)
        if Retain_Supp_Samples:
            self.Hyper_Ellipse = HE.Hyper_Ellipse(Data = self.Data)
            self.Supp_Samples = self.Hyper_Ellipse.Sample(No_Supp_Samples)
            self.Z_Supp_Samples = np.array(*ZExpand(self.Supp_Samples, self.DoF))
            self.Z_Supp_Phi = -1*np.array([*map(Phi, self.Z_Supp_Samples - self.mu, [self.Sigma]*No_Supp_Samples)])
            self.Z_Supp_PhiSumExp = sum(map(np.exp, self.Z_Supp_Phi))
            self.Z_Data_PhiSum = -1 * sum(map(Phi, self.Z_Data - self.mu, [self.Sigma]*len(Data)))
            objfun = lambda gamma: -((-len(self.Data) * np.log(sum(np.exp(self.Z_Supp_Phi * gamma)))) + gamma * self.Z_Data_PhiSum)
        else:
            Hyper_Ellipse = HE.Hyper_Ellipse(Data = self.Data)
            Supp_Samples = Hyper_Ellipse.Sample(No_Supp_Samples)
            Z_Supp_Samples = map(sub, ZExpand(Supp_Samples, self.DoF), [self.mu]*No_Supp_Samples)
            Z_Supp_Phi = np.array(list(map(Phi, Z_Supp_Samples, [self.Sigma]*No_Supp_Samples)))
            Z_Data_PhiSum = sum(map(np.exp, map(neg, Z_Supp_Phi)))
            objfun = lambda gamma: -((-len(self.Data) * np.log(sum(np.exp(Z_Supp_Phi * gamma)))) + gamma * Z_Data_PhiSum)
        self.gamma = scimin(objfun, 1e-9, bounds=((0, None),)).x
        self.Sigma = self.Sigma/self.gamma

def Phi(Dmu, Sigma):
    # Unnormalised log-likelihood
    # Dmu = Data - mu
    return sum((Dmu)*np.linalg.solve(Sigma, (Dmu)))/2

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

def ZExpand(P_Data, DoF = 1):
    return map(ZExpandFunc, P_Data, [DoF]*len(P_Data))

def ZExpandFunc(Data, DoF):
    return [reduce(mul, C) for C in chain.from_iterable([cwr(Data, D) for D in range(1, DoF + 1)])]