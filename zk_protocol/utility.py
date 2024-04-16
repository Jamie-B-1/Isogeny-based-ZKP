from Crypto.Hash import SHA3_256
import random


def generate_random_binary_string(length):
    return ''.join(random.choice('01') for _ in range(length))


# hash commitment concatenated with random binary string
def hash_commitment(c, r):
    h_obj = SHA3_256.new()
    h_obj.update(f'{c}'.encode())
    h_obj.update(f'{r}'.encode())
    return h_obj.hexdigest()
