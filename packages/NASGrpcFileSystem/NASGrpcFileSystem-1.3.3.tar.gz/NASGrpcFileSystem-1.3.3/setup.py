# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='NASGrpcFileSystem',
    version='1.3.3',
    description=('A python file handler use Grpc client. It used to handle ctec file work, and include: upload and download file from remote, modify file name, copy and move file.'),
    author='Kepner Wu',
    author_email='kepner_wu@hotmail.com',
    license='MIT',
    packages=find_packages(),
    platforms=['all'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='CTEC NAS file Grpc system includes create file, get file describe, modify, copy and move file',
    install_requires=[
        'future==0.18.2',
        'grpcio==1.30.0',
        'werkzeug==0.15.4',
        'protobuf==3.12.2'
    ],
)
