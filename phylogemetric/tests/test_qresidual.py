import pytest

def test_simple(simple_qres, simple_expected):
    for taxon in simple_expected:
        assert taxon in simple_qres.scores, "Missing score for taxon %s" % taxon
        assert pytest.approx(simple_qres.scores[taxon], abs=1e-4) == simple_expected[taxon]['q']
    
    # cache used? 
    assert len(simple_qres.cache) == 10, 'should be 10 things in cache'


def test_complex(complex_qres, complex_expected):
    for taxon in complex_expected:
        assert taxon in complex_qres.scores, "Missing score for taxon %s" % taxon
        assert pytest.approx(complex_qres.scores[taxon], abs=1e-4) == complex_expected[taxon]['q']
    
    # cache used? 
    assert len(complex_qres.cache) == 1225, 'should be 1225 things in cache'

