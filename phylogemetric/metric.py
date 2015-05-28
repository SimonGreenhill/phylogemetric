from operator import mul
from fractions import Fraction
from functools import reduce

class Metric(object):
    """Base Metric Class"""
    def __init__(self, matrix=None):
        self.matrix = matrix
        self.cache = {}
        self.scores = {}
        if self.matrix:
            self.taxa = dict([(k,i) for (i,k) in enumerate(self.matrix.keys(), 1)])
    
    def dist(self, a, b):
        """
        Calculates the Hamming Distance between two sequences
        
        Returns a value in the range of [1.0-0.0]
        """
        same, compared = 0.0, 0.0
        for i in range(0, len(a)):
            if a[i] in ('?', '-') or b[i] in ('?', '-'):
                continue
            elif a[i] == b[i]:
                same += 1.0
            compared += 1.0
        return 1.0 - (same / compared)
    
    def nquartets(self):
        """Caclulates the number of quartets"""
        # http://stackoverflow.com/questions/3025162/statistics-combinations-in-python
        if not hasattr(self, "_nquartets"):
            self._nquartets = int(reduce(mul, (Fraction(len(self.taxa) - i, i + 1) for i in range(4)), 1))
        return self._nquartets
    
    def get_dist(self, taxon1, taxon2, sequence1, sequence2):
        """
        Gets distance between sequence1 and sequence2
        
        Handles caching of scores too.
        """
        cachekey = tuple(sorted([self.taxa[taxon1], self.taxa[taxon2]]))
        # return 0 for identity matches
        if taxon1 == taxon2:
            return 0.0
        # check cache
        elif cachekey in self.cache:
            return self.cache[cachekey]
        else:
            dist = self.dist(sequence1, sequence2)
            self.cache[cachekey] = dist
            return dist
    
    def pprint(self):
        max_len = max([len(_) for _ in self.matrix])
        for taxon in sorted(self.scores):
            print("%s\t%0.4f" % (taxon.ljust(max_len + 1), self.scores[taxon]))

