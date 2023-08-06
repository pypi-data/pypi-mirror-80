# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_aws']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.26,<2.0.0',
 'fastparquet>=0.3.3,<0.4.0',
 'pandas>=1.0.3,<2.0.0',
 'pyarrow>=0.16.0,<0.17.0',
 'xlrd>=1.2.0,<2.0.0',
 'xlsxwriter>=1.2.8,<2.0.0']

setup_kwargs = {
    'name': 'pandas-aws',
    'version': '0.1.1',
    'description': '',
    'long_description': "[![Build Status](https://travis-ci.com/FlorentPajot/pandas-aws.svg?branch=master)](https://travis-ci.com/FlorentPajot/pandas-aws) [![codecov](https://codecov.io/gh/FlorentPajot/pandas-aws/branch/master/graph/badge.svg)](https://codecov.io/gh/FlorentPajot/pandas-aws)\n\n# Pandas AWS - AWS use made easy for data scientists\n\nPandas AWS makes it super easy to use a pandas.DataFrame along with AWS services.\n\n```\n# Example : get a DataFrame from multiple CSV files in S3\n\nfrom pandas_aws import get_client, get_df_from_keys\n\nMY_BUCKET= 'pandas-aws-bucket'\n\ns3 = get_client('s3')\n\ndf = get_df_from_keys(s3, MY_BUCKET, prefix='my-folder', suffix='.csv')\n```\n\n# Installing pandas-aws\n\n## Pip installation\n\nYou can use pip to download the package\n\n`pip install pandas-aws`\n\n# Contributing to pandas-aws\n\n## Git clone\n\nWe use the `develop` brand as the release branch, thus `git clone` the repository and `git checkout develop` in order to get the latest version in development.\n\n```\ngit clone git@github.com:FlorentPajot/pandas-aws.git\n```\n\n## Preparing your environment\n\nPandas AWS uses `poetry` to manage dependencies. Thus, `poetry` is required:\n\n`curl -SSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`\n\nCreate a separate Python environment, for example using `pyenv`:\n\n```\npyenv virtualenv pandas-aws\npyenv activate pandas-aws\n```\nThen install dependencies with poetry after your `git clone` from the project repository:\n\n`poetry install`\n\n## Guidelines\n\nTodo\n",
    'author': 'FlorentPajot',
    'author_email': 'pro.florent.pajot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FlorentPajot/pandas-aws',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
