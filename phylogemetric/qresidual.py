from math import pow
from itertools import combinations

from .metric import Metric


class QResidualMetric(Metric):
    """
    Calculates the Q-Residual Score (Gray et al. 2010) for a nexus file.

    Returns a dictionary of Q-Residual scores for each taxon
    """
    def _get_score_for_quartet(self, quartet):
        """Calculates score for given quartet"""
        i, j, k, l = quartet
        dij = self.get_dist(i, j, self.matrix[i], self.matrix[j])
        dkl = self.get_dist(k, l, self.matrix[k], self.matrix[l])
        dik = self.get_dist(i, k, self.matrix[i], self.matrix[k])
        djl = self.get_dist(j, l, self.matrix[j], self.matrix[l])
        dil = self.get_dist(i, l, self.matrix[i], self.matrix[l])
        djk = self.get_dist(j, k, self.matrix[j], self.matrix[k])
        
        m1, m2, m3 = sorted([dij + dkl, dik + djl, dil + djk], reverse=True)
        return pow((m1 - m2), 2)
    
    def _summarise_taxon_scores(self):
        """Summarises quartet scores for each taxon"""
        scale = self.get_average_distance()
        scale = scale * scale
        self.scores = {}
        for taxon in self.qscores:
            numerator = self.qscores[taxon][0] / scale
            self.scores[taxon] = numerator / self.qscores[taxon][1]
        return self.scores
    
    def score(self):
        self.qscores = dict(zip(self.matrix, [[0,0] for _ in self.matrix]))
        # go through quartet and calculate scores
        for quartet in combinations(self.matrix, 4):
            score = self._get_score_for_quartet(quartet)
            for taxon in quartet:
                self.qscores[taxon][0] += score
                self.qscores[taxon][1] += 1
        return self._summarise_taxon_scores()

    def get_average_distance(self):
        return sum(self.cache.values()) / len(self.cache.values())