import os
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
    
from phylogemetric.qresidual import QResidualMetric
from phylogemetric.delta import DeltaScoreMetric
from phylogemetric.bin.phylogemetric import parse_args, main
from phylogemetric.bin.create_random_nexus import create_nex
from phylogemetric.tests.data_simple import EXPECTED

TEST_NEXUS_FILE = os.path.join(os.path.dirname(__file__), '../data', 'test.nex')

class Test_ParseArgs(unittest.TestCase):
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


class Test_Main(unittest.TestCase):
    def test_main(self):
        stdout = sys.stdout
        sys.stdout = StringIO()
        main(args=['delta', TEST_NEXUS_FILE])
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = stdout
        
        for taxon in sorted(EXPECTED):
            line = r"""%s\s+%f""" % (taxon, EXPECTED[taxon]['delta'])
            assert len(re.findall(line, out)) == 1, 'Expected %r' % line
    
    def test_sys_argv(self):
        stdout = sys.stdout
        argv = sys.argv
        sys.stdout = StringIO()
        sys.argv = ["testcase", "qres", TEST_NEXUS_FILE]
        main()
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = stdout
        sys.argv = argv
        
        for taxon in sorted(EXPECTED):
            line = r"""%s\s+%f""" % (taxon, EXPECTED[taxon]['q'])
            assert len(re.findall(line, out)) == 1, 'Expected %r' % line
        

class Test_CreateNex(unittest.TestCase):
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
