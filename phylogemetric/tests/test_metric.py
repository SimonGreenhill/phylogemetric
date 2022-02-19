import re
import sys

import pytest

from phylogemetric.metric import Metric
   

def test_nquartets():
    assert Metric(dict([(_, []) for _ in range(0, 5)])).nquartets() == 5
    assert Metric(dict([(_, []) for _ in range(0, 6)])).nquartets() == 15
    assert Metric(dict([(_, []) for _ in range(0, 7)])).nquartets() == 35
    assert Metric(dict([(_, []) for _ in range(0, 8)])).nquartets() == 70
    assert Metric(dict([(_, []) for _ in range(0, 9)])).nquartets() == 126
    assert Metric(dict([(_, []) for _ in range(0, 10)])).nquartets() == 210


def test_get_dist_same_taxon(simple_metric):
    assert simple_metric.get_dist('A', 'A') == 0.0


def test_regenerate_qscores(simple_metric):
    assert simple_metric.qscores is not None
    simple_metric.qscores = None
    simple_metric.score()
    

def test_pprint(capsys, simple_metric):
    simple_metric.score()
    simple_metric.pprint()
    captured = capsys.readouterr() 
    # all scores will be 0 as `Metric` doesn't implement a distance
    expected = sorted(simple_metric.matrix.keys())
    obtained = sorted(re.findall(r"""([A-E]{1})\s+""", captured.out))
    assert expected == obtained


def test_pprint_error(simple_metric):
    with pytest.raises(ValueError) as e:
        simple_metric.pprint()
