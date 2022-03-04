import logging
import multiprocessing
from operator import mul
from fractions import Fraction
from itertools import combinations
from functools import reduce

from phylogemetric.dist import hammingdist


class Metric(object):
    """Base Metric Class"""
    
    def __init__(self, matrix=None, distance_function=hammingdist):
        self.log = logging.getLogger(__name__)
        self.matrix = {k: "".join(matrix[k]) for k in matrix}
        self.scores = {}
        self.taxa = {}
        self.cache = None
        self.qscores = None
        self.dist = hammingdist
        if self.matrix:
            self.taxa = dict([
                (k, i) for (i, k) in enumerate(self.matrix.keys(), 1)
            ])
            self._setup_qscores()
            
    def _setup_qscores(self):
        self.log.debug("_setup_qscores")
        self.qscores = dict(zip(self.matrix, [[0, 0] for _ in self.matrix]))
    
    def ncombinations(self, n):
        # http://stackoverflow.com/questions/3025162/
        return int(reduce(
            mul, (Fraction(len(self.taxa) - i, i + 1) for i in range(n)), 1
        ))
    
    def nquartets(self):
        """Calculates the number of quartets"""
        if not hasattr(self, "_nquartets"):
            self.log.debug("nquartets")
            self._nquartets = self.ncombinations(4)
        return self._nquartets
    
    def get_cachekey(self, taxon1, taxon2):
        """Returns a consistent cache key"""
        return tuple(sorted([self.taxa[taxon1], self.taxa[taxon2]]))
        
    def get_dist(self, taxon1, taxon2):
        """Gets distance between sequence1 and sequence2"""
        cachekey = self.get_cachekey(taxon1, taxon2)
        if taxon1 == taxon2:  # return 0 for identity matches
            return 0.0
        return self.cache[cachekey]

    def get_dist_parallel(self, key, sequence1, sequence2):
        """Gets distance between sequence1 and sequence2 -- for parallel functions."""
        return (key, self.dist(sequence1, sequence2))

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

        # go through quartet and calculate scores
        self.log.debug("score: calculate combinations")
        quartets = combinations(self.matrix, 4)

        if workers > 1:  # parallel process
            self.log.debug("score: starting work (%d workers)" % workers)

            with multiprocessing.Pool(processes=workers) as pool:
                #chunksize = int(self.nquartets() / workers) + 1
                chunksize = 65535
                self.log.debug("score: set chunksize to %d" % chunksize)

                self.log.debug("_setup_cache: set up cache (n=%d)" % self.ncombinations(2))
                jobs = [
                    (self.get_cachekey(t1, t2), self.matrix[t1], self.matrix[t2])
                    for (t1, t2) in
                    combinations(self.matrix, 2)
                ]
                self.cache = {k: d for k, d in pool.starmap(self.get_dist_parallel, jobs)}
                
                self.log.debug("score: _get_score_for_quartet (n=0 / %d = 0%%)" % self.nquartets())
                for i, (quartet, d) in enumerate(pool.imap_unordered(self._get_score_for_quartet, quartets, chunksize=chunksize), 1):
                    for taxon in quartet:
                        self.qscores[taxon][0] += d
                        self.qscores[taxon][1] += 1

                    if i % chunksize == 0:
                        self.log.debug("score: _get_score_for_quartet (n=%d / %d = %0.2f%%)" % (i, self.nquartets(), (i / self.nquartets()) * 100))

                self.log.debug("score: pool close")
                pool.close()
                self.log.debug("score: pool join")
                pool.join()

        else:  # single process
            self.log.debug("score: starting work (single process)")
            self.log.debug("_setup_cache: set up cache (n=%d)" % self.ncombinations(2))
            self.cache = {
                self.get_cachekey(t1, t2): self.dist(self.matrix[t1], self.matrix[t2])
                for t1, t2 in combinations(self.matrix, 2)
            }

            self.log.debug("score: _get_score_for_quartet (n=0 / %d = 0%%)" % self.nquartets())
            for i, quartet in enumerate(quartets, 1):
                _, d = self._get_score_for_quartet(quartet)
                for taxon in quartet:
                    self.qscores[taxon][0] += d
                    self.qscores[taxon][1] += 1
                if i % 1000 == 0:
                    self.log.debug("score: _get_score_for_quartet (n=%d / %d = %0.2f%%)" % (i, self.nquartets(), (i / self.nquartets()) * 100))

        return self._summarise_taxon_scores()

    def _summarise_taxon_scores(self):
        """Summarises quartet scores for each taxon"""
        self.log.debug("_summarise_taxon_scores")
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

