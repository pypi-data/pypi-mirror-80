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
    'version': '0.1.6',
    'description': 'Upload Mydumper directories to S3.',
    'long_description': '# Mydumper To S3\n\n![Action](https://github.com/laixintao/mydumper2s3/workflows/Test/badge.svg)\n\nA tool that can upload mydumper dumped files to S3 bucket.\n\n![](./docs/mydumper2s3.gif)\n\nIt works even while mydumper is running, for mydumper opened files, mydumper2s3\nwill wait mydumper to close those files then upload. `--delete-after-upload`\noption enables you to backup your MySQL without dumping all of your data to\nlocal disk.\n\nIt works like this:\n\n```\n\n+-----------+\n|  mydumper |\n+-----+-----+\n      |\n      |\n      v\n+-----+------+  upload  +-------------+      +------+\n| local disk +----------> mydumper2s3 +------>  s3  |\n|            <----------+             |      |bucket|\n+------------+  delete  +-------------+      +------+\n                after\n                upload\n```\n\n## Install\n\n```\n   pip install mydumper2s3\n```\n\n## Usage\n\nCheck help:\n\n```\n$ mydumper2s3 --help\nUsage: mydumper2s3.py [OPTIONS]\n\n  mydumper2s3: upload mydumper dumped files to s3 bucket. It works even\n  while mydumper is running!\n\nOptions:\n  -a, --access_key TEXT           S3 access_key\n  -s, --secret_key TEXT           S3 secret_key\n  -d, --domain TEXT               S3 domain\n  -b, --bucket TEXT               S3 bucket, if not spcified, a new bucket\n                                  named by directory will be created\n\n  -l, --path TEXT\n  -i, --check-interval INTEGER\n  --ssl / --no-ssl\n  -t, --upload-thread INTEGER     thread numbers used to upload to s3\n  --delete-after-upload / --no-delete-after-upload\n                                  if set to True, files will be deleted in\n                                  local space after uploading.\n\n  --help                          Show this message and exit.\n```\n\n### Example\n\nUpload files to S3 (If mydumper is running, you can still using this command,\nmydumper2s3 will search mydumper process pid and watch files opended by\nmydumper.):\n\n```\n$ mydumper2s3 --domain 127.0.0.1:9000 \\\n             --bucket test1 \\\n             --path ~/Downloads/target \\\n             --access_key AKIAIOSFODNN7EXAMPLE \\\n             --secret_key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \\\n             --upload-thread=10\n138 files in directory,   0 dumping,   0 uploading,  138 uploaded.\n138 files successfully uploaded.\n```\n\nYou can check the backup with this command (available in your $PATH after install mydumper2s3):\n\n```\n$ verify-dump --domain 127.0.0.1:9000 \\\n              --bucket test1 \\\n              --path ~/Downloads/target \\\n              --access_key AKIAIOSFODNN7EXAMPLE \\\n              --secret_key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\nAll files are exist both on local and on S3, file name check pass...\nstart verifying file\'s md5, file count: 138.\n(1/138) verifying metadata...pass\n(2/138) verifying test-schema-create.sql...pass\n(3/138) verifying test.foo_event-schema.sql...pass\n(4/138) verifying test.foo_event_alarms-schema.sql...pass\n(5/138) verifying test.foo_list-schema.sql...pass\n…\n```\n\n# Development\n\n## Run monio locally\n\n```\ndocker run -p 9000:9000 \\\n  -e "MINIO_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE" \\\n  -e "MINIO_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \\\n  minio/minio server /data\n```\n',
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
