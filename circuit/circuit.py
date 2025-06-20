import time

from zk_protocol import utility
from isogeny_curve import curve, sidh
import wire
import gate


def one_gate():
    t0 = time.perf_counter()
    # one gate
    circuit = Circuit()
    # Add wires
    circuit.add_wire('input1')
    circuit.add_wire('input2')
    circuit.add_wire('output1')
    # print(circuit)
    # Add gates
    circuit.add_gate(['input1', 'input2'], 'output1', 'OR')
    # print(circuit.wires.values())
    # Set input values
    circuit.set_input('input1', 1)
    circuit.set_input('input2', 0)
    # print(circuit.gates)
    # print(circuit.wires.values())
    # compute circuit
    circuit.evaluate()
    print("Output values: ", circuit.wires['output1'].value)
    # set SIDH commitments
    circuit.set_sidh_commitments(c, params)
    print("committed vals", circuit.wires.get('input1').value.bit, circuit.wires.get('input2').value.bit,
          circuit.wires.get('output1').value.bit)
    # verify SIDH commitments
    print(circuit.verify_sidh_commitments())
    t1 = time.perf_counter()
    print(f"Execution time: {t1 - t0} seconds")

def two_gate():
    t0 = time.perf_counter()
    # two gates
    circuit = Circuit()
    # Add wires
    circuit.add_wire('input1')
    circuit.add_wire('input2')
    circuit.add_wire('input3')
    circuit.add_wire('output1')
    circuit.add_wire('output2')
    # Add gates
    circuit.add_gate(['input1', 'input2'], 'output1', 'OR')
    circuit.add_gate(['input3', 'output1'], 'output2', 'AND')
    # Set input values
    circuit.set_input('input1', 1)
    circuit.set_input('input2', 0)
    circuit.set_input('input3', 1)
    # compute circuit
    circuit.evaluate()
    print("Output values: ", circuit.wires['output1'].value, circuit.wires['output2'].value)
    # set SIDH commitments
    circuit.set_sidh_commitments(c, params)
    print("committed vals", circuit.wires.get('input1').value.get_commitment(), circuit.wires.get('input2').value.bit,
          circuit.wires.get('output1').value.bit, circuit.wires.get('output2').value.bit)
    # verify SIDH commitments
    print(circuit.verify_sidh_commitments())
    t1 = time.perf_counter()
    print(f"Execution time: {t1 - t0} seconds")


def n_gate(n):
    t0 = time.perf_counter()
    # n gates
    circuit = Circuit()
    # Add wires
    for i in range(n):
        circuit.add_wire(f'input{i}')
    # circuit.add_wire('output1')
    # Add gates
    for i in range(n - 1):
        circuit.add_gate([f'input{i}', f'input{i + 1}'], f'output{i}', 'AND')
    # Set input values
    for i in range(n):
        circuit.set_input(f'input{i}', 1)
    # compute circuit
    circuit.evaluate()
    # print(circuit)
    # print("Output values: ", circuit.wires[f'output{n-2}'].value)
    # set SIDH commitments
    circuit.set_sidh_commitments(c, params)
    # print("committed vals", circuit.wires.get('input1').value.bit, circuit.wires.get('input2').value.bit,
          # circuit.wires.get('output1').value.bit)
    # verify SIDH commitments
    print(circuit.verify_sidh_commitments())
    t1 = time.perf_counter()
    print(f"Execution time: {t1 - t0} seconds")


class Circuit:
    def __init__(self):
        # Set of wires W = {w_i}  # values in {0,1}
        self.wires = {}
        # Set of gates G = {g_i}  # each gate is a tuple (input_i, output_i, gate_type)
        self.gates = []
        self.commitments = []

    def add_wire(self, wire_id, value=None):
        self.wires[wire_id] = wire.Wire(wire_id, value)

    def add_gate(self, input_ids, output_id, gate_type):
        for id in input_ids:
            self.add_wire(id)  # Ensure input wires are added
        circuit_gate = gate.Gate(input_ids, output_id, gate_type)
        self.gates.append(circuit_gate)
        if output_id not in self.wires:
            self.add_wire(output_id)

    def set_input(self, wire_id, value):
        #self.add_wire(wire_id, value)
        if wire_id not in self.wires:
            raise ValueError(f"Wire {wire_id} not found in circuit.")
        self.wires[wire_id].set_value(value)

    def set_commitments(self, input):
        bitstring1, bitstring2 = utility.j_to_bin_str(input)
        self.commitments, bitstring = utility.bit_commitment(bitstring1, bitstring2)
        # while len(self.wires) < len(self.commitments):
        #     wire_id = f'wire_{len(self.wires)}'
        #     self.add_wire(wire_id)
        wire_list = list(self.wires.keys())
        for i, (bit, com, r) in enumerate(self.commitments):
            if i < len(wire_list):
                w = self.wires[wire_list[i]]
                w.set_value(int(bit))
                w.set_commitment(bit, com, r)
            else:
                raise ValueError("Not enough wires to set commitments.")
        return self.commitments

    def commmit_to_inputs(self):
        for w in self.wires.values():
            if w.value is None:
                continue
            bit = str(w.value)
            com, r = utility.commit_bit(bit)
            w.set_commitment(w.value, com, r)

    def verify_coms(self):
        for w in self.wires.values():
            if w.verify_commitment():
                print(f"Wire {w.wire_id} commitment verified.")
            else:
                print(f"Wire {w.wire_id} commitment verification failed.")
        return True

    def verify_commitments(self, commitments):
        for com in commitments:
            if not self.wires[com[0]].verify_commitment():
                raise ValueError("Commitment verification failed.")
        return True

    def set_sidh_commitments(self, curve, params):
        for w in self.wires.values():
            if w.value is None:
                continue
            bit = str(w.value)
            w.set_sidh_commitment(bit, curve, params)

    def verify_sidh_commitments(self):
        for w in self.wires.values():
            if not w.verify_sidh_commitment():
                raise ValueError("SIDH commitment verification failed.")
        return True

    def evaluate(self):
        wire_values = {wid: wire.value for wid, wire in self.wires.items()}
        for g in self.gates:
            if wire_values[g.input_wires[0]] is None or wire_values[g.input_wires[1]] is None:
                raise ValueError("Input wires must have values before evaluation.")
            out_val = g.compute(wire_values)
            wire_values[g.output_wire] = out_val
            self.wires[g.output_wire].value = out_val
        return wire_values

    def __repr__(self):
        return f"Circuit(wires={list(self.wires.keys())}, gates={self.gates})"


if __name__ == "__main__":
    # Example usage
    # instantiate SIDH
    c = curve.create_curve(2, 18, 3, 13, 1)
    params = sidh.create_params(c.l_a, c.e_a, c.l_b, c.e_b, c.P_a, c.Q_a, c.P_b, c.Q_b)
    one_gate()
    print("-------------------")
    n_gate(10)
    print("-------------------")
    n_gate(100)
    print("-------------------")
    # n_gate(10000)
