from concrete import fhe
import numpy as np
import random
import ecdsa
from ecdsa.curves import SECP256k1
import hashlib
import time

# TODO: if larger than 4 we get table size errors. But at 4 we get divide by zero warnings. :(
CHUNK_SIZE = 8
WIDTH = 512
DO_FHE_COMP = False
DO_FHE_EVAL = False
DO_FHE_VERIFY = True

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

def double_point(P, p):
    if P is None:
        return None

    x1, y1 = P
    s = ((3 * x1**2 + a) * inv_mod_p(2 * y1, p)) % p
    x3 = (s**2 - 2 * x1) % p
    y3 = (s * (x1 - x3) - y1) % p

    return np.array([x3, y3])

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

# Computes the modular inverse of a modulo n using the extended Euclidean algorithm.
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

def encode(number: int, width: int = WIDTH) -> np.array:
    binary_repr = np.binary_repr(number, width=width)
    blocks = [binary_repr[i:i+CHUNK_SIZE] for i in range(0, len(binary_repr), CHUNK_SIZE)]
    return np.array([int(block, 2) for block in blocks])

def decode(encoded_number: np.array) -> int:
    result = 0
    for i in range(len(encoded_number)):
        result += 2**(CHUNK_SIZE*i) * encoded_number[(len(encoded_number) - i) - 1]
    return int(result)

# secp256k1 parameters
a = 0
b = 7
p = 2**256 - 2**32 - 977
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = np.array([Gx, Gy])

# TODO: for now used as a global (will encrypt?)
r = 0

#@fhe.compiler({"hashed_message": "clear", "private_key": "clear"})
def fhe_secp256k1_signature(hashed_message, private_key):
    global r

    for iter in range(10000):
        k = 550662630222773436695787188951685343262506034537775941755001873603891167292434  # random.randrange(1, n)
        Px, _ = scalar_mult(k, G, p)
        r = Px % n

        # TODO: find a better way to go to the next interation when r == 0
        if r == 0:
            continue
        
        # for better debugging, the calculation of s is split into stages.
        # s = (k_inv * (hashed_message + r * private_key)) % n
        # s = (encode(k_inv) * (hashed_message + np.multiply(encode(r) , private_key))) % encode(n)

        k_inv = inv_mod_p(k, n)
            
        # r * private_key
        with fhe.tag("step 1"):
            a1 = r * decode(private_key)
            print("a1", a1)
            a = encode(r) * private_key
            print("a ", decode(a))

        # hashed_message + r * private_key
        with fhe.tag("step 2"):
            b1 = decode(hashed_message) + decode(a)
            print("b1",b1)
            b = hashed_message + a
            print("b ", decode(b))

        # k_inv * (hashed_message + r * private_key)
        with fhe.tag("step 3"):
            c1 = k_inv * decode(b)
            print("c1", c1)
            c = k_inv * b
            print("c ", decode(c))

        # (k_inv * (hashed_message + r * private_key)) % n
        with fhe.tag("step 4"):
            s1 = (decode(c) % n)
            print("s1", s1)
            s = np.fmod(c, n)
            print(n)
            print("s ", decode(s))
       
        #s = (encode(k_inv) * (hashed_message + np.multiply(encode(r) , private_key))) % encode(n)

        # TODO: also return r as an encrypted value
        # TODO: I don't think it is possible to check that s != 0, so that has to be checked afterwards and then re-evaluated if so.
        return (s)

# The input set for the query circuit
inputset = [
    (
        encode(0), # x
        encode(0), # y
    ),
    (
        encode((2 ** 256 - 1)), # x
        encode((2 ** 256 - 1)), # y
    )
]


message = b"Hello, world!"
message_hash = hashlib.sha256(message).digest()
message_hash_int = int.from_bytes(message_hash, byteorder="big")

# Generate a private key / signing key
sk = ecdsa.keys.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
sk = ecdsa.keys.SigningKey.from_secret_exponent(
    secexp = 17651905026989572040457232691516362649858112147122850611845203420377099938754,
    curve = SECP256k1,
    hashfunc = hashlib.sha256)
sk_int = sk.privkey.secret_multiplier

# Convert signing key to verifying key / public key
vk = sk.get_verifying_key()

# Create a configuration for the compiler
configuration = fhe.Configuration(
    enable_unsafe_features=True,
    use_insecure_key_cache=True,
    insecure_key_cache_location=".keys",
)

if DO_FHE_COMP:
    print(f"Compilation...", flush=True)
    start = time.time()
    circuit = fhe_secp256k1_signature.compile(inputset, configuration)
    end = time.time()
    print(f"(took {end - start:.3f} seconds)")

#print(circuit)

if DO_FHE_EVAL:
    print(f"Evaluation...", flush=True)
    start = time.time()
    res = circuit.encrypt_run_decrypt(encode(message_hash_int), encode(sk_int))
    end = time.time()
    print(f"(took {end - start:.3f} seconds)")

# Create a signature using the ecdsa library and without FHE, for comparison
# note that this is not the same signature because of the random integer

signature_regular = sk.sign(message, hashfunc=hashlib.sha256)
is_valid_regular = vk.verify(signature_regular, message)
print("Regular signature is valid:", is_valid_regular)

res = fhe_secp256k1_signature(encode(message_hash_int), encode(sk_int))

# Verify the FHE signature

if DO_FHE_VERIFY:
    print("r_fhe:", r)
    print("s_fhe:", decode(res))

    signature_fhe = ecdsa.util.sigencode_string(r, decode(res), vk.pubkey.order)
    is_valid_fhe = vk.verify(signature_fhe, message)

    print("FHE signature is valid:", is_valid_fhe)