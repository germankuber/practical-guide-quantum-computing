import os

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import IBMBackend, QiskitRuntimeService, SamplerV2 as Sampler

SHOTS = 100
TOKEN_ENV_VAR = "IBM_QUANTUM_TOKEN"


def build_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(1)
    circuit.x(0)
    circuit.barrier()
    circuit.h(0)
    circuit.measure_all()
    return circuit


def connect_service() -> QiskitRuntimeService:
    token = os.getenv(TOKEN_ENV_VAR)
    if not token:
        raise SystemExit(f"Missing {TOKEN_ENV_VAR}. Copy .env.example to .env and set your token.")
    return QiskitRuntimeService(token=token, channel="ibm_quantum_platform")


def select_backend(service: QiskitRuntimeService) -> IBMBackend:
    backend = service.least_busy(simulator=False, operational=True)
    print(f"Selected backend: {backend}")
    return backend


def transpile_for(backend: IBMBackend, circuit: QuantumCircuit) -> QuantumCircuit:
    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
    return pass_manager.run(circuit)


def sample_counts(backend: IBMBackend, circuit: QuantumCircuit) -> dict[str, int]:
    job = Sampler(backend).run([circuit], shots=SHOTS)
    print(f"Job ID: {job.job_id()}")
    print("Waiting for results...")
    return job.result()[0].data.meas.get_counts()


def show_circuit(circuit: QuantumCircuit) -> None:
    circuit.draw("mpl", idle_wires=False)
    plt.show()


def main() -> None:
    load_dotenv()
    backend = select_backend(connect_service())
    transpiled = transpile_for(backend, build_circuit())
    counts = sample_counts(backend, transpiled)
    print(f"Counts: {counts}")
    show_circuit(transpiled)


if __name__ == "__main__":
    main()
