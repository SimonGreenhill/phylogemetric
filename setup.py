#!/usr/bin/env python
import os
import re
from setuptools import setup, find_packages
from codecs import open

description = "A python library for calculating the delta score (Holland et al. 2002) and Q-Residual (Gray et al. 2010)"

def get_version():
    VERSIONFILE = os.path.join('phylogemetric', '__init__.py')
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))



try:
    from pythran.dist import PythranExtension, PythranBuildExt
    setup_args = {
        'cmdclass': {"build_ext": PythranBuildExt},
        'ext_modules': [PythranExtension('phylogemetric.dist', sources = ['phylogemetric/dist.py'])],
    }
except ImportError:
    print("Not building Pythran extension")
    setup_args = {}

setup(
    name='phylogemetric',
    version=get_version(),
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
    install_requires=['pythran', 'numpy', 'python-nexus'],
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
    **setup_args
)
