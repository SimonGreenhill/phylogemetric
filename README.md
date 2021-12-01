# phylogemetric

A python library for calculating delta score ([Holland et al. 2002](http://mbe.oxfordjournals.org/content/19/12/2051.full)) and Q-Residual ([Gray et al. 2010](http://dx.doi.org/10.1098/rstb.2010.0162)) for phylogenetic data.

[![Build Status](https://travis-ci.org/SimonGreenhill/phylogemetric.svg?branch=master)](https://travis-ci.org/SimonGreenhill/phylogemetric)
[![Coverage Status](https://coveralls.io/repos/SimonGreenhill/phylogemetric/badge.svg?branch=master&service=github)](https://coveralls.io/github/SimonGreenhill/phylogemetric?branch=master)
[![DOI](https://zenodo.org/badge/22704/SimonGreenhill/phylogemetric.svg)](https://zenodo.org/badge/latestdoi/22704/SimonGreenhill/phylogemetric)
[![License](https://img.shields.io/pypi/l/phylogemetric.svg)](https://github.com/SimonGreenhill/phylogemetric/blob/master/LICENSE)
[![JOSS](http://joss.theoj.org/papers/10.21105/joss.00028/status.svg)](http://joss.theoj.org/papers/10.21105/joss.00028)

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

### Speeding things up by using multiple processes.

You can tell phylogemetric to use multiple cores with the `-w/--workers` argument:

```shell
> phylogemetric -w 4 qresidual example.nex
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
m.score(workers=4) # with multiple processes.


# pretty prints the metric scores:
m.pprint()

```

## Requirements:

* python-nexus >= 1.1

## Performance Notes:

Currently _phylogemetric_ is implemented in python, and the Delta/Q-Residual algorithms are O(n). This means
that performance is not optimal, and it may take a while to calculate these metrics for datasets with more than
100 taxa or so. To help speed this up, use the multiple processes argument `-w/--workers` at the command line or by passing `workers=n` to the `score` function.

I hope to improve performance in the near future, but in the meantime, if this is an issue for you then try 
using the implementations available in [SplitsTree](http://splitstree.org).

## Citation:

If you use _phylogemetric_, please cite: 

```
Greenhill, SJ. 2016. Phylogemetric: A Python library for calculating phylogenetic network metrics. Journal of Open Source Software.
http://dx.doi.org/10.21105/joss.00028
```

## Changelog:

* 1.1.0:
- Added support for multiple processes.
- Removed python 2 support.

## Acknowledgements:

* Thanks to David Bryant for clarifying the Q-Residual code.
* Thanks to [Kristian Rother](https://github.com/krother) for code quality suggestions.
