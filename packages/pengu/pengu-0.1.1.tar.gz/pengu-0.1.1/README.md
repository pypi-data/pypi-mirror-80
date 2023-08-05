
# Pengu: a Library for Deep Learning in Computer Vision
Work In Progress！

![Test](https://github.com/peachanG/pengu/workflows/Test/badge.svg?branch=master)
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue?logo=python)
[![GitHub Issues](https://img.shields.io/github/issues/peachanG/pengu.svg?cacheSeconds=60&color=yellow)](https://github.com/peachanG/pengu/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/peachanG/pengu.svg?cacheSeconds=60&color=yellow)](https://github.com/peachanG/pengu/issues)
[![GitHub Release](https://img.shields.io/github/release/peachanG/pengu.svg?cacheSeconds=60&color=red)](https://github.com/peachanG/pengu/releases)

# command
```
$ mlflow server --backend-store-uri ./.mlflow_v2 --default-artifact-root s3://pengu-mlflow -p 5001
$ tensorboard --logdir=./logs
```
```
$ python -m pengu.main.crawler -config config/crawler.yaml -csv data/v2/crawler/crawler_result.csv -i data/v2/crawler/images -n 50
$ python -m pengu.main.preprocess_images -config config/preprocess.yaml -csv data/preprocessed
$ python -m pengu.main.train -config config/train.yaml -i data/train/inputs -m data/train/models -t ./logs
```