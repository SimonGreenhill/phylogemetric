from phylogemetric.dist import hammingdist

def test_hammingdist():
    assert hammingdist('10', '10') == 0.0
    assert hammingdist('00', '11') == 1.0
    assert hammingdist('11', '01') == 0.5
    assert hammingdist('11', '10') == 0.5
    assert hammingdist('1?', '01') == 1.0
    assert hammingdist('11', '1?') == 0.0
    assert hammingdist('1-', '01') == 1.0
    assert hammingdist('11', '1-') == 0.0
 