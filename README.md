# phylogemetric

A python library for calculating delta score (Holland et al. 2002) and Q-Residual (Gray et al. 2010) for phylogenetic data.

[![Build Status](https://travis-ci.org/SimonGreenhill/phylogemetric.svg?branch=master)](https://travis-ci.org/SimonGreenhill/phylogemetric)
[![Coverage Status](https://coveralls.io/repos/SimonGreenhill/phylogemetric/badge.svg?branch=master&service=github)](https://coveralls.io/github/SimonGreenhill/phylogemetric?branch=master)
[![DOI](https://zenodo.org/badge/22704/SimonGreenhill/phylogemetric.svg)](https://zenodo.org/badge/latestdoi/22704/SimonGreenhill/phylogemetric)

## Installation:

Installation is only a pip install away:

```shell
pip install phylogemetric
```

## Usage: Command line

Basic usage: 

```shell
> phylogemetric

usage: phylogemetric [-h] method filename
```

Calculate delta score for filename example.nex:

```shell
> phylogemetric delta example.nex

taxon1              0.2453
taxon2              0.2404
taxon3              0.2954
...
```

Calculate qresidual score for filename example.nex:

```shell
> phylogemetric qresidual example.nex

taxon1              0.0030
taxon2              0.0037
taxon3              0.0063
...
```

Note: to save the results to a file use shell piping e.g.:

```shell
> phylogemetric qresidual example.nex > qresidual.txt
```


## Usage: Library

Calculate scores:

```python
from nexus import NexusReader
from phylogemetric import DeltaScoreMetric
from phylogemetric import QResidualMetric

# load data from a nexus file:
nex = NexusReader("filename.nex")
qres = QResidualMetric(nex.data.matrix)

# Or construct a data matrix directly: 

matrix = {
    'A': [
        '1', '1', '1', '1', '0', '0', '1', '1', '1', '0', '1', '1',
        '1', '1', '0', '0', '1', '1', '1', '0'
    ],
    'B': [
        '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1',
        '1', '1', '1', '0', '0', '1', '1', '1'
    ],
    'C': [
        '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '0',
        '0', '0', '0', '1', '0', '1', '1', '1'
    ],
    'D': [
        '1', '0', '0', '0', '0', '1', '0', '1', '1', '1', '1', '0',
        '0', '0', '0', '1', '0', '1', '1', '1'
    ],
    'E': [
        '1', '0', '0', '0', '0', '1', '0', '1', '0', '1', '1', '0',
        '0', '0', '0', '1', '1', '1', '1', '1'
    ],
}

delta = DeltaScoreMetric(matrix)
```

Class Methods:

```python

m = DeltaScoreMetric(matrix)

# calculates the number of quartets in the data:
m.nquartets()

# returns the distance between two sequences:
m.dist(['1', '1', '0'], ['0', '1', '0'])

# gets a dictionary of metric scores:
m.score()

# pretty prints the metric scores:
m.pprint()

```

## Requirements:

* python-nexus >= 1.1

## Acknowledgements:

* Thanks to David Bryant for clarifying the Q-Residual code.
