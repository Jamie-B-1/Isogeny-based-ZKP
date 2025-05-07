from Crypto.Hash import SHA3_256
import secrets
from isogeny_curve import curve, sidh
import cypari
pari = cypari.pari


# equation to verify a bit is well-formed, 0 or 1 only.
def bit_proof(bit):
    intbit = int(bit)
    if intbit*(intbit-1) == 0:
        return True
    else:
        return False

def generate_random_binary_string(length):
    return ''.join(str(secrets.choice('01')) for _ in range(length))

# hash commitment concatenated with random binary string
def hash_commitment(c, r):
    h_obj = SHA3_256.new()
    h_obj.update(f'{c}'.encode())
    h_obj.update(f'{r}'.encode())
    return h_obj.hexdigest()

# open commitment
def open_commitment(c, r, com):
    h_obj = SHA3_256.new()
    h_obj.update(f'{c}'.encode())
    h_obj.update(f'{r}'.encode())
    if h_obj.hexdigest() == com and bit_proof(c):
        return True
    return False

# function to convert curve j-invariant to binary string
def j_to_bin_str(j):
    # j = a*i + b where a and b are integers and i is the generator of field Fp^2
    str_j = str(j)
    # strip imaginary part from number
    if str_j.count('*i') == 0:
        j = int(str_j)
        return bin(j)[2:], 0
    str_a, str_b = str_j.split('*i + ')
    # use only the real part to convert to binary string
    a, b = int(str_a), int(str_b)
    a_bin = bin(a)[2:]
    b_bin = bin(b)[2:]
    return a_bin, b_bin

# commitment scheme for a binary bit 0 or 1
def commit_bit(bit):
    if bit_proof(bit):
        r = generate_random_binary_string(256)
        return hash_commitment(bit, r), r
    else:
        raise ValueError("Invalid bit value. Bit must be 0 or 1.")

# bit commitment based on hashing the bits from an input binary string
# use in turning a curves j-invariant to a list of committed bits
def bit_commitment(bitstring1, bitstring2):
    bitstring = bitstring1 + bitstring2
    commitments = []
    for bit in bitstring:
        com, r = commit_bit(bit)
        commitments.append((bit, com, r))
    return commitments, bitstring

# open the commitment to check the bit satisfies the gate
def verify_commitments(commitments):
    # check if the commitment is valid
    for i, (bit, com, r) in enumerate(commitments):
        if not open_commitment(bit, r, com):
            print(f"Commitment {i} is invalid.")
            return False
    return True


if __name__ == "__main__":
    c = curve.create_curve(2, 216, 3, 137, 1)
    params = sidh.create_params(c.l_a, c.e_a, c.l_b, c.e_b, c.P_a, c.Q_a, c.P_b, c.Q_b)
    A = sidh.SIDH("A", c.elli_curve, params, c)
    j = A.pub_key[0].j()
    # print(j)
    p = c.p
    # print(p)
    # convert j-invariant to binary string
    a, b = j_to_bin_str(j)
    commitments, bitstring = bit_commitment(a, b)
    verify = verify_commitments(commitments)
    print(verify)
