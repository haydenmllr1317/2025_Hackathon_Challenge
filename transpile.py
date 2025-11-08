import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime.fake_provider import FakeFez
from qiskit.qasm2 import dump
from qiskit.quantum_info import Operator
import os

print(qiskit.__version__)

def read_qasm(qasm_filepath):
  original_circuit = QuantumCircuit.from_qasm_file(qasm_filepath)
  return original_circuit

def read_qasm(qasm_filepath):
  original_circuit = QuantumCircuit.from_qasm_file(qasm_filepath)
  return original_circuit

current_directory = os.getcwd()

# print(current_directory)


original_circuit = read_qasm(current_directory + '/circuits/6.qasm')

two_qubit_gate_count = 0
for instruction in original_circuit.data:
    # Check if the number of qubits the instruction acts on is 2
    if len(instruction.qubits) == 2:
        two_qubit_gate_count += 1

print(f"Number of 2-qubit gates: {two_qubit_gate_count}")


# print(original_circuit)


two_qubit_gate_count = 0
for instruction in original_circuit.data:
    # Check if the number of qubits the instruction acts on is 2
    if len(instruction.qubits) == 2:
        two_qubit_gate_count += 1

print(f"Number of 2-qubit gates: {two_qubit_gate_count}")

qc_all = transpile(original_circuit, coupling_map=None, basis_gates=['cx','u3','u2','u1'], optimization_level=3)

backend_fez = FakeFez()

qc_fez = transpile(
    original_circuit,
    backend=backend_fez,
    optimization_level=3,
    layout_method='sabre',
    routing_method='sabre'
)

# print(qc_all)

# print(qc_fez)

qc_all_2qb_count = 0
for instruction in qc_all.data:
    # Check if the number of qubits the instruction acts on is 2
    if len(instruction.qubits) == 2:
        qc_all_2qb_count += 1

with open("all_qc.qasm", "w") as f:
    dump(qc_all, f)
with open("fez_qc.qasm", "w") as f:
    dump(qc_fez, f)

print(f"Number of 2-qubit gates in fully-connected case: {qc_all_2qb_count}")

qc_all_fez_count = 0
for instruction in qc_fez.data:
    # Check if the number of qubits the instruction acts on is 2
    if len(instruction.qubits) == 2:
        qc_all_fez_count += 1


print(f"Number of 2-qubit gates in IBM Fez case: {qc_all_fez_count}")

# The Operator class attempts to convert the quantum circuit into its corresponding unitary matrix representation.
# For a circuit with n qubits, this matrix has dimensions 2^n x 2^n.
# If the number of qubits is large (typically around 15-20 or more), this matrix becomes too large to allocate in memory,
# leading to a ValueError: Maximum allowed dimension exceeded.
# To avoid this error, we can check the number of qubits before attempting to create the Operator.

# Print the number of qubits to diagnose the issue
print(f"Number of qubits in original_circuit: {original_circuit.num_qubits}")
print(f"Number of qubits in qc_all: {qc_all.num_qubits}")
print(f"Number of qubits in qc_fez: {qc_fez.num_qubits}")

# For circuits with a large number of qubits, checking equivalence using Operator is not feasible.
# If equivalence checking is still desired for large circuits, alternative methods (e.g., property-based checking or simulation)
# that do not rely on dense matrix representation would be required.
# # Commenting out the problematic lines to prevent the error.
# op1 = Operator(original_circuit)
# opall = Operator(qc_all)
# # opfez = Operator(qc_fez)

# are_equivalent_all = op1.equiv(opall)

# # are_equivalent_fez = op1.equiv(opfez)

# print(are_equivalent_all)
