from concrete import fhe
import numpy as np
import random
import ecdsa
import hashlib
import time
import fhe_ecc.constants as c



def secp256k1_sign(message_hash, private_key):
    k = random.randrange(1, c.n)
    return _secp256k1_sign(message_hash, private_key, k)

def secp256k1_sign_with_k(message_hash, private_key, k):
    return _secp256k1_sign(message_hash, private_key, k)


def _secp256k1_sign(message_hash, private_key, k):
    
    pass