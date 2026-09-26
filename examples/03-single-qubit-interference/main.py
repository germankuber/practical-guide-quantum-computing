from qiskit import QuantumCircuit
from qiskit.primitives import BackendSamplerV2
from qiskit.primitives.base import BaseSamplerV2
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

SHOTS = 1000
SEED = 18620123
PRECISION = 3


def create_sampler(seed: int) -> BaseSamplerV2:
    return BackendSamplerV2(
        backend=AerSimulator(seed_simulator=seed),
    )


def format_amplitude(amplitude: complex) -> str:
    real = round(amplitude.real, PRECISION) + 0.0
    imag = round(amplitude.imag, PRECISION) + 0.0

    if imag == 0:
        return f"{real:+.{PRECISION}f}"

    return f"{real:+.{PRECISION}f}{imag:+.{PRECISION}f}j"


def format_state(circuit: QuantumCircuit) -> str:
    state = Statevector.from_instruction(circuit)
    amplitude_0, amplitude_1 = state.data

    return f"{format_amplitude(amplitude_0)}|0> {format_amplitude(amplitude_1)}|1>"


def measure_counts(sampler: BaseSamplerV2, circuit: QuantumCircuit) -> dict[str, int]:
    measured_circuit = circuit.copy()
    measured_circuit.measure_all()

    result = sampler.run([measured_circuit], shots=SHOTS).result()[0]

    return dict(sorted(result.data.meas.get_counts().items()))


def report(label: str, sampler: BaseSamplerV2, circuit: QuantumCircuit) -> None:
    print(f"{label:<10} state: {format_state(circuit):<22} counts: {measure_counts(sampler, circuit)}")


def main() -> None:
    sampler = create_sampler(SEED)
    circuit = QuantumCircuit(1)

    report("|0>", sampler, circuit)

    circuit.h(0)
    report("H -> |+>", sampler, circuit)

    circuit.z(0)
    report("Z -> |->", sampler, circuit)

    circuit.h(0)
    report("H -> |1>", sampler, circuit)

    print()
    print(circuit.draw())


if __name__ == "__main__":
    main()
