import pytest

def test_simple(simple_delta, simple_expected):
    for taxon in simple_expected:
        assert taxon in simple_delta.scores, "Missing score for taxon %s" % taxon
        assert pytest.approx(simple_delta.scores[taxon], abs=1e-4) == simple_expected[taxon]['delta']

    # cache used? 
    assert len(simple_delta.cache) == 10, 'should be 10 things in cache'


def test_complex(complex_delta, complex_expected):
    for taxon in complex_expected:
        assert taxon in complex_delta.scores, "Missing score for taxon %s" % taxon
        assert pytest.approx(complex_delta.scores[taxon], abs=1e-4) == complex_expected[taxon]['delta']
    
    # cache used? 
    assert len(complex_delta.cache) == 1225, 'should be 1225 things in cache'

