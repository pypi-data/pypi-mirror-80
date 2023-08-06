# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geosardine', 'geosardine.interpolate']

package_data = \
{'': ['*']}

install_requires = \
['affine>=2.3.0,<3.0.0',
 'fiona',
 'gdal',
 'nptyping>=1.3.0,<2.0.0',
 'numba>=0.51.2,<0.52.0',
 'numpy>=1.18,<2.0',
 'rasterio',
 'shapely>=1.6.4,<2.0.0',
 'tqdm>=4.48.2,<5.0.0']

entry_points = \
{'console_scripts': ['dine = geosardine.__main__:main']}

setup_kwargs = {
    'name': 'geosardine',
    'version': '0.4.0a0',
    'description': 'Spatial operations extend fiona and rasterio',
    'long_description': '## Geo-Sardine\n\nCollection of spatial operation which i occasionally use \n\n### Setup\ninstall it with pip\n```pip install --pre geosardine```\n\n### How to use it\n```python\nimport geosardine as dine\nimport rasterio\nimport fiona\n\nwith rasterio.open("/home/user/data.tif") as raster, fiona.open("/home/user/data.shp") as vector:\n    draped = dine.drape_geojson(vector, raster)\n    joined = dine.spatial_join(vector, raster) \n```\n\n### Geosardine CLI\nYou can use it through terminal or command prompt by calling **dine**\n\n```\n$ dine --help\nUsage: dine [OPTIONS] COMMAND [ARGS]...\n\n  GeoSardine CLI\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  drape         Drape vector to raster to obtain height value\n  info          Get supported format\n  join-spatial  Join attribute by location\n```\n\n### License\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n',
    'author': 'Sahit Tuntas Sadono',
    'author_email': '26474008+sahitono@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sahitono/geosardine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
