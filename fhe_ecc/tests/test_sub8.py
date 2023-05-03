import numpy as np
from fhe_ecc.ops import sub8
from fhe_ecc.utils import e,d
from fhe_ecc.constants import WIDTH, CHUNK_SIZE

def test_sub8_zero():    
    max_chunk_value = 2**CHUNK_SIZE-1
    a = np.full(WIDTH, max_chunk_value)
    b = np.full(WIDTH, 0)
    result = sub8(a, b)
    expected = np.full(WIDTH, max_chunk_value)
    assert np.array_equal(result, expected), f"Error: {result} != {expected}"

def test_sub8_itself():    
    max_chunk_value = 2**CHUNK_SIZE-1
    a = np.full(WIDTH, max_chunk_value)
    result = sub8(a, a)
    expected = np.full(WIDTH, 0)
    assert np.array_equal(result, expected), f"Error: {result} != {expected}"


def test_sub8_borrow():    
    max_chunk_value = 2**CHUNK_SIZE-1
    a = 12345678
    b = 9999999
    result = sub8(e(a), e(b))
    expected = e(a-b)
    assert np.array_equal(result, expected), f"Error: {result} != {expected}"
    assert np.array_equal(d(result),d(expected)), f"Error: {d(result)} != {d(expected)}"