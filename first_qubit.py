import os
from dotenv import load_dotenv
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import matplotlib.pyplot as plt

# Load environment variables from .env
load_dotenv()

# Create circuit with barrier
circuit = QuantumCircuit(1)
circuit.x(0)
circuit.barrier()
circuit.h(0)
circuit.measure_all()

# Connect to IBM Quantum Platform
token = os.getenv("IBM_QUANTUM_TOKEN")
service = QiskitRuntimeService(token=token, channel="ibm_quantum_platform")

# Get the least busy quantum computer
backend = service.least_busy(simulator=False, operational=True)
print(f"Selected backend: {backend}")

# Transpile the circuit for the specific backend
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
transpiled = pm.run(circuit)

# Create sampler and run on real quantum computer
sampler = Sampler(backend)
job = sampler.run([transpiled], shots=100)

print(f"Job ID: {job.job_id()}")
print("Waiting for results...")

# Get results (may take time depending on queue)
result = job.result()[0].data.meas

# Show results
print(f"Counts: {result.get_counts()}")

# Draw the transpiled circuit
transpiled.draw("mpl", idle_wires=False)
plt.show()
