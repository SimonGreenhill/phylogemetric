import pytest

from phylogemetric.metric import Metric
from phylogemetric.delta import DeltaScoreMetric
from phylogemetric.qresidual import QResidualMetric

# Data
@pytest.fixture
def simple_matrix():
    from phylogemetric.tests.data_simple import MATRIX
    return MATRIX


@pytest.fixture
def simple_expected():
    from phylogemetric.tests.data_simple import EXPECTED
    return EXPECTED


@pytest.fixture
def complex_matrix():
    from phylogemetric.tests.data_complex import MATRIX
    return MATRIX


@pytest.fixture
def complex_expected():
    from phylogemetric.tests.data_complex import EXPECTED
    return EXPECTED


# metrics
@pytest.fixture
def simple_metric(simple_matrix):
    return Metric(simple_matrix)
    

@pytest.fixture
def simple_delta(simple_matrix):
    d = DeltaScoreMetric(simple_matrix)
    d.score()
    return d


@pytest.fixture
def complex_delta(complex_matrix):
    d = DeltaScoreMetric(complex_matrix)
    d.score()
    return d


@pytest.fixture
def simple_qres(simple_matrix):
    d = QResidualMetric(simple_matrix)
    d.score()
    return d


@pytest.fixture
def complex_qres(complex_matrix):
    d = QResidualMetric(complex_matrix)
    d.score()
    return d
    