# !/usr/bin/env python
# coding=utf-8
# /usr/bin/env/ python

"""
Author: AlibabaCloudRPA
Email:
Create time: 2020-04-26 10:01
IDE: PyCharm
desc: 
"""

import re
import setuptools

version = "1.0.0"
with open('rpa_openapi/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpa_openapi",
    version=version,
    author="AlibabaCloudRPA",
    author_email="",
    description="This is the SDK for AlibabaCloudRPA OpenAPI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.aliyun.com/product/codestore",
    install_requires=[
        'requests!=2.23.0',
        'pydantic!=1.5.1'
    ],
    packages=setuptools.find_packages(exclude="tests"),
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5"
    ),
    python_requires='>=3.5',
    exclude_package_data={'': ["rpa_openapi/test.py", "rpa_openapi/config.txt"]},
    license="GPL"
)
