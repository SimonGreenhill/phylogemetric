from operator import mul
from fractions import Fraction
from itertools import combinations
from functools import reduce


class Metric(object):
    """Base Metric Class"""
    def __init__(self, matrix=None):
        self.matrix = matrix
        self.cache = {}
        self.scores = {}
        self.qscores = None
        if self.matrix:
            self.taxa = dict([
                (k, i) for (i, k) in enumerate(self.matrix.keys(), 1)
            ])
            self._setup_qscores()
            
    def _setup_qscores(self):
        self.qscores = dict(zip(self.matrix, [[0, 0] for _ in self.matrix]))
    
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
            self._nquartets = int(reduce(
                mul, (Fraction(len(self.taxa) - i, i + 1) for i in range(4)), 1
            ))
        return self._nquartets
    
    def get_dist(self, taxon1, taxon2, sequence1, sequence2):
        """
        Gets distance between sequence1 and sequence2
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
    
    def _get_score_for_quartet(self, quartet):
        """
        Calculates score for given quartet
        
        NOTE: needs to be overridden in subclass. Here it
        just returns 0.0
        """
        return 0.0
    
    def score(self):
        """Returns a dictionary of metric scores"""
        if not self.qscores:
            self._setup_qscores()
        # go through quartet and calculate scores
        for quartet in combinations(self.matrix, 4):
            score = self._get_score_for_quartet(quartet)
            for taxon in quartet:
                self.qscores[taxon][0] += score
                self.qscores[taxon][1] += 1
        return self._summarise_taxon_scores()
    
    def _summarise_taxon_scores(self):
        """Summarises quartet scores for each taxon"""
        self.scores = {}
        for taxon in self.qscores:
            self.scores[taxon] = self.qscores[taxon][0] / self.qscores[taxon][1]
        return self.scores
    
    def pprint(self):
        max_len = max([len(_) for _ in self.matrix])
        for taxon in sorted(self.scores):
            print("%s\t%0.4f" % (taxon.ljust(max_len + 1), self.scores[taxon]))

