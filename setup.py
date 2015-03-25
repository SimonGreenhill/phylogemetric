# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='phylogemetric',
    version='0.9',
    description='A python library for calculating the delta score (Holland et al. 2002) and Q-Residual (Gray et al. 2010)',
    long_description=long_description,
    url='https://github.com/SimonGreenhill/phylogemetric',
    author='Simon J. Greenhill',
    author_email='simon@simon.net.nz',
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
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
    ],
    keywords='phylogenetics delta-score q-residual',
    packages=find_packages('phylogemetric', exclude=['tests*']),
    install_requires=['python-nexus'],
    scripts=['phylogemetric/bin/phylogemetric.py'],
    test_suite="tests",
)