import numpy as np
from fhe_ecc.ops import add8
from fhe_ecc.constants import WIDTH, CHUNK_SIZE
from concrete import fhe
from fhe_ecc.utils import e, d
import pytest


@pytest.mark.fhe_add
@pytest.mark.fhe
def test_fhe_add8_e_e():    

    @fhe.compiler({"x": "encrypted", "y": "encrypted"})
    def add(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return add8(x,y)

    a = e(55066263022277343669578718895168534326250603453777594175500187360389116729240)
    b = e(12670510020758816978083085130507043184471273380659243275938904335757337482424)

    inputset = [(a, b)]
    circuit = add.compile(inputset)

    expected_res = add(a, b)
    res = circuit.encrypt_run_decrypt(a, b)

    assert np.array_equal(res, expected_res)
    assert d(res) == d(expected_res)


@pytest.mark.fhe_add
@pytest.mark.fhe
def test_fhe_add8_e_c():    

    @fhe.compiler({"x": "encrypted", "y": "clear"})
    def add(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return add8(x,y)
    
    a = e(134)
    b = e(2422)

    inputset = [(a, b)]
    circuit = add.compile(inputset)

    expected_res = add(a, b)
    res = circuit.encrypt_run_decrypt(a, b)

    assert np.array_equal(res, expected_res)
    assert d(res) == d(expected_res)


@pytest.mark.fhe_add
@pytest.mark.fhe
def test_fhe_add8_c_e():    

    @fhe.compiler({"x": "clear", "y": "encrypted"})
    def add(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return add8(x,y)

    a = e(1)
    b = e(2)

    inputset = [(a, b)]
    circuit = add.compile(inputset)

    expected_res = add(a, b)
    res = circuit.encrypt_run_decrypt(a, b)

    assert np.array_equal(res, expected_res)
    assert d(res) == d(expected_res)