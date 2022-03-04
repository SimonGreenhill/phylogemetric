from .metric import Metric

# Delta Score
#  - scores each taxon for how often it's involved in conflicting signal
#  - for each quartet (i,j,k,l)
#     - sum paths of
#         d(i-j) + d(k-l)
#         d(i-k) + d(j-l)
#         d(i-l) + d(j-k)
#     - m1, m2, m3 = these values from largest to smallest.
#     - score for the quartet is:
#         - (m1 - m2) / (m1 - m3)
#         - (or 0 if denominator is zero)
#
#     - rational - score is 0 if distances between 4 taxa exactly fit a tree.
#                 - otherwise it ranges from [0 - 1]
#
#     - note: scaling distances by some constant has no effect on delta.
#
# - in practice normalization by (m1 - m3) obscures some of the signal.
#     Q-residual =  (m1-m2)^2
#     - all distances need to be rescaled before computing Q.
#         -> make average of distances between taxa =1
#
#import numba

class DeltaScoreMetric(Metric):
    """
    Calculates the Delta Score (Holland et al. 2002) for a nexus file.

    Returns a dictionary of delta scores for each taxon.
    """
    #@numba.jit
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
        denom = (m1 - m3)
        if denom == 0:
            return (quartet, 0.0)
        else:
            return (quartet, (m1 - m2) / denom)

