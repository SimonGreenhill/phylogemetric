import unittest

from phylogemetric.qresidual import QResidualMetric
from phylogemetric.delta import DeltaScoreMetric
from phylogemetric.bin.phylogemetric import parse_args

class TestScript(unittest.TestCase):
    def test_parse_args_fail_on_missing_file(self):
        with self.assertRaises(IOError):
            parse_args("qresidual", "sausage.nex")
    
    def test_parse_args_fail_on_invalid_method(self):
        with self.assertRaises(SystemExit):
            parse_args("PefectMethod", __file__)
    
    def test_parse_args_qresidual(self):
        assert parse_args("q",  __file__)[0] == QResidualMetric
        assert parse_args("qres", __file__)[0] == QResidualMetric
        assert parse_args("qresidual", __file__)[0] == QResidualMetric
    
    def test_parse_args_delta(self):
        assert parse_args("d", __file__)[0] == DeltaScoreMetric
        assert parse_args("delta", __file__)[0] == DeltaScoreMetric


