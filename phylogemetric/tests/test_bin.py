import unittest

from phylogemetric.qresidual import QResidualMetric
from phylogemetric.delta import DeltaScoreMetric
from phylogemetric.bin.phylogemetric import parse_args
from phylogemetric.bin.create_random_nexus import create_nex

class TestScript(unittest.TestCase):
    def test_parse_args_fail_on_missing_file(self):
        with self.assertRaises(IOError):
            parse_args("qresidual", "sausage.nex")
    
    def test_parse_args_fail_on_invalid_method(self):
        with self.assertRaises(SystemExit):
            parse_args("PefectMethod", __file__)
    
    def test_parse_args_qresidual(self):
        assert parse_args("q", __file__)[0] == QResidualMetric
        assert parse_args("qres", __file__)[0] == QResidualMetric
        assert parse_args("qresidual", __file__)[0] == QResidualMetric
    
    def test_parse_args_delta(self):
        assert parse_args("d", __file__)[0] == DeltaScoreMetric
        assert parse_args("delta", __file__)[0] == DeltaScoreMetric


class TestCreateNex(unittest.TestCase):
    def setUp(self):
        self.nex = create_nex(3, 3, list('acgt'))
    
    def test_ntax(self):
        assert 'ntax=3' in self.nex
        
    def test_nchar(self):
        assert 'nchar=3' in self.nex
        
    def test_species(self):
        assert 'species000' in self.nex
        assert 'species001' in self.nex
        assert 'species002' in self.nex
        


if __name__ == '__main__':
    unittest.main()
