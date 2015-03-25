class Metric(object):
    """Base Metric Class"""
    def __init__(self, matrix=None):
        self.matrix = matrix
        self.cache = {}
        self.scores = {}
    
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
    
    def get_dist(self, taxon1, taxon2, sequence1, sequence2):
        """
        Gets distance between sequence1 and sequence2
        
        Handles caching of scores too.
        """
        
        # return 0 for identity matches
        if taxon1 == taxon2:
            return 0.0
        # check cache
        elif (taxon1, taxon2) in self.cache:
            return self.cache[(taxon1, taxon2)]
        elif (taxon2, taxon1) in self.cache:
            return self.cache[(taxon2, taxon1)]
        else:
            dist = self.dist(sequence1, sequence2)
            self.cache[(taxon1, taxon2)] = dist
            self.cache[(taxon2, taxon1)] = dist
            return dist
    
    def pprint(self):
        max_len = max([len(_) for _ in self.matrix])
        for taxon in sorted(self.scores):
            print("%s\t%0.4f" % (taxon.ljust(max_len + 1), self.scores[taxon]))