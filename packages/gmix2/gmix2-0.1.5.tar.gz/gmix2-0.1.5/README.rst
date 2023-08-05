###################
Gaussian Mixtures 2
###################

.. image:: https://bitbucket.org/reidswanson/gmix2/raw/a8393abd4c09dc00ff23f33b6fa6645ac04bdf54/docs/source/images/single-density-plot.png
    :width: 100%
    :alt: Single Mixture Density Plot

********
Overview
********
`gmix2 <https://bitbucket.org/reidswanson/gmix2>`_ is a reimplementation of `gmix <https://bitbucket.org/reidswanson/gmix/src/master/>`_ that provides functions for working with univariate `Gaussian Mixture distributions <https://brilliant.org/wiki/gaussian-mixture-model/>`_ similar to `dmixnorm <https://rdrr.io/cran/KScorrect/man/dmixnorm.html>`_ of the `KScorrect <https://rdrr.io/cran/KScorrect/>`_ R package.
Unlike gmix, gmix2 does not include the code and recipes for implementing conditional density implementation using neural networks.
This reduces the number of external dependencies and complexity of the project considerably (e.g., no need for TensorFlow).
gmix2 is entirely written in C++ (and provides python bindings), so it is also slightly faster than gmix in most cases, and considerably faster in a a few cases [1]_.
It also provides a few bug fixes and the plotting function has been improved.

.. [1] Most of the functions in gmix were written using numpy so it was already relatively efficient.

************
Dependencies
************

C++
===

* A recent C++ compiler (gcc 9.3 is known to work)
* `CMake <https://cmake.org/>`_ >= 3.16
* `Boost <https://www.boost.org/>`_ (>= 1.73.0) with python support
* Python development libraries (for Python.h)
* `Eigen3 <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_

Python
======
Only python3 is supported.

**Required**

* `numpy <https://numpy.org/install/>`_

**Needed For Plotting**

* `scipy <https://www.scipy.org/install.html>`_
* `pandas <https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html>`_
* `plotnine <https://plotnine.readthedocs.io/en/stable/installation.html>`_
* `pycairo <https://pycairo.readthedocs.io/en/latest/>`_ Matplotlib may complain if this is not installed separately.
* `PyQt5 <https://pypi.org/project/PyQt5/>`_ You may need to install a rending package for interactive plots.

*******
Install
*******
Note, this package is only available as a source distribution.
So, you must have a working C++ compiler and the required libraries listed above installed in a location visible to CMake.

From Git:

.. code-block:: bash

   >pip install git+https://bitbucket.org/reidswanson/gmix2.git

Or on PyPI:

.. code-block:: bash

   >pip install gmix2

***********
C++ Library
***********
The base C++ code is also available as a `header only library <https://bitbucket.org/reidswanson/gmix2/src/master/include/gmix2/gmix.hpp>`_, but no additional documentation is provided for using it.

*************
Documentation
*************

The full documentation is available on `Read the Docs <https://gmix2.readthedocs.io/en/latest/>`_.

*******
License
*******
Any file without a specific copyright notification is released using the Apache v2 License by me (Reid Swanson).
See the `LICENSE <https://bitbucket.org/reidswanson/gmix2/src/master/LICENSE>`_ file for more details.
Some code has been copied or adapted from the web (e.g., StackOverflow) that does not have clear license indications.
In those cases the code is flagged with comments and links to where the code was found.
