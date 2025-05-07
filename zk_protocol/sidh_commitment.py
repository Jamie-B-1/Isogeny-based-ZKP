import random
from zk_protocol import sigma_protocol, utility
from isogeny_curve import curve, sidh
# from circuit import wire, gate, circuit


class BitCom:
    def __init__(self, bit, curve, params):
        self.bit = bit
        self.curve = curve
        self.params = params
        self.challenge = random.choice([-1, 1]) if bit == 0 else random.choice([0, 1])
        self.commitment, self.response = sigma_protocol.prover(curve, params, self.challenge)

    def get_commitment(self):
        try:
            return self.commitment
        except AttributeError:
            raise ValueError("Commitment not set or invalid.")

    def verify(self):
        return sigma_protocol.verify(self.curve, (self.commitment, self.response), self.challenge)


if __name__ == "__main__":
    # Example usage
    c = curve.create_curve(2, 4, 3, 3, 1)
    params = sidh.create_params(c.l_a, c.e_a, c.l_b, c.e_b, c.P_a, c.Q_a, c.P_b, c.Q_b)
    bitcom = BitCom(1, c, params)
    bitcom2 = BitCom(0, c, params)
    print("Commitment:", bitcom.commitment)
    print("Response:", bitcom.response)

    print("Verification of second commit:", bitcom2.verify())
    print("Verification:", bitcom.verify())
