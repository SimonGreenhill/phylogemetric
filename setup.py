#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path

description = "A python library for calculating the delta score (Holland et al. 2002) and Q-Residual (Gray et al. 2010)"

setup(
    name='phylogemetric',
    version='1.1.0',
    description=description,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='phylogenetics delta-score q-residual',
    packages=find_packages(),
    package_data={'phylogemetric': ['data/*.nex']},
    install_requires=['python-nexus'],
    extras_require={
        'dev': ['wheel', 'twine'],
        'test': [
            'pytest>=5',
            'pytest-cov',
            'coverage>=4.2',
        ],
    },
    entry_points={
        'console_scripts': [
            'phylogemetric = phylogemetric.bin.phylogemetric:main'
        ],
    },
)
