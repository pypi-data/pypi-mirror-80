# -*- coding: utf-8 -*-
# @Time    : 2020/9/22 下午5:02
# @Author  : jinzening
# @File    : setup.py
# @Software: PyCharm
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example12121", # Replace with your own username
    version="0.0.3",
    author="jinzening",
    author_email="zening918@163.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
