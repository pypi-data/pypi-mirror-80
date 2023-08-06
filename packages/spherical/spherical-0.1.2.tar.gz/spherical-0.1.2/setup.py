# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spherical',
 'spherical.SWSH',
 'spherical.SWSH_grids',
 'spherical.SWSH_modes',
 'spherical.WignerD',
 'spherical.recursions']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.13,<2.0', 'quaternionic>=0.2.0,<0.3.0', 'scipy>=1.0,<2.0']

extras_require = \
{':implementation_name == "cpython"': ['numba>=0.50'],
 ':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'mkdocs:implementation_name == "cpython"': ['mkdocs>=1.1.2'],
 'mktheapidocs:implementation_name == "cpython"': ['mktheapidocs>=0.2'],
 'pymdown-extensions:implementation_name == "cpython"': ['pymdown-extensions>=8,<9']}

setup_kwargs = {
    'name': 'spherical',
    'version': '0.1.2',
    'description': 'Evaluate and transform D matrices, 3-j symbols, and (scalar or spin-weighted) spherical harmonics',
    'long_description': "[![Test Status](https://github.com/moble/spherical/workflows/tests/badge.svg)](https://github.com/moble/spherical/actions)\n[![Test Coverage](https://codecov.io/gh/moble/spherical/branch/master/graph/badge.svg)](https://codecov.io/gh/moble/spherical)\n[![Documentation Status](https://readthedocs.org/projects/spherical/badge/?version=main)](https://spherical.readthedocs.io/en/main/?badge=main)\n[![PyPI Version](https://img.shields.io/pypi/v/spherical?color=)](https://pypi.org/project/spherical/)\n[![Conda Version](https://img.shields.io/conda/vn/conda-forge/spherical.svg?color=)](https://anaconda.org/conda-forge/spherical)\n\n\n# Spherical Functions\n\nPython/numba package for evaluating and transforming Wigner's 𝔇 matrices,\nWigner's 3-j symbols, and spin-weighted (and scalar) spherical harmonics.\nThese functions are evaluated directly in terms of quaternions, as well as in\nthe more standard forms of spherical coordinates and Euler\nangles.<sup>[1](#1-euler-angles-are-awful)</sup>\n\nThe conventions for this package are described in detail on\n[this page](http://moble.github.io/spherical/).\n\n## Installation\n\nBecause this package is pure python code, installation is very simple.  In\nparticular, with a reasonably modern installation, you can just run a command\nlike\n\n```bash\nconda install -c conda-forge spherical\n```\n\nor\n\n```bash\npython -m pip install spherical\n```\n\nEither of these will download and install the package.\n\n\n## Usage\n\nFirst, we show a very simple example of usage with Euler angles, though it\nbreaks my heart to do so:<sup>[1](#euler-angles-are-awful)</sup>\n\n```python\n>>> import spherical as sf\n>>> alpha, beta, gamma = 0.1, 0.2, 0.3\n>>> ell,mp,m = 3,2,1\n>>> sf.Wigner_D_element(alpha, beta, gamma, ell, mp, m)\n\n```\n\nOf course, it's always better to use unit quaternions to describe rotations:\n\n```python\n>>> import numpy as np\n>>> import quaternionic\n>>> R = quaternionic.array(1,2,3,4).normalized\n>>> ell,mp,m = 3,2,1\n>>> sf.Wigner_D_element(R, ell, mp, m)\n\n```\n\nIf you need to calculate values of the 𝔇<sup>(ℓ)</sup> matrix elements for many\nvalues of (ℓ, m', m), it is more efficient to do so all at once.  The following\ncalculates all modes for ℓ from 2 to 8 (inclusive):\n\n```python\n>>> indices = np.array([[ell,mp,m] for ell in range(2,9)\n... for mp in range(-ell, ell+1) for m in range(-ell, ell+1)])\n>>> sf.Wigner_D_element(R, indices)\n\n```\n\nFinally, if you really need to put the pedal to the metal, and are willing to\nguarantee that the input arguments are correct, you can use a special hidden\nform of the function:\n\n```python\n>>> sf._Wigner_D_element(R.a, R.b, indices, elements)\n\n```\n\nHere, `R.a` and `R.b` are the two complex parts of the quaternion defined on\n[this page](http://moble.github.io/spherical/) (though the user need\nnot care about that).  The `indices` variable is assumed to be a\ntwo-dimensional array of integers, where the second dimension has size three,\nrepresenting the (ℓ, m', m) indices.  This avoids certain somewhat slower\npure-python operations involving argument checking, reshaping, etc.  The\n`elements` variable must be a one-dimensional array of complex numbers (can be\nuninitialized), which will be replaced with the corresponding values on return.\nAgain, however, there is no input dimension checking here, so if you give bad\ninputs, behavior could range from silently wrong to exceptions to segmentation\nfaults.  Caveat emptor.\n\n\n## Acknowledgments\n\nI very much appreciate Barry Wardell's help in sorting out the relationships\nbetween my conventions and those of other people and software packages\n(especially Mathematica's crazy conventions).\n\nThis code is, of course, hosted on github.  Because it is an open-source\nproject, the hosting is free, and all the wonderful features of github are\navailable, including free wiki space and web page hosting, pull requests, a\nnice interface to the git logs, etc.\n\nThe work of creating this code was supported in part by the Sherman Fairchild\nFoundation and by NSF Grants No. PHY-1306125 and AST-1333129.\n\n\n<br/>\n\n---\n\n###### <sup>1</sup> Euler angles are awful\n\nEuler angles are pretty much\n[the worst things ever](http://moble.github.io/spherical/#euler-angles)\nand it makes me feel bad even supporting them.  Quaternions are\nfaster, more accurate, basically free of singularities, more\nintuitive, and generally easier to understand.  You can work entirely\nwithout Euler angles (I certainly do).  You absolutely never need\nthem.  But if you're so old fashioned that you really can't give them\nup, they are fully supported.\n",
    'author': 'Michael Boyle',
    'author_email': 'michael.oliver.boyle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moble/spherical',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
