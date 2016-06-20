#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

description = "A python library for calculating the delta score (Holland et al. 2002) and Q-Residual (Gray et al. 2010)"

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='phylogemetric',
    version='1.0.0',
    description=description,
    long_description=long_description,
    url='https://github.com/SimonGreenhill/phylogemetric',
    author='Simon J. Greenhill',
    author_email='simon@simon.net.nz',
    license='BSD',
    zip_safe=True,
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='phylogenetics delta-score q-residual',
    packages=find_packages(),
    package_data={'phylogemetric': ['data/*.nex']},
    install_requires=['python-nexus'],
    entry_points={
        'console_scripts': [
            'phylogemetric = phylogemetric.bin.phylogemetric:main'
        ],
    },
)
