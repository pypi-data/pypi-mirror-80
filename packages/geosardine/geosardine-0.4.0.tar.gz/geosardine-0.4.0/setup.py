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
    'version': '0.4.0',
    'description': 'Spatial operations extend fiona and rasterio',
    'long_description': '# Geo-Sardine\n\nCollection of spatial operation which i occasionally use \n\n## Setup\ninstall it with pip\n```pip install geosardine```\n\n## How to use it\n\n#### Drape and spatial join\n```python\nimport geosardine as dine\nimport rasterio\nimport fiona\n\nwith rasterio.open("/home/user/data.tif") as raster, fiona.open("/home/user/data.shp") as vector:\n    draped = dine.drape_geojson(vector, raster)\n    joined = dine.spatial_join(vector, raster) \n```\n#### IDW Interpolation\n```python\nimport numpy as np\nimport geosardine as dine\nxy = np.array([\n        [106.8358,  -6.585 ],\n        [106.6039,  -6.7226],\n        [106.7589,  -6.4053],\n        [106.9674,  -6.7092],\n        [106.7956,  -6.5988]\n])\nvalues = np.array([132., 127.,  37.,  90., 182.])\n\n"""\nif epsg not provided, it will assume that coordinate is in wgs84 geographic\nFind your epsg here https://epsg.io/\n"""\ninterpolated = dine.interpolate.idw(xy, values, spatial_res=(0.01,0.01), epsg=4326)\n\n# Save interpolation result to tiff\ninterpolated.save(\'idw.tif\')\n\n# The result array can be accessed like this\nprint(interpolated.array)\n"""\n[[ 88.63769859  86.24219616  83.60463194 ... 101.98185127 103.37001289\n  104.54621272]\n [ 90.12053232  87.79279317  85.22030848 ... 103.77118852 105.01425289\n  106.05302554]\n [ 91.82987695  89.60855271  87.14722258 ... 105.70090081 106.76928067\n  107.64635337]\n ...\n [127.21214817 127.33208302 127.53878268 ...  97.80436475  94.96247196\n   93.12113458]\n [127.11315081 127.18465002 127.33444124 ...  95.86455668  93.19212577\n   91.51135399]\n [127.0435062  127.0827023  127.19214624 ...  94.80175756  92.30685734\n   90.75707134]]\n"""\n\n\n\n```\n\n\n## Geosardine CLI\nYou can use it through terminal or command prompt by calling **dine**\n\n```\n$ dine --help\nUsage: dine [OPTIONS] COMMAND [ARGS]...\n\n  GeoSardine CLI\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  drape         Drape vector to raster to obtain height value\n  info          Get supported format\n  join-spatial  Join attribute by location\n  idw           Create raster with Inverse Distance Weighting interpolation\n```\n\n### License\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n',
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
