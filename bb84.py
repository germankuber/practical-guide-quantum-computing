import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSamplerV2 as Sampler

random.seed(18620123)
backend = AerSimulator(seed_simulator=18620123)
sampler = Sampler(backend=backend)

# The key we want to send:
alice_bits = [0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0]
# A list for the bits that bob will receive:
bob_bits = []

# We will create lists to store whether Alice/Bob used H.
# If they do, we add "True", otherwise we add "False".
alice_used_h = []
bob_used_h = []

for bit in alice_bits:
    circuit = QuantumCircuit(1)
    # If we are going to send 1, we apply an X gate.
    # Remember that the state is initialized to |0>.
    if bit:
        circuit.x(0)

    # Choose at random if Alice applies H, and do it.
    alice_h = random.choice([True, False])
    if alice_h:
        circuit.h(0)

    # Apply a barrier and choose whether Bob does H, and do it.
    circuit.barrier()
    bob_h = random.choice([True, False])
    if bob_h:
        circuit.h(0)

    # Measure the qubit (on Bob's end).
    circuit.measure_all()
    job = sampler.run([circuit], shots=1)
    bob_bit = int(job.result()[0].data.meas.get_bitstrings()[0])

    # Add the measured bit to bob_bits and record who used H.
    bob_bits.append(bob_bit)
    alice_used_h.append(alice_h)
    bob_used_h.append(bob_h)

# List of indices where Alice and Bob agree on whether to apply H.
agree = [i for i in range(len(alice_used_h)) if alice_used_h[i] == bob_used_h[i]]

# Get the sent/received bits when they agree on applying H.
alice = [alice_bits[i] for i in agree]
bob = [bob_bits[i] for i in agree]

print(alice)
print(bob)
