from concrete import fhe
import numpy as np

def div(x):
    quotient = 0
    try:
        quotient = x // 0
    except ZeroDivisionError: 
        pass
    
    return x

compiler = fhe.Compiler(div, {"x": "encrypted"})

inputset = [45, 100, 1000]
circuit = compiler.compile(inputset)

x = 20

clear_evaluation = div(x)
homomorphic_evaluation = circuit.encrypt_run_decrypt(x)

print(clear_evaluation, "=", homomorphic_evaluation)