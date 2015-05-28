#!/usr/bin/env python
#coding=utf-8
"""Calculates a network metric"""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2015 Simon J. Greenhill'
__license__ = 'New-style BSD'
__package__ = 'phylogemetric'
import os

try:
    from nexus import NexusReader
except ImportError:
    raise ImportError("Please install python-nexus")

from phylogemetric.delta import DeltaScoreMetric
from phylogemetric.qresidual import QResidualMetric

def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(
        description='Calculates a phylogenetic network metric from a nexus file'
    )
    parser.add_argument("method", help="Method [delta/qresidual]")
    parser.add_argument("filename", help="nexusfile")
    args = parser.parse_args()
    
    if not os.path.isfile(args.filename):
        raise IOError("File %s does not exist" % args.filename)
    nex = NexusReader(args.filename)
    
    if args.method in ('q', 'qresidual'):
        metric = QResidualMetric(nex.data.matrix)
    elif args.method in ('d', 'delta'):
        metric = DeltaScoreMetric(nex.data.matrix)
    else:
        raise SystemExit(
            "Unknown method %s. Please choose either 'delta' or 'q'"
            % args.method
        )
    
    metric.score()
    metric.pprint()
    

if __name__ == '__main__':
    main()