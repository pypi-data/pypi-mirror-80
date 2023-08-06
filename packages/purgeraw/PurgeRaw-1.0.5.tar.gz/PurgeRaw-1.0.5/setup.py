# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['purgeraw']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'toolz>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['praw = purgeraw.main:main']}

setup_kwargs = {
    'name': 'purgeraw',
    'version': '1.0.5',
    'description': 'Utility to remove unprocessed RAW files from a folder keeping only RAW files that yielded results',
    'long_description': "**Overview**\n\nFor photographers keeping every raw file captured can use a lot of space.  \nThis utility allows a photographer to purge any unused raw files leaving \nonly the processed files with their associated raws.\n\nThe app trawls the input directory for raw and processed images.\nWhere it finds a raw image with a numeric index that can't be\nfound in the processed images it is marked for removal.\n\nAny sequence of 3 to 6 (inc) numbers in the image filename is deemed as its index which is used\nto associate processed and raw images.\n\nProcessed images may also have a filename format with a range of indexes, e.g. IMG_01234-1236.jpg\nThis processed file would be associated with IMG_01234.cr3, IMG_01235.cr3 and IMG_01236.cr3 raw images\nthus ensuring they are not deleted. This is useful for HDR or panoramic processed images.\n\nFor example, given the folder1 below:\n\n<pre>\nfolder1/\n  IMG_1000.cr3\n  IMG_1001.cr3\n  IMG_1002.cr3\n  IMG_1003.cr3\n  IMG_1004.cr3\n  Processed/\n    IMG_1000.jpg\n    IMG_1002-1003.jpg\n</pre>\n\nRunning `praw folder1 -d` would remove the IMG_1001.cr3 and \nIMG_1004.cr3 raw images as they don't have associated processed images.\n\nThe resulting directory would be left as:\n<pre>\nfolder1/\n  IMG_1000.cr3\n  IMG_1002.cr3\n  IMG_1003.cr3\n  Processed/\n    IMG_1000.jpg\n    IMG_1002-1003.jpg\n</pre>\n\nTo install run `pip install purgeraw`\n",
    'author': 'Andy Phelps',
    'author_email': 'andrew.m.phelps@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andyphelps/purgeraw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
