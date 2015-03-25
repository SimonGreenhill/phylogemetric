import unittest

from phylogemetric import QResidualMetric

from data_simple import MATRIX as SIMPLE_MATRIX
from data_simple import EXPECTED as SIMPLE_EXPECTED

from data_complex import MATRIX as COMPLEX_MATRIX
from data_complex import EXPECTED as COMPLEX_EXPECTED

class Test_QResidualMetric_Simple(unittest.TestCase):
    def setUp(self):
        self.expected = dict([(k, SIMPLE_EXPECTED[k]['q']) for k in SIMPLE_EXPECTED])
        self.QResidualMetric = QResidualMetric(SIMPLE_MATRIX)
        self.QResidualMetric.score()
    
    def test(self):
        errors = 0
        for taxon in self.expected:
            expected = round(self.expected[taxon], 5)
            obtained = round(self.QResidualMetric.scores[taxon], 5)
            
            if expected != obtained:
                print("\nERROR %s got %0.5f expected %0.5f" % (taxon, obtained, expected))
                errors += 1
        assert errors == 0


class Test_QResidualMetric_Complex(unittest.TestCase):
    def setUp(self):
        self.expected = dict([(k, COMPLEX_EXPECTED[k]['q']) for k in COMPLEX_EXPECTED])
        self.QResidualMetric = QResidualMetric(COMPLEX_MATRIX)
        self.QResidualMetric.score()

    def test(self):
        for taxon in self.expected:
            expected = round(self.expected[taxon], 4)
            obtained = round(self.QResidualMetric.scores[taxon], 4)
            assert expected == obtained, "%s got %0.5f expected %0.5f" % (taxon, obtained, expected)


if __name__ == '__main__':
    unittest.main()