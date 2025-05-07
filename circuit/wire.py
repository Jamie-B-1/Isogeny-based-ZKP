from zk_protocol import utility, sidh_commitment
from isogeny_curve import curve, sidh


# Defines a wire in a binary circuit that can be assigned a value
# Hash and SIDH based commitments can be made to the value by a prover and verified by a verifier
class Wire:
    def __init__(self, wire_id, value=None):
        self.wire_id = wire_id
        self.value = value
        self.bit = None
        # hash based commitment attribute
        self.commitment = None  # (bit, com, r) for commitment

    # sets a value and confirms it is a bit
    def set_value(self, value):
        if not utility.bit_proof(value):
            raise ValueError("Invalid bit value. Bit must be 0 or 1.")
        self.value = value

    # sets a hash based commitment
    def set_commitment(self, bit, com, r):
        self.commitment = (bit, com, r)

    # sets a SIDH-based commitment
    def set_sidh_commitment(self, bit, curve, params):
        self.bit = bit
        # sidh commitment to bit assigned to wire value
        # overwrites the bit value with a hiding commitment to the bit
        self.value = sidh_commitment.BitCom(bit, curve, params)

    # verifies the SIDH commitment using the SIDH protocol
    def verify_sidh_commitment(self):
        return self.value.verify()

    # verifies a hash based commitment by opening to a bit
    def verify_commitment(self):
        if self.commitment is None:
            raise ValueError("No commitment set for this wire.")
        bit, com, r = self.commitment
        return utility.open_commitment(bit, r, com)

    def __repr__(self):
        return f"Wire(id={self.wire_id}, value={self.value})"


if __name__ == "__main__":
    # Test usage
    c = curve.create_curve(2, 4, 3, 3, 1)
    params = sidh.create_params(c.l_a, c.e_a, c.l_b, c.e_b, c.P_a, c.Q_a, c.P_b, c.Q_b)
    wire1 = Wire("wire_1")
    wire2 = Wire("wire_2")
    # Set value and commitment
    wire1.set_value(1)
    wire2.set_value(0)
    print("Wire 1 Value:", wire1.value)
    print("Wire 2 Value:", wire2.value)
    # Set SIDH commitment
    wire1.set_sidh_commitment(wire1.value, c, params)
    wire2.set_sidh_commitment(wire2.value, c, params)
    # Print SIDH commitments
    print("Wire 1 SIDH Commitment:", wire1.value.get_commitment()[0])
    print("Wire 2 SIDH Commitment:", wire2.value.get_commitment()[0])
    # Verify SIDH commitment
    print("Wire 1 Commitment Verification:", wire1.verify_sidh_commitment())
    print("Wire 2 Commitment Verification:", wire2.verify_sidh_commitment())
