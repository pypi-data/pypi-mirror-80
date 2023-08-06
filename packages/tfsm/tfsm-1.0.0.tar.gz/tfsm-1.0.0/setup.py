# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
import setuptools


################################################
#################### Setup #####################
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tfsm',  
    version='1.0.0',
    author="Edward Y. Liu",
    author_email="edwardy.liu@mail.utoronto.ca",
    description="A Trader Finite State Machine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edwardyliu/Ars",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},  # Optional
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6.8',
    install_requires=['dataclasses', 'numpy', 'pytz', 'tulipy'],
)
