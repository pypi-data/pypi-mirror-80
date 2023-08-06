from SlicedNormals import Scaled_SN
from SlicedNormals import ZExpand, ZExpandFunc
#from slicednormals.SlicedNormals import Phi
from timeit import timeit
import numpy as np

setup = """\
from SlicedNormals import Scaled_SN
from SlicedNormals import ZExpand, ZExpandFunc
#from slicednormals.SlicedNormals import Phi
from timeit import timeit
import numpy as np
from operator import mul, add, sub, truediv

def pol2cart(phi, rho):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

dlen = 100
DoF = 9

[datax,datay] = pol2cart(np.random.rand(1,dlen)*2*np.pi-1, np.random.rand(1,dlen)*0.2+2)
data1 = np.append(datax.T, datay.T,1)
data2 = np.random.multivariate_normal([0, 0], [[0.8, 0.793],[0.793, 0.8]], int(dlen/2))
data3 = np.random.multivariate_normal([0, 0], [[0.8, -0.793],[-0.793, 0.8]], int(dlen/2))
Phdata = np.append(data1, np.append(data2, data3, 0), 0)

def datadraw():
    r = np.random.rand()
    if r <=0.5:
        [x, y] = pol2cart(np.random.rand(1)*2*np.pi-1, np.random.rand(1)*0.2+2)
        return np.hstack([x, y])
    elif r <= 0.75:
        return np.random.multivariate_normal([0, 0], [[0.8, 0.793],[0.793, 0.8]], 1)[0]
    else:
        return np.random.multivariate_normal([0, 0], [[0.8, -0.793],[-0.793, 0.8]], 1)[0]

data = np.vstack([datadraw() for n in range(0,50)])

def mapmean(data):
    return np.array([*map(truediv, map(sum, zip(*data)), [len(data)]*len(data[0]))])
print('Mapmean')
print(mapmean(data))
print('numpy')
print(np.mean(data, 0))
"""
def pol2cart(phi, rho):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

dlen = 100
DoF = 9

[datax,datay] = pol2cart(np.random.rand(1,dlen)*2*np.pi-1, np.random.rand(1,dlen)*0.2+2)
data1 = np.append(datax.T, datay.T,1)
data2 = np.random.multivariate_normal([0, 0], [[0.8, 0.793],[0.793, 0.8]], int(dlen/2))
data3 = np.random.multivariate_normal([0, 0], [[0.8, -0.793],[-0.793, 0.8]], int(dlen/2))
Phdata = np.append(data1, np.append(data2, data3, 0), 0)

def datadraw():
    r = np.random.rand()
    if r <=0.5:
        [x, y] = pol2cart(np.random.rand(1)*2*np.pi-1, np.random.rand(1)*0.2+2)
        return np.hstack([x, y])
    elif r <= 0.75:
        return np.random.multivariate_normal([0, 0], [[0.8, 0.793],[0.793, 0.8]], 1)[0]
    else:
        return np.random.multivariate_normal([0, 0], [[0.8, -0.793],[-0.793, 0.8]], 1)[0]

data = np.vstack([datadraw() for n in range(0,50)])
sn = Scaled_SN(data, 3, 1000)
print(timeit("np.mean(data,0)",setup,number=10000))
print(timeit("mapmean(data)",setup,number=10000))
print(-1*np.array([*sn.SN_Phi(data[0])]))