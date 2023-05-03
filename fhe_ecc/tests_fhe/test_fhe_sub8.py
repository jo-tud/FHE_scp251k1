import numpy as np
from fhe_ecc.ops import sub8
from fhe_ecc.constants import WIDTH, CHUNK_SIZE
from concrete import fhe
from fhe_ecc.utils import e, d
import pytest

@pytest.mark.fhe_sub
@pytest.mark.fhe
def test_fhe_sub8_e_e():    

    @fhe.compiler({"x": "encrypted", "y": "encrypted"})
    def sub(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return sub8(x,y)

    a = e(3558685672)
    b = e(999999999)

    inputset = [(a, b)]
    circuit = sub.compile(inputset)

    expected_res = sub(a, b)
    #res = circuit.encrypt_run_decrypt(a, b)
    res = circuit.simulate(a, b)

    assert np.array_equal(res, expected_res)
    assert d(res) == d(expected_res)

@pytest.mark.fhe_sub
@pytest.mark.fhe
def test_fhe_sub8_e_c():    

    @fhe.compiler({"x": "encrypted", "y": "clear"})
    def sub(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return sub8(x,y)
    
    a = e(134)
    b = e(0)

    inputset = [(a, b)]
    circuit = sub.compile(inputset)

    expected_res = sub(a, b)
    #res = circuit.encrypt_run_decrypt(a, b)
    res = circuit.simulate(a, b)

    assert np.array_equal(res, expected_res)
    assert d(res) == d(expected_res)

@pytest.mark.fhe_sub
@pytest.mark.fhe
def test_fhe_sub8_c_e():    

    @fhe.compiler({"x": "clear", "y": "encrypted"})
    def sub(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return sub8(x,y)

    a = e(2342)
    b = e(768)

    inputset = [(a, b)]
    circuit = sub.compile(inputset)

    expected_res = sub(a, b)
    #res = circuit.encrypt_run_decrypt(a, b)
    res = circuit.simulate(a, b)

    assert np.array_equal(res, expected_res)
    assert d(res) == d(expected_res)