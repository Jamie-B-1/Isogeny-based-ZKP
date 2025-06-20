# Defines a class for a gate in a binary circuit.
# Takes input and output wires and a gate type (AND, OR, XOR, NAND).
# Computes the logical operation of gate on bits
from wire import Wire
from isogeny_curve import curve, sidh

class Gate:
    def __init__(self, input_wires, output_wire, gate_type):
        self.input_wires = input_wires
        self.output_wire = output_wire
        self.gate_type = gate_type

    def compute(self, wire_values):
        x = wire_values[self.input_wires[0]]
        y = wire_values[self.input_wires[1]]
        if self.gate_type == 'AND':
            return x & y
        elif self.gate_type == 'OR':
            return x | y
        elif self.gate_type == 'XOR':
            return x ^ y
        elif self.gate_type == 'NAND':
            return 1 - (x & y)
        else:
            raise ValueError("Invalid gate type")

    def __repr__(self):
        return f"Gate(input={self.input_wires}, output={self.output_wire}, type={self.gate_type})"


if __name__ == "__main__":
    # Example usage
    # Create wires
    wire1 = Wire('input1')
    wire2 = Wire('input2')
    wire3 = Wire('output1')
    # Set values for wires
    wire1.set_value(1)
    wire2.set_value(1)
    # Create a gate
    gate = Gate(['input1', 'input2'], 'output1', 'AND')
    output = gate.compute({wire1.wire_id: wire1.value, wire2.wire_id: wire2.value})
    print(f"Gate output: {output}")
    c = curve.create_curve(2, 4, 3, 3, 1)
    params = sidh.create_params(c.l_a, c.e_a, c.l_b, c.e_b, c.P_a, c.Q_a, c.P_b, c.Q_b)
    wire1.set_sidh_commitment(wire1.value, c, params)
    wire2.set_sidh_commitment(wire2.value, c, params)
    #wire3.set_sidh_commitment(wire3.value, c, params)
    # output2 = gate.compute({wire1.wire_id: wire1.value, wire2.wire_id: wire2.value})
    # print(f"Gate output with SIDH commitment: {output2}")

    # Verify SIDH commitment
    print("Verification of wire1 SIDH commitment:", wire1.verify_sidh_commitment())
    print("Verification of wire2 SIDH commitment:", wire2.verify_sidh_commitment())
    #print("Verification of wire3 SIDH commitment:", wire3.verify_sidh_commitment())

