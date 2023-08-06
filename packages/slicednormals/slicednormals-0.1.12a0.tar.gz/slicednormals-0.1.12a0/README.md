# Sliced Normals for Python
This package allows sliced normal distributions to be fit to data. These are a highly flexible class of distributions capable of capturing characteristics of unusual data. Densities are not normalised, so the output of the Phi function is used for unnormalised densities. As such, these distributions cannot as yet produce density estimations of data points. However, sliced normals are simply a higher-dimensional gaussian distribution, and the mean and covariance can be utilised for sampling as with any other gaussian.

# Generating a Sliced Normal Distribution
A sliced normal distribution can be created by first providing the SNDist class with the target data, and then specifying the degree of expansion desired (DoF) and the class of Sliced Normal you want to use for modelling: basic or scaled. 
```sh
import slicednormals as sn
sn_fit = sn.basic_sn(data, dof = 3)
```
Crespo et al note that scaling improves the ability of the distribution to accurately reflect probability density, at the cost of increased computational effort. Scaled sliced normals require a large number of samples to be drawn across the support of the data.

```sh
sn_fit = sn.scaled_sn(data, 1e5, dof = 3)
```
Either operation saves the mean and covariance matrix of the sliced normal as an attribute of the sliced normal class. Re-fitting either a basic or a sliced normal will over-write the old distribution characteristics. These can then be used for unnormalised density estimation of expanded input data.

```sh
print(sn_fit.mu)
print(sn_fit.sigma)
print([*sn_fit.sn_phi(data)])
```
# Key Literature
Two papers represent the primary sources of this package:
Improving the Uncertainty Quantifcation of Sliced Normal Distributions by Scaling the Covariance Matrix, Colbert et al 2020
Density Estimation and Data-Enclosing Sets using Sliced-Normal Distributions, Crespo et al 2019

License
----

GPL-3.0

