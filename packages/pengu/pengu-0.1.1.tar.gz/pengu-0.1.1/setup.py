# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pengu',
 'pengu.data',
 'pengu.dataset',
 'pengu.main',
 'pengu.model',
 'pengu.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.38,<2.0.0',
 'hydra>=2.5,<3.0',
 'icrawler>=0.6.3,<0.7.0',
 'imagehash>=4.1.0,<5.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'mlflow>=1.10.0,<2.0.0',
 'mypy>=0.782,<0.783',
 'opencv-python==4.2.0.34',
 'scikit-learn>=0.23.2,<0.24.0',
 'tensorboard_plugin_profile>=2.3.0,<3.0.0',
 'tensorflow==2.3.0']

setup_kwargs = {
    'name': 'pengu',
    'version': '0.1.1',
    'description': 'WIP',
    'long_description': '\n# Pengu: a Library for Deep Learning in Computer Vision\nWork In Progress！\n\n![Test](https://github.com/peachanG/pengu/workflows/Test/badge.svg?branch=master)\n![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue?logo=python)\n[![GitHub Issues](https://img.shields.io/github/issues/peachanG/pengu.svg?cacheSeconds=60&color=yellow)](https://github.com/peachanG/pengu/issues)\n[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/peachanG/pengu.svg?cacheSeconds=60&color=yellow)](https://github.com/peachanG/pengu/issues)\n[![GitHub Release](https://img.shields.io/github/release/peachanG/pengu.svg?cacheSeconds=60&color=red)](https://github.com/peachanG/pengu/releases)\n\n# command\n```\n$ mlflow server --backend-store-uri ./.mlflow_v2 --default-artifact-root s3://pengu-mlflow -p 5001\n$ tensorboard --logdir=./logs\n```\n```\n$ python -m pengu.main.crawler -config config/crawler.yaml -csv data/v2/crawler/crawler_result.csv -i data/v2/crawler/images -n 50\n$ python -m pengu.main.preprocess_images -config config/preprocess.yaml -csv data/preprocessed\n$ python -m pengu.main.train -config config/train.yaml -i data/train/inputs -m data/train/models -t ./logs\n```',
    'author': 'peachanG',
    'author_email': 'kenkman0427@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/peachanG',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.6,<4.0.0',
}


setup(**setup_kwargs)
