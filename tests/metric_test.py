import unittest
from phylogemetric import Metric

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
