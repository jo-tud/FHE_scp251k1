
import numpy as np
from fhe_ecc.constants import WIDTH
from fhe_ecc.utils import e, d


def encode_decode(number: int):
    return d(e(number))

def test_enc_dec():   
    max = 2**WIDTH-1

    a = 1
    assert (encode_decode(a)==a)

    a = 0
    assert (encode_decode(a)==a)

    a = max
    assert (encode_decode(a)==a)

    a = int(2**60)
    assert (encode_decode(a)==a)
