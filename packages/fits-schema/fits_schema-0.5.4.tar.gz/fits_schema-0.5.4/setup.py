# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fits_schema']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=3.0', 'numpy>=1.16,<2.0']

extras_require = \
{'travis': ['codecov>=2.0.22,<3.0.0']}

setup_kwargs = {
    'name': 'fits-schema',
    'version': '0.5.4',
    'description': '',
    'long_description': "# fits_schema [![Build Status](https://travis-ci.com/open-gamma-ray-astro/fits_schema.svg?branch=master)](https://travis-ci.com/open-gamma-ray-astro/fits_schema) [![codecov](https://codecov.io/gh/open-gamma-ray-astro/fits_schema/branch/master/graph/badge.svg)](https://codecov.io/gh/open-gamma-ray-astro/fits_schema) [![PyPI version](https://badge.fury.io/py/fits-schema.svg)](https://badge.fury.io/py/fits-schema)\n\n\n\nA python package to define and validate schemata for FITS files.\n\n\n```python\nfrom fits_schema.binary_table import BinaryTable, Double\nfrom fits_schema.header import HeaderSchema, HeaderCard\nimport astropy.units as u\nfrom astropy.io import fits\n\n\nclass Events(BinaryTable):\n    '''A Binary Table of Events'''\n    energy = Double(unit=u.TeV)\n    ra     = Double(unit=u.deg)\n    dec    = Double(unit=u.deg)\n\n    class __header__(HeaderSchema):\n        EXTNAME = HeaderCard(allowed_values='events')\n\n\nhdulist = fits.open('events.fits')\nEvents.validate_hdu(hdulist['events'])\n```\n",
    'author': 'Maximilian Nöthe',
    'author_email': 'maximilian.noethe@tu-dortmund.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
