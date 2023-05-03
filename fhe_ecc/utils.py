from fhe_ecc.constants import WIDTH, CHUNK_SIZE
import numpy as np
import hashlib

def sha256(data):
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.digest()

def encode(number: int, width: int = WIDTH) -> np.ndarray:
    # Convert the number to binary representation with the specified width
    binary_repr = np.binary_repr(number, width=width)

    # Split the binary string into chunks of length CHUNK_SIZE
    blocks = [binary_repr[i:i+CHUNK_SIZE] for i in range(0, len(binary_repr), CHUNK_SIZE)]

    # Convert each chunk to an integer and store the results in a numpy array
    if CHUNK_SIZE == 8:
        result = np.array([int(block, 2) for block in blocks], dtype=np.uint16)
    elif CHUNK_SIZE == 16:
        result = np.array([int(block, 2) for block in blocks], dtype=np.uint32)
    elif CHUNK_SIZE == 32:
        result = np.array([int(block, 2) for block in blocks], dtype=np.uint64)
    elif CHUNK_SIZE == 64:
        result = np.array([int(block, 2) for block in blocks], dtype=np.uint128)
    else:
        result = np.array([int(block, 2) for block in blocks])

    return result

def e(number: int, width: int = WIDTH) -> np.ndarray:
    return encode(number, width)

def decode(encoded_number: np.ndarray) -> int:
    # Check that the array has the correct dimensions
    assert encoded_number.shape == (WIDTH // CHUNK_SIZE,)
    
    # Convert each chunk to an integer and concatenate them
    chunks = ['{:08b}'.format(x) for x in encoded_number]
    binary_str = ''.join(chunks)
    return int(binary_str, 2)

def d(encoded_number: int) -> np.array:
    return decode(encoded_number)