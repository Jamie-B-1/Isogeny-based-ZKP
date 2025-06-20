import random
import time
from zk_protocol import sigma_protocol, utility
from isogeny_curve import curve, sidh
# from circuit import wire, gate, circuit
from zk_protocol.sidh_ladders.prover import p1
from zk_protocol.sidh_ladders.verifier import v


class BitCom:
    def __init__(self, bit, curve, params):
        self.bit = bit
        self.curve = curve
        self.params = params
        t0 = time.perf_counter()
        self.bit_proof = utility.bit_proof(bit)
        t1 = time.perf_counter()
        #print(f"Time taken for bit proof: {t1-t0:} seconds")
        self.challenge = random.choice([-1, 1]) if bit == 0 else random.choice([0, 1])
        self.commitment, self.response = sigma_protocol.prover(curve, params, self.challenge)
        # self.commitment = p1(self.challenge)

    def get_commitment(self):
        try:
            return self.commitment
        except AttributeError:
            raise ValueError("Commitment not set or invalid.")

    def verify(self):
        if self.bit_proof:
            return sigma_protocol.verify(self.curve, (self.commitment, self.response), self.challenge)
            # return v(self.challenge, self.commitment)
        else:
            return "bit commitment failed, invalid bit value"


if __name__ == "__main__":
    # Example usage
    c = curve.create_curve(2, 4, 3, 3, 1)
    params = sidh.create_params(c.l_a, c.e_a, c.l_b, c.e_b, c.P_a, c.Q_a, c.P_b, c.Q_b)
    bitcom = BitCom(1, c, params)
    print(bitcom.challenge)
    bitcom2 = BitCom(0, c, params)
    print("Commitment:", bitcom.commitment)
    #print("Response:", bitcom.response)

    print("Verification of second commit:", bitcom2.verify())
    print("Verification:", bitcom.verify())
