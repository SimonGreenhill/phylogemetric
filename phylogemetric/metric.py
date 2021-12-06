import multiprocessing
from operator import mul
from fractions import Fraction
from itertools import combinations
from functools import reduce

from phylogemetric.dist import hammingdist


class Metric(object):
    """Base Metric Class"""
    
    def __init__(self, matrix=None, distance_function=hammingdist):
        self.matrix = matrix
        self.cache = {}
        self.scores = {}
        self.taxa = {}
        self.qscores = None
        self.dist = hammingdist
        if self.matrix:
            self.taxa = dict([
                (k, i) for (i, k) in enumerate(self.matrix.keys(), 1)
            ])
            self._setup_qscores()
            
    def _setup_qscores(self):
        self.qscores = dict(zip(self.matrix, [[0, 0] for _ in self.matrix]))
    
    def nquartets(self):
        """Calculates the number of quartets"""
        # http://stackoverflow.com/questions/3025162/statistics-combinations-in-python
        if not hasattr(self, "_nquartets"):
            self._nquartets = int(reduce(
                mul, (Fraction(len(self.taxa) - i, i + 1) for i in range(4)), 1
            ))
        return self._nquartets
    
    def get_cachekey(self, taxon1, taxon2):
        """Returns a consistent cache key"""
        return tuple(sorted([self.taxa[taxon1], self.taxa[taxon2]]))
        
    def get_dist(self, taxon1, taxon2, sequence1, sequence2):
        """Gets distance between sequence1 and sequence2"""
        cachekey = self.get_cachekey(taxon1, taxon2)
        # return 0 for identity matches
        if taxon1 == taxon2:
            return 0.0
        if cachekey not in self.cache:
            self.cache[cachekey] = self.dist("".join(sequence1), "".join(sequence2))
        return self.cache[cachekey]
    
    def _get_score_for_quartet(self, quartet):
        """
        Calculates score for given quartet
        
        NOTE: needs to be overridden in subclass. Here it just returns 0.0
        """
        return (quartet, 0.0)
        
    def score(self, workers=1):
        """Returns a dictionary of metric scores"""
        if not self.qscores:
            self._setup_qscores()
        
        # prefill cache. This should speed up calculation as all get_dist calls
        # will then be just cache hits, and it means we don't need to hook in
        # a multiprocessing manager on self.cache (which seems to cause the
        # analysis to stall, presumably because each process then has to wait
        # for locks).
        for t1, t2 in combinations(self.matrix, 2):
           self.get_dist(t1, t2, self.matrix[t1], self.matrix[t2])

        # go through quartet and calculate scores
        combs = combinations(self.matrix, 4)
        if workers > 1:  # parallel process
            with multiprocessing.Pool(processes=workers) as pool:
                scores = pool.map(self._get_score_for_quartet, combs)
                pool.close()
                pool.join()
        
        else:  # single process
            scores = [self._get_score_for_quartet(c) for c in combs]

        for quartet, d in scores:
            for taxon in quartet:
                self.qscores[taxon][0] += d
                self.qscores[taxon][1] += 1
        
        return self._summarise_taxon_scores()
    
    def _summarise_taxon_scores(self):
        """Summarises quartet scores for each taxon"""
        self.scores = {}
        for taxon in self.qscores:
            self.scores[taxon] = (
                self.qscores[taxon][0] / self.qscores[taxon][1]
            )
        return self.scores
    
    def pprint(self):
        if not self.scores:
            raise ValueError("Scores not calculated yet. Run .score()")
        max_len = max([len(_) for _ in self.matrix])
        for taxon in sorted(self.scores):
            print("%s\t%f" % (taxon.ljust(max_len + 1), self.scores[taxon]))

