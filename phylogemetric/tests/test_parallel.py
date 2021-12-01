import pytest

from phylogemetric.metric import Metric
from phylogemetric.delta import DeltaScoreMetric
from phylogemetric.qresidual import QResidualMetric

NPROCESSES = 2


def test_delta_simple(simple_matrix, simple_expected):
    metric = DeltaScoreMetric(simple_matrix)
    metric.score(workers=NPROCESSES)
    for taxon in simple_expected:
        assert taxon in metric.scores, "Missing score for taxon %s" % taxon
        assert pytest.approx(metric.scores[taxon], abs=1e-4) == simple_expected[taxon]['delta']


def test_delta_complex(complex_matrix, complex_expected):
    metric = DeltaScoreMetric(complex_matrix)
    metric.score(workers=NPROCESSES)
    for taxon in complex_expected:
        assert taxon in metric.scores, "Missing score for taxon %s" % taxon
        assert pytest.approx(metric.scores[taxon], abs=1e-4) == complex_expected[taxon]['delta']


def test_qresidual_simple(simple_matrix, simple_expected):
    metric = QResidualMetric(simple_matrix)
    metric.score(workers=NPROCESSES)
    for taxon in simple_expected:
        assert taxon in metric.scores, "Missing score for taxon %s" % taxon
        assert pytest.approx(metric.scores[taxon], abs=1e-4) == simple_expected[taxon]['q']


def test_qresidual_complex(complex_matrix, complex_expected):
    metric = QResidualMetric(complex_matrix)
    metric.score(workers=NPROCESSES)
    for taxon in complex_expected:
        assert taxon in metric.scores, "Missing score for taxon %s" % taxon
        assert pytest.approx(metric.scores[taxon], abs=1e-4) == complex_expected[taxon]['q']
