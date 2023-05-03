import numpy as np
from fhe_ecc.ops import rshift8, lshift8
from fhe_ecc.constants import WIDTH, CHUNK_SIZE
from fhe_ecc.utils import e, d
from concrete import fhe
import pytest

@pytest.mark.fhe_shift
@pytest.mark.fhe
def test_fhe_lshift():    

    @fhe.compiler({"x": "encrypted"})
    def lshift(x: np.ndarray) -> np.ndarray:
        return lshift8(x)

    a = e(1)

    inputset = [(a)]
    circuit = lshift.compile(inputset)

    expected_res = lshift8(a)
     #res = circuit.encrypt_run_decrypt(a)
    res = circuit.simulate(a)

    assert np.array_equal(res, expected_res)
    assert d(res) == d(expected_res)

@pytest.mark.fhe_shift
@pytest.mark.fhe
def test_fhe_rshift():    

    @fhe.compiler({"x": "encrypted"})
    def rshift(x: np.ndarray) -> np.ndarray:
        return rshift8(x)

    a = e(99999999999999999999999999999999999999999999)

    inputset = [(a)]
    circuit = rshift.compile(inputset)

    expected_res = rshift8(a)
     #res = circuit.encrypt_run_decrypt(a)
    res = circuit.simulate(a)

    assert np.array_equal(res, expected_res)
    assert d(res) == d(expected_res)
