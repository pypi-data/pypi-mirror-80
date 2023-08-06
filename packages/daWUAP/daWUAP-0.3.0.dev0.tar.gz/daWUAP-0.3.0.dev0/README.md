daWUAP - data assimilation Water Use and Agricultural Productivity Model
========================================================================

The data assimilation Water Use and Agricultural Productivity model (daWUAP) is a hydro-economic model that couples an economic model of agricultural production calibrated using positive mathematical programming (PMP) and a semidistributed rainfall-runoff-routing model that simulates water available to producers.

**Features:**

* Calibration of economic component can use standard the mathematical programming method or a new recursive stochastic filter.
* Stochastic calibration permits to obtain simulation results of agricultural outputs (land and water allocation, etc) as probability distributions that reflect the quality of the calibration.
* Recursive stochastic filter permits calibration of economic model with noisy but frequent remote sensing observations of agricultural activity.
* Model permits to trace the effect of producer choices on the hydrologic system and on other users.

[**Check out the project website.**](https://www.umt.edu/hydro-econ-ag/dawuap/)

Contributions and comments are welcome [on our Bitbucket repository](https://bitbucket.org/umthydromodeling/dawuap.git).


Use and Citation
----------------

A DOI is forthcoming. Users and encouraged to cite the peer-reviewed journal article(s) that describe the model in technical detail.

Maneta, M. P., J. S. Kimball, M. He, N. L. Silverman, B. C. Chaffin, B. Maxwell, S. Ewing, K. Cobourn, and X. Ji. 2020. [**A satellite-driven hydro-economic model to support agricultural water resources management.**](https://www.sciencedirect.com/science/article/abs/pii/S1364815220308938) *Environmental Modelling & Software.*


Dependencies
============

Please note that daWUAP requires:

* Python >= 3.7
* `GDAL support <https://gdal.org/>` (version 1.13 or higher)
* `HDF5 support <https://www.hdfgroup.org/solutions/hdf5/>`


Installation
============

There are multiple ways to install the `dawuap` Python package.


Installation from Source
------------------------

It is recommended that you install the package in a virtual environment, either with `virtualenv` or `conda`. In general:

1. Download or clone repository;
2. Change your working directory (`cd`) to the repository directory;
3. `python setup.py install`

**Or, with `pip`:**

1. Download or clone repository;
2. Change your working directory (`cd`) to the repository directory;
3. `pip install .`

**Or, for installation using `conda`:**

1. Download or clone repository;
2. Change your working directory (`cd`) to the repository directory;
3. Create a new environment: `conda create --name dawuap python=3`
4. Activate the environment: `source activate dawuap`
5. `conda install .`


Installation from Source (for Developers)
-----------------------------------------

If you plan to make changes to the source code, it's most convenient to install daWUAP in "editable" mode.

Using `pip` (preferably in a virtual environment), from the top-level directory of the repository:

``
pip install -e .
``

If you use `conda` to create and manage your virtual environments, be sure to `conda install pip` before running the above.


Testing
-------

```
python daWUAP/tests/tests.py
```


Documentation
=============

The documentation available as of the date of this release is included in HTML format in the Documentation directory of the repository. `The most up-to-date documentation can be found here. <https://dawuap.readthedocs.io/en/latest/>`

**Demos of the core functionality of `daWUAP` are available as [interactive Jupyter Notebooks on Bitbucket.](https://bitbucket.org/umthydromodeling/dawuap-demo/src/master/)**


Input Vector File Schema
------------------------

All input vector datasets need to have a standard schema. For the basins attributes (or "properties"):

``
'FROM_NODE', 'TO_NODE', 'SUBBASIN', 'SUBBASINR', 'AREAC', 'hbv_ck0', 'hbv_ck1', 'hbv_ck2', 'hbv_hl1', 'hbv_perc', 'hbv_pbase'
``

For the river or network attributes:

``
'ARCID', 'FROM_NODE', 'TO_NODE', 'SUBBASIN', 'SUBBASINR', 'AREAC', 'k', 'es'
``

In particular, "SHAPE_AREA" (if present), "ARCID", "SUBBASIN" must be in all upper-case. Currently, "ARCID" and "SUBBASIN" are the unique identifiers for stream/ network segments and subsheds, respectively.


Economic Model Parameters
-------------------------

The economic model is described in its entirety in Maneta et al. (2020). The individual model parameters defined in a Farm data dictionary are:

- `deltas` are the return-to-scale parameters, describing the factor by which crop production is increased for a proportional increase in inputs.
- `betas` correspond to the share factors in a constant elasticity of substitution (CES) model; they can be interpreted as the relative importance of an input factor (e.g., water vs. land) towards crop production.
- `lambdas_land`, the Lagrange multipliers associated with resource constraints; they can be interpreted as the shadow prices of the limiting resources (the additional revenue farmers would receive per additional unit of crop, could they produce it). Another interpretation of `lambdas_land` is "a measure of the value that farmers may receive from increasing the acreage of [a crop]" (Maneta and Howitt, 2014), or the marginal value of production.
- `first_stage_lambda`, also a Lagrange multiplier, "this parameter represents the shadow value for the total amount of land available for crop production" (Maneta et al. 2020).
- `sigmas` is the (constant) elasticity of substitution parameter.
- `mus` is an array of productivity parameters for the CES model.


Licensing
=========

  Please see the file called LICENSE.txt.


Bugs & Contribution
===================

[Please use Bitbucket](https://bitbucket.org/umthydromodeling/dawuap/issues) to report any bugs, to ask questions, or to submit pull requests.
