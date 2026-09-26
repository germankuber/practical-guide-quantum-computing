import os
import random
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial

from dotenv import load_dotenv
from qiskit import QuantumCircuit
from qiskit.primitives import BackendSamplerV2
from qiskit.primitives.base import BaseSamplerV2
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import IBMBackend, QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as RuntimeSampler

NUM_BITS = 16
SEED = 18620123
TOKEN_ENV_VAR = "IBM_QUANTUM_API_KEY"

COMPUTATIONAL = 0
HADAMARD = 1

BASIS_SYMBOLS = {
    COMPUTATIONAL: "Z",
    HADAMARD: "X",
}

CircuitPreparation = Callable[[list[QuantumCircuit]], list[QuantumCircuit]]


@dataclass(frozen=True)
class RandomChoices:
    alice_bits: list[int]
    alice_bases: list[int]
    bob_bases: list[int]


@dataclass(frozen=True)
class Transmission:
    alice_bits: list[int]
    alice_bases: list[int]
    bob_bases: list[int]
    bob_results: list[int]


def random_bits(rng: random.Random, size: int) -> list[int]:
    return [rng.randint(0, 1) for _ in range(size)]


def generate_choices(seed: int, size: int) -> RandomChoices:
    rng = random.Random(seed)

    return RandomChoices(
        alice_bits=random_bits(rng, size),
        alice_bases=random_bits(rng, size),
        bob_bases=random_bits(rng, size),
    )


def build_circuit(
    bit: int,
    alice_basis: int,
    bob_basis: int,
) -> QuantumCircuit:
    circuit = QuantumCircuit(1)

    if bit == 1:
        circuit.x(0)

    if alice_basis == HADAMARD:
        circuit.h(0)

    circuit.barrier()

    if bob_basis == HADAMARD:
        circuit.h(0)

    circuit.measure_all()

    return circuit


def build_circuits(
    choices: RandomChoices,
) -> list[QuantumCircuit]:
    return [
        build_circuit(bit, alice_basis, bob_basis)
        for bit, alice_basis, bob_basis in zip(
            choices.alice_bits,
            choices.alice_bases,
            choices.bob_bases,
        )
    ]


def keep_circuits(circuits: list[QuantumCircuit]) -> list[QuantumCircuit]:
    return circuits


def measure_all(
    sampler: BaseSamplerV2,
    circuits: list[QuantumCircuit],
) -> list[int]:
    results = sampler.run(circuits, shots=1).result()

    return [int(result.data.meas.get_bitstrings()[0]) for result in results]


def create_simulator(seed: int) -> BaseSamplerV2:
    return BackendSamplerV2(
        backend=AerSimulator(seed_simulator=seed),
    )


def connect_service() -> QiskitRuntimeService:
    token = os.getenv(TOKEN_ENV_VAR)

    if not token:
        raise SystemExit(f"Missing {TOKEN_ENV_VAR}. Export it or set it in .env (see .env.example).")

    return QiskitRuntimeService(
        token=token,
        channel="ibm_quantum_platform",
    )


def create_ibm_backend(service: QiskitRuntimeService) -> IBMBackend:
    return service.least_busy(
        operational=True,
        simulator=False,
    )


def transpile_for_backend(
    backend: IBMBackend,
    circuits: list[QuantumCircuit],
) -> list[QuantumCircuit]:
    pass_manager = generate_preset_pass_manager(
        backend=backend,
        optimization_level=1,
    )

    return pass_manager.run(circuits)


def transmit(
    sampler: BaseSamplerV2,
    choices: RandomChoices,
    prepare: CircuitPreparation = keep_circuits,
) -> Transmission:
    circuits = prepare(build_circuits(choices))

    return Transmission(
        alice_bits=choices.alice_bits,
        alice_bases=choices.alice_bases,
        bob_bases=choices.bob_bases,
        bob_results=measure_all(sampler, circuits),
    )


def sift_keys(
    transmission: Transmission,
) -> tuple[list[int], list[int]]:
    matching = [
        i
        for i, (alice_basis, bob_basis) in enumerate(
            zip(
                transmission.alice_bases,
                transmission.bob_bases,
            )
        )
        if alice_basis == bob_basis
    ]

    alice_key = [transmission.alice_bits[i] for i in matching]
    bob_key = [transmission.bob_results[i] for i in matching]

    return alice_key, bob_key


def as_bases(bases: list[int]) -> str:
    return " ".join(BASIS_SYMBOLS[basis] for basis in bases)


def as_bits(bits: list[int]) -> str:
    return " ".join(str(bit) for bit in bits)


def print_transmission(
    title: str,
    transmission: Transmission,
) -> None:
    print()
    print(f"=== {title} ===")
    print(f"Alice bits:  {as_bits(transmission.alice_bits)}")
    print(f"Alice bases: {as_bases(transmission.alice_bases)}")
    print(f"Bob bases:   {as_bases(transmission.bob_bases)}")
    print(f"Bob results: {as_bits(transmission.bob_results)}")


def print_keys(
    transmission: Transmission,
) -> None:
    alice_key, bob_key = sift_keys(transmission)

    print(f"Alice key:   {as_bits(alice_key)}")
    print(f"Bob key:     {as_bits(bob_key)}")
    print(f"Key length:  {len(alice_key)}/{len(transmission.alice_bits)}")
    print(f"Keys match:  {alice_key == bob_key}")


def report(title: str, transmission: Transmission) -> None:
    print_transmission(title, transmission)
    print_keys(transmission)


def run_on_simulator(choices: RandomChoices) -> None:
    transmission = transmit(create_simulator(SEED), choices)
    report("AER SIMULATOR", transmission)


def run_on_ibm(choices: RandomChoices) -> None:
    backend = create_ibm_backend(connect_service())

    print()
    print(f"IBM backend: {backend.name}")

    transmission = transmit(
        RuntimeSampler(mode=backend),
        choices,
        prepare=partial(transpile_for_backend, backend),
    )

    report("IBM QUANTUM HARDWARE", transmission)


def main() -> None:
    load_dotenv()
    choices = generate_choices(SEED, NUM_BITS)
    run_on_simulator(choices)
    run_on_ibm(choices)


if __name__ == "__main__":
    main()
