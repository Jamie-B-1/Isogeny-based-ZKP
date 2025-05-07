# Defines a class for a gate in a binary circuit.
# Takes input and output wires and a gate type (AND, OR, XOR, NAND).
# Computes the logical operation of gate on bits
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
