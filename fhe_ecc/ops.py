import numpy as np
from ecdsa import SECP256k1, SigningKey, VerifyingKey
from fhe_ecc.constants import WIDTH, CHUNK_SIZE
from concrete import fhe
from fhe_ecc.utils import e, d

# def add8(a: np.ndarray, b: np.ndarray) -> np.ndarray:
#     # Check that a and b have the same shape
#     assert a.shape == b.shape
    
#     # Initialize an array to store the result
#     result = fhe.zeros(a.shape)
    
#     # Initialize a carry variable to 0
#     carry = 0

#     # Iterate over the elements of a and b
#     for i in range(a.size):
#         # Compute the sum of the current elements and the carry
#         sum = a[i] + b[i] + carry
        
#         # Compute the carry for the next element
#         carry = sum // (2**CHUNK_SIZE-1) # bit-size dependent
        
#         # Store the result in the result array after applying modulo to handle overflow
#         result[i] = sum % (2**CHUNK_SIZE-1) # bit-size dependent

#     # Return the result array
#     return result

# Shifts elements of the array one position to the left and sets the last element to zero.
def lshift8(arr: np.ndarray) -> np.ndarray:
    tmp = arr[0]
    arr[:-1] = arr[1:]  # Shift elements to the left
    arr[-1] = tmp
    return arr

def rshift8(arr: np.ndarray) -> np.ndarray:
    tmp = arr[-1]
    arr[1:] = arr[:-1]  # Shift elements to the right
    arr[0] = tmp
    return arr


def add8(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    carry = 0
    result = fhe.zeros(a.size)
    for i in range(a.size-1, -1, -1):
        tmp = a[i] + b[i] + carry
        carry = tmp >> CHUNK_SIZE
        result[i] = tmp % 2**CHUNK_SIZE
    return result



def sub8(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    borrow = 0
    result = fhe.zeros(a.size)
    for i in range(a.size-1, -1, -1):
        tmp = a[i] - b[i] - borrow
        borrow = tmp >> CHUNK_SIZE & 1
        result[i] = tmp % 2**CHUNK_SIZE
    return result


