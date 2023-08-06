# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

class_base_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(class_base_dir, 'README.md'),'r',encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='simple-mysql',
    license='MIT',
    version="1.0.3",
    description='sql query for humans',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yaphp",
    author_email="yaphp960907@gmail.com",
    url="https://github.com/Yaphp/simple-mysql",
    download_url='https://github.com/Yaphp/simple-mysql.git',
    py_modules=["simple_mysql"],
    install_requires=[
        "mysql-connector"
    ],
    keywords=['help','simple','mysql','orm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False
)