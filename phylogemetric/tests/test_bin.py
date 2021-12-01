import os
import re
import pytest

from phylogemetric.delta import DeltaScoreMetric
from phylogemetric.qresidual import QResidualMetric
from phylogemetric.bin.phylogemetric import parse_args, main
from phylogemetric.bin.create_random_nexus import create_nex

TEST_NEXUS_FILE = os.path.join(os.path.dirname(__file__), '../data', 'test.nex')

def test_parse_args_fail_on_missing_file():
    with pytest.raises(IOError):
        parse_args("qresidual", "sausage.nex")


def test_parse_args_fail_on_invalid_method():
    with pytest.raises(SystemExit):
        parse_args("PefectMethod", __file__)


def test_parse_args_qresidual():
    assert parse_args("q", __file__)[0] == QResidualMetric
    assert parse_args("qres", __file__)[0] == QResidualMetric
    assert parse_args("qresidual", __file__)[0] == QResidualMetric


def test_parse_args_delta():
    assert parse_args("d", __file__)[0] == DeltaScoreMetric
    assert parse_args("delta", __file__)[0] == DeltaScoreMetric


def test_main(capsys, simple_expected):
    main(args=['delta', TEST_NEXUS_FILE])
    captured = capsys.readouterr() 
    for taxon in sorted(simple_expected):
        line = r"""%s\s+%f""" % (taxon, simple_expected[taxon]['delta'])
        assert len(re.findall(line, captured.out)) == 1, 'Expected %r' % line


def test_createnex():
    nex = create_nex(3, 3, 'acgt')
    assert 'ntax=3' in nex
    assert 'nchar=3' in nex
    assert 'species000' in nex
    assert 'species001' in nex
    assert 'species002' in nex
