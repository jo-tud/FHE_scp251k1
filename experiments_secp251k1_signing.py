import numpy as np
from concrete import fhe
import hashlib
import random
import ecdsa
from ecdsa.curves import SECP256k1



# Curve parameters
a = 0
b = 7
p = 2**256 - 2**32 - 977
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
h = 1

# Create the base point G
G = np.array([Gx, Gy])

def inv_mod_p(x, p):
    return pow(x, p - 2, p)

def add_points(P, Q, p):
    if P is None: return Q
    if Q is None: return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 == y2:
        return double_point(P, p)

    if x1 == x2:
        return None

    s = ((y2 - y1) * inv_mod_p(x2 - x1, p)) % p
    x3 = (s**2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p

    return np.array([x3, y3])

def double_point(P, p):
    if P is None:
        return None

    x1, y1 = P
    s = ((3 * x1**2 + a) * inv_mod_p(2 * y1, p)) % p
    x3 = (s**2 - 2 * x1) % p
    y3 = (s * (x1 - x3) - y1) % p

    return np.array([x3, y3])

def scalar_mult(k, P, p):
    if k == 0:
        return None

    result = None
    addend = P

    while k:
        if k & 1:
            result = add_points(result, addend, p)
        addend = double_point(addend, p)
        k >>= 1

    return result

def private_to_public(private_key, p, G):
    return scalar_mult(private_key, G, p)

def hash_message(message):
    return int(hashlib.sha256(message.encode('utf-8')).hexdigest(), 16)

def ecdsa_verify(message, signature, public_key, p, n, G):
    r, s = signature
    z = hash_message(message)

    if not (1 <= r < n) or not (1 <= s < n):
        return False

    w = inv_mod_p(s, n)
    u1 = (z * w) % n
    u2 = (r * w) % n

    x, _ = add_points(scalar_mult(u1, G, p), scalar_mult(u2, public_key, p), p)

    return r % n == x % n

def ecdsa_sign(message, private_key, p, n, G):
    z = hash_message(message)
    r = 0
    s = 0

    while not r or not s:
        k = random.randrange(1, n)
        x, _ = scalar_mult(k, G, p)
        r = x % n
        s = (inv_mod_p(k, n) * (z + r * private_key)) % n

    return r, s

import random


def ecdsa_sign2(hashed_message, private_key):
    # Curve parameters
    p = 2**256 - 2**32 - 977
    n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
    Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    G = np.array([Gx, Gy])

    # Point addition for elliptic curves
    def point_add(P, Q, p):
        if np.all(P == np.array([0,0])):
            return Q
        if np.all(Q == np.array([0,0])):
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and (y1 != y2 or y1 == 0):
            return np.array([0, 0])

        if x1 == x2:
            l = (3 * x1 * x1) * pow(2 * y1, -1, p) % p
        else:
            l = (y2 - y1) * pow(x2 - x1, -1, p) % p

        x3 = (l * l - x1 - x2) % p
        y3 = (l * (x1 - x3) - y1) % p
        return x3, y3

    # Scalar multiplication for elliptic curves
    def scalar_mult(k, G, p):
        result = np.array([0, 0])
        current = G

        while k > 0:
            if k % 2:
                result = point_add(result, current, p)
            current = point_add(current, current, p)
            k //= 2

        return result

    # Extended Euclidean algorithm for modular inverse
    def inv_mod_p(a, n):
        t, new_t = 0, 1
        r, new_r = n, a

        for _ in range(256):
            quotient = 0
            try:
                quotient = r // new_r
            except ZeroDivisionError:
                pass            
            t, new_t, quotient = new_t, t - quotient * new_t, quotient
            r, new_r, quotient = new_r, r - quotient * new_r, quotient

        return (t + n) % n

    r = 0
    s = 0

    while not r or not s:
        k = 550662630222773436695787188951685343262506034537775941755001873603891167292434 # random.randrange(1, n)
        Px, _ = scalar_mult(k, G, p)
        r = Px % n
        s = (inv_mod_p(k, n) * (hashed_message + r * private_key)) % n

        print(inv_mod_p(k, n) * (hashed_message +r*private_key) % n)
        print(n)

    print("r:",r)
    print("s:",s)
    return r, s


def main():
    # Generate a private key
    private_key = random.randrange(1, n)
    private_key = 17651905026989572040457232691516362649858112147122850611845203420377099938754

    # Convert private key to public key
    public_key = private_to_public(private_key, p, G)

    # Sign a message
    message = "Hello, world!"
    signature = ecdsa_sign(message, private_key, p, n, G)
    signature2 = ecdsa_sign2(hash_message(message), private_key)


    # Verify the signature1
    is_valid1 = ecdsa_verify(message, signature, public_key, p, n, G)
    print("Signature is valid:", is_valid1)

    # Verify the signature2
    is_valid2 = ecdsa_verify(message, signature2, public_key, p, n, G)
    print("Signature is valid:", is_valid2)

    # Verify the signature3
    public_key_bytes = b'\x04' + public_key[0].to_bytes(32, byteorder='big') + public_key[1].to_bytes(32, byteorder='big')
    signature_bytes = signature[0].to_bytes(32, byteorder='big') + signature[1].to_bytes(32, byteorder='big')
        
    vk = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)
    is_valid3 = vk.verify(signature_bytes, message.encode('utf8'), hashfunc=hashlib.sha256)
    print("Signature is valid:", is_valid3)

if __name__ == "__main__":
    main()
