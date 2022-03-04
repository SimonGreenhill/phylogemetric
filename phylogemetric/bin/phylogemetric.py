#!/usr/bin/env python
#coding=utf-8
"""Calculates a network metric"""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2015-2016 Simon J. Greenhill'
__license__ = 'New-style BSD'
__package__ = 'phylogemetric'

import os
import sys
import logging
import argparse

try:
    from nexus import NexusReader
except ImportError:  # pragma: no cover
    raise ImportError("Please install python-nexus")

from . import __version__
from . import DeltaScoreMetric
from . import QResidualMetric


def parse_args(*args):
    """
    Parses command line arguments
    
    Returns a tuple of (metric, filename)
    """
    descr = 'Calculates a phylogenetic network metric from a nexus file'
    parser = argparse.ArgumentParser(prog="phylogemetric", description=descr)
    parser.add_argument("method", help="Method [delta/qresidual]")
    parser.add_argument("filename", help="nexusfile")
    parser.add_argument(
        '-w', "--workers",
        action='store', type=int, default=1,
        help="set number of workers"
    )
    parser.add_argument(
        "-log", "--loglevel",
        default='warning',
        help="Provide logging level. Example --loglevel debug, default=warning"
    )
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args(args)

    logging.basicConfig(level=args.loglevel.upper())
    logging.info("Logging initialised to %s" % args.loglevel.upper())
    
    if not os.path.isfile(args.filename):
        raise IOError("File %s does not exist" % args.filename)
    
    if args.method in ('q', 'qres', 'qresidual'):
        metric = QResidualMetric
    elif args.method in ('d', 'delta'):
        metric = DeltaScoreMetric
    else:
        raise SystemExit(
            "Unknown method %s. Please choose either 'delta' or 'q'"
            % args.method
        )
    return (metric, args.filename, args.workers)
    

def main(args=None):
    if args is None:  # pragma: no cover
        args = sys.argv[1:]
    metric, filename, workers = parse_args(*args)
    nex = NexusReader(filename)
    M = metric(nex.data.matrix)
    M.score(workers=workers)
    M.pprint()

