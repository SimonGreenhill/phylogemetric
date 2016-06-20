import re
import sys
import unittest

# do not want to use the unified io.* library on py2.7 as we get a TypeError:
#   TypeError: unicode argument expected, got 'str'
# for TestMetric.test_pprint
try:
    from StringIO import StringIO
except:
    from io import StringIO
    
from phylogemetric.metric import Metric
from phylogemetric.tests.data_simple import MATRIX


class TestDist(unittest.TestCase):
    def setUp(self):
        self.metric = Metric()

    def test_identical(self):
        assert self.metric.dist(['1', '0'], ['1', '0']) == 0.0
    
    def test_difference(self):
        assert self.metric.dist(['0', '0'], ['1', '1']) == 1.0
    
    def test_half(self):
        assert self.metric.dist(['1', '1'], ['0', '1']) == 0.5
        assert self.metric.dist(['1', '1'], ['1', '0']) == 0.5
    
    def test_missing(self):
        assert self.metric.dist(['1', '?'], ['0', '1']) == 1.0
        assert self.metric.dist(['1', '1'], ['1', '?']) == 0.0
        
    def test_gap(self):
        assert self.metric.dist(['1', '-'], ['0', '1']) == 1.0
        assert self.metric.dist(['1', '1'], ['1', '-']) == 0.0

    def test_nquartets(self):
        assert Metric(dict([(_, []) for _ in range(0, 5)])).nquartets() == 5
        assert Metric(dict([(_, []) for _ in range(0, 6)])).nquartets() == 15
        assert Metric(dict([(_, []) for _ in range(0, 7)])).nquartets() == 35
        assert Metric(dict([(_, []) for _ in range(0, 8)])).nquartets() == 70
        assert Metric(dict([(_, []) for _ in range(0, 9)])).nquartets() == 126
        assert Metric(dict([(_, []) for _ in range(0, 10)])).nquartets() == 210


class TestMetric(unittest.TestCase):
    # tests that require data
    def setUp(self):
        self.metric = Metric(MATRIX)
        self.metric.score()
    
    def test_get_dist_same_taxon(self):
        assert self.metric.get_dist('A', 'A', [0, 1], [0, 1]) == 0.0
    
    def test_regenerate_qscores(self):
        m = Metric(MATRIX)
        assert m.qscores is not None
        m.qscores = None
        m.score()
    
    def test_pprint(self):
        stdout = sys.stdout
        sys.stdout = StringIO()
        self.metric.pprint()
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = stdout
        # all scores will be 0 as `Metric` doesn't implement a distance
        expected = sorted(MATRIX.keys())
        obtained = sorted(re.findall(r"""([A-E]{1})\s+""", out))
        self.assertEqual(expected, obtained)


if __name__ == '__main__':
    unittest.main()
