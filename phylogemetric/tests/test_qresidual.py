import unittest

from phylogemetric.qresidual import QResidualMetric

from phylogemetric.tests.data_simple import MATRIX as SIMPLE_MATRIX
from phylogemetric.tests.data_simple import EXPECTED as SIMPLE_EXPECTED

from phylogemetric.tests.data_complex import MATRIX as COMPLEX_MATRIX
from phylogemetric.tests.data_complex import EXPECTED as COMPLEX_EXPECTED

class Test_QResidualMetric_Simple(unittest.TestCase):
    def setUp(self):
        self.expected = dict([
            (k, SIMPLE_EXPECTED[k]['q']) for k in SIMPLE_EXPECTED
        ])
        self.metric = QResidualMetric(SIMPLE_MATRIX)
        self.metric.score()
    
    def test(self):
        for taxon in self.expected:
            expected = round(self.expected[taxon], 5)
            obtained = round(self.metric.scores[taxon], 5)
            if expected != obtained:
                raise AssertionError(
                    "%s %0.5f != %0.5f" % (taxon, obtained, expected)
                )


class Test_QResidualMetric_Complex(unittest.TestCase):
    def setUp(self):
        self.expected = dict([
            (k, COMPLEX_EXPECTED[k]['q']) for k in COMPLEX_EXPECTED
        ])
        self.metric = QResidualMetric(COMPLEX_MATRIX)
        self.metric.score()

    def test(self):
        for taxon in self.expected:
            expected = round(self.expected[taxon], 4)
            obtained = round(self.metric.scores[taxon], 4)
            if expected != obtained:
                raise AssertionError(
                    "%s %0.5f != %0.5f" % (taxon, obtained, expected)
                )


if __name__ == '__main__':
    unittest.main()
