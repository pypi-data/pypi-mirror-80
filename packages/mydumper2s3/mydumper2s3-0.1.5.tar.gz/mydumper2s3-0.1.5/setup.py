# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mydumper2s3']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'minio>=6.0.0,<7.0.0', 'psutil>=5.7.2,<6.0.0']

entry_points = \
{'console_scripts': ['delete-bucket = mydumper2s3.delete_bucket:main',
                     'mydumper2s3 = mydumper2s3.mydumper2s3:main',
                     'verify-dump = mydumper2s3.verify_dump:main']}

setup_kwargs = {
    'name': 'mydumper2s3',
    'version': '0.1.5',
    'description': 'Upload Mydumper directories to S3.',
    'long_description': None,
    'author': 'laixintao',
    'author_email': 'laixintaoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
