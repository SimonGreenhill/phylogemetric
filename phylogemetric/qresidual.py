import warnings
from math import pow

from .metric import Metric


class QResidualMetric(Metric):
    """
    Calculates the Q-Residual Score (Gray et al. 2010) for a nexus file.
    
    Returns a dictionary of Q-Residual scores for each taxon
    """
    def _get_score_for_quartet(self, quartet):
        """Calculates score for given quartet"""
        i, j, k, l = quartet
        dij = self.get_dist(i, j)
        dkl = self.get_dist(k, l)
        dik = self.get_dist(i, k)
        djl = self.get_dist(j, l)
        dil = self.get_dist(i, l)
        djk = self.get_dist(j, k)
        
        m1, m2, m3 = sorted([dij + dkl, dik + djl, dil + djk], reverse=True)
        return (quartet, pow((m1 - m2), 2))
    
    def _summarise_taxon_scores(self):
        """Summarises quartet scores for each taxon"""
        scale = pow(self.get_average_distance(), 2)
        self.scores = {}
        for taxon in self.qscores:
            numerator = self.qscores[taxon][0] / scale
            self.scores[taxon] = numerator / self.qscores[taxon][1]
        return self.scores
    
    def get_average_distance(self):
        try:
            return sum(self.cache.values()) / len(self.cache.values())
        except ZeroDivisionError:  # pragma: no cover
            warnings.warn("Zero Division")
            return 0
