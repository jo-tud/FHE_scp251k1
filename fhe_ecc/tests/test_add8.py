import numpy as np
from fhe_ecc.ops import add8
from fhe_ecc.constants import WIDTH, CHUNK_SIZE
from fhe_ecc.utils import e, d

def test_add8():

    a = e(55066263022277343669578816853432625060345377759417550018736038911672924)
    b = e(12670510020758816978050704318447127338065924327593890433575733748242000)

    result = d(add8(a, b))
    expected = d(a)+d(b)
    assert np.array_equal(result, expected), f"Error: {result} != {expected}"
    
    a = e(500)
    b = e(500)
    result = add8(a, b)
    expected = e(d(a)+d(b))
    assert np.array_equal(result, expected), f"Error: {result} != {expected}"
    assert d(result) == d(a)+d(b)

    a = e(435345)
    b = e(0)
    result = add8(a, b)
    expected = a
    assert np.array_equal(result, expected), f"Error: {result} != {expected}"
    assert d(result) == d(a)+d(b)

    max_chunk_value = 2**CHUNK_SIZE-1
    a = np.full(WIDTH//CHUNK_SIZE, max_chunk_value)
    b = np.full(WIDTH//CHUNK_SIZE, 0)
    result = add8(a, b)
    expected = np.full(WIDTH//CHUNK_SIZE, max_chunk_value)
    assert np.array_equal(result, expected), f"Error: {result} != {expected}"
    assert d(result) == d(a)+d(b)


