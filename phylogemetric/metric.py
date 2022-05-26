import logging
import multiprocessing
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Sequence, Union
from typing import cast
from operator import mul
from fractions import Fraction
from itertools import combinations
from functools import reduce

from phylogemetric.dist import hammingdist

# type aliases
Matrix = Dict[str, Sequence[str]]
QuartetType = Tuple[str, str, str, str]
NumericType = Union[float, int]

class Metric(object):
    """Base Metric Class"""
    
    def __init__(self, matrix: Optional[Matrix] = None):
        self.log = logging.getLogger(__name__)
        self.scores: dict[str, float] = {}
        self.taxa: list[str] = []
        self.cache: dict[str, float] = {}
        self.dist = hammingdist

        if matrix:
            #self.matrix: dict[str, str] = cast(dict, matrix)  # enforce type
            self.matrix: dict[str, str] = {
                str(k): "".join(matrix[k]) for k in matrix
            }
            self.taxa.extend(self.matrix.keys())

    @property
    def qscores(self) -> Dict[str, List[NumericType]]:
        if not hasattr(self, '_qscores'):
            self._qscores: dict[str, List[NumericType]] = dict(zip(
                self.matrix, [[0.0, 0.0] for _ in self.matrix]))
        return self._qscores
    
    def ncombinations(self, n: int) -> int:
        # http://stackoverflow.com/questions/3025162/
        return int(reduce(
            mul, (Fraction(len(self.taxa) - i, i + 1) for i in range(n)), 1
        ))
    
    def nquartets(self) -> int:
        """Calculates the number of quartets"""
        if not hasattr(self, "_nquartets"):
            self.log.debug("nquartets")
            self._nquartets = self.ncombinations(4)
        return self._nquartets
    
    def get_cachekey(self, taxon1: str, taxon2: str) -> str:
        """Returns a consistent cache key"""
        return "_vs_".join(sorted([taxon1, taxon2]))

    def get_dist(self, taxon1: str, taxon2: str) -> float:
        """Gets distance between sequence1 and sequence2"""
        if taxon1 == taxon2:  # return 0 for identity matches
            return 0.0
        return self.cache[self.get_cachekey(taxon1, taxon2)]

    def _get_score_for_quartet(self, quartet: QuartetType) -> Tuple[QuartetType, float]:
        """
        Calculates score for given quartet
        
        NOTE: needs to be overridden in subclass. Here it just returns 0.0
        """
        return (quartet, 0.0)
        
    def score(self, workers: int = 1) -> Dict[str, float]:
        """Returns a dictionary of metric scores"""
        # go through quartet and calculate scores
        self.log.debug("score: calculate combinations")
        quartets = combinations(self.matrix, 4)

        self.log.debug("_setup_cache: set up cache (n=%d)" % self.ncombinations(2))
        self.cache = {
            self.get_cachekey(t1, t2): self.dist(self.matrix[t1], self.matrix[t2])
            for t1, t2 in combinations(self.matrix, 2)
        }

        if workers > 1:  # parallel process
            self.log.debug("score: starting work (%d workers)" % workers)

            with multiprocessing.Pool(processes=workers) as pool:
                chunksize = 65535
                self.log.debug("score: set chunksize to %d" % chunksize)
                self.log.debug("score: _get_score_for_quartet (n=%d)" % self.nquartets())
                for i, (quartet, d) in enumerate(pool.imap_unordered(self._get_score_for_quartet, quartets, chunksize=chunksize), 1):
                    for taxon in quartet:
                        self.qscores[taxon][0] += d
                        self.qscores[taxon][1] += 1

                self.log.debug("score: pool close")
                pool.close()
                pool.join()

        else:  # single process
            self.log.debug("score: starting work (single process)")
            self.log.debug("score: _get_score_for_quartet (n=%d)" % self.nquartets())
            for i, quartet in enumerate(quartets, 1):
                _, d = self._get_score_for_quartet(quartet)
                for taxon in quartet:
                    self.qscores[taxon][0] += d
                    self.qscores[taxon][1] += 1

        return self._summarise_taxon_scores()

    def _summarise_taxon_scores(self) -> Dict[str, float]:
        """Summarises quartet scores for each taxon"""
        self.log.debug("_summarise_taxon_scores")
        for taxon in self.qscores:
            self.scores[taxon] = (
                self.qscores[taxon][0] / self.qscores[taxon][1]
            )
        return self.scores
    
    def pprint(self) -> None:
        if not self.scores:
            raise ValueError("Scores not calculated yet. Run .score()")
        max_len = max([len(_) for _ in self.matrix])
        for taxon in sorted(self.scores):
            print("%s\t%f" % (taxon.ljust(max_len), self.scores[taxon]))

