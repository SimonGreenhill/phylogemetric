import unittest

from phylogemetric import DeltaScoreMetric

from data_simple import MATRIX as SIMPLE_MATRIX
from data_simple import EXPECTED as SIMPLE_EXPECTED

from data_complex import MATRIX as COMPLEX_MATRIX
from data_complex import EXPECTED as COMPLEX_EXPECTED

class Test_DeltaScoreMetric_Simple(unittest.TestCase):
    def setUp(self):
        self.expected = dict([(k, SIMPLE_EXPECTED[k]['delta']) for k in SIMPLE_EXPECTED])
        self.DeltaScoreMetric = DeltaScoreMetric(SIMPLE_MATRIX)
        self.DeltaScoreMetric.score()
    
    def test_A(self):
        assert round(self.DeltaScoreMetric.scores['A'], 5) == self.expected['A']
    
    def test_B(self):
        assert round(self.DeltaScoreMetric.scores['B'], 5) == self.expected['B']
    
    def test_C(self):
        assert round(self.DeltaScoreMetric.scores['C'], 5) == self.expected['C']
    
    def test_D(self):
        assert round(self.DeltaScoreMetric.scores['D'], 5) == self.expected['D']
    
    def test_E(self):
        assert round(self.DeltaScoreMetric.scores['E'], 5) == self.expected['E']
    


class Test_DeltaScoreMetric_Complex(unittest.TestCase):
    def setUp(self):
        self.expected = dict([(k, COMPLEX_EXPECTED[k]['delta']) for k in COMPLEX_EXPECTED])
        self.DeltaScoreMetric = DeltaScoreMetric(COMPLEX_MATRIX)
        self.DeltaScoreMetric.score()
    
    def test(self):
        for taxon in self.expected:
            expected = round(self.expected[taxon], 3)
            obtained = round(self.DeltaScoreMetric.scores[taxon], 3)
            assert expected == obtained, "%s %0.5f != %0.5f" % (taxon, obtained, expected)
