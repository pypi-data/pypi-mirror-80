#!/usr/bin/env python3

from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
name='testthisqawsedrftg',
version = '0.0.1',
description='test',
py_modules=['practice_package'],
package_dir={'':'src'},
long_description=long_description,
long_description_content_type="text/markdown",
install_requires=["pandas"],
extras_require={"dev":["pytest>=3.7",]},
url = "https://github.com/The-Data-Hound/tutorials", #sdist
author="Barry Guglielmo",
author_email="barryguglielmo@gmail.com"
)
