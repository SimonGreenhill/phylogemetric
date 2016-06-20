import unittest

from phylogemetric.delta import DeltaScoreMetric

from phylogemetric.tests.data_simple import MATRIX as SIMPLE_MATRIX
from phylogemetric.tests.data_simple import EXPECTED as SIMPLE_EXPECTED

from phylogemetric.tests.data_complex import MATRIX as COMPLEX_MATRIX
from phylogemetric.tests.data_complex import EXPECTED as COMPLEX_EXPECTED

class Test_DeltaScoreMetric_Simple(unittest.TestCase):
    def setUp(self):
        self.expected = dict([
            (k, SIMPLE_EXPECTED[k]['delta']) for k in SIMPLE_EXPECTED
        ])
        self.metric = DeltaScoreMetric(SIMPLE_MATRIX)
        self.metric.score()
    
    def test_A(self):
        assert round(self.metric.scores['A'], 5) == self.expected['A']
    
    def test_B(self):
        assert round(self.metric.scores['B'], 5) == self.expected['B']
    
    def test_C(self):
        assert round(self.metric.scores['C'], 5) == self.expected['C']
    
    def test_D(self):
        assert round(self.metric.scores['D'], 5) == self.expected['D']
    
    def test_E(self):
        assert round(self.metric.scores['E'], 5) == self.expected['E']


class Test_DeltaScoreMetric_Complex(unittest.TestCase):
    def setUp(self):
        self.expected = dict([
            (k, COMPLEX_EXPECTED[k]['delta']) for k in COMPLEX_EXPECTED
        ])
        self.metric = DeltaScoreMetric(COMPLEX_MATRIX)
        self.metric.score()
    
    def test(self):
        for taxon in self.expected:
            expected = round(self.expected[taxon], 3)
            obtained = round(self.metric.scores[taxon], 3)
            if expected != obtained:
                raise AssertionError(
                    "%s %0.5f != %0.5f" % (taxon, obtained, expected)
                )


if __name__ == '__main__':
    unittest.main()
