import numpy as np
from fhe_ecc.ops import rshift8, lshift8
from fhe_ecc.constants import WIDTH, CHUNK_SIZE
from fhe_ecc.utils import e, d

def test_lshift():
    # Test case 1
    arr1 = np.array([1, 2, 3, 4, 5])
    expected_output1 = np.array([2, 3, 4, 5, 1])
    assert np.array_equal(lshift8(arr1), expected_output1)

    # Test case 2
    arr2 = np.array([5, 4, 3, 2, 1])
    expected_output2 = np.array([4, 3, 2, 1, 5])
    assert np.array_equal(lshift8(arr2), expected_output2)

    # Test case 3
    arr3 = np.array([1])
    expected_output3 = np.array([1])
    assert np.array_equal(lshift8(arr3), expected_output3)


def test_rshift():
    # Test case 1
    arr1 = np.array([1, 2, 3, 4, 5])
    expected_output1 = np.array([5, 1, 2, 3, 4])
    assert np.array_equal(rshift8(arr1), expected_output1)

    # Test case 2
    arr2 = np.array([5, 4, 3, 2, 1])
    expected_output2 = np.array([1, 5, 4, 3, 2])
    assert np.array_equal(rshift8(arr2), expected_output2)

    # Test case 3
    arr3 = np.array([1])
    expected_output3 = np.array([1])
    assert np.array_equal(rshift8(arr3), expected_output3)
