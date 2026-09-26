import random
from dataclasses import dataclass

from qiskit import QuantumCircuit
from qiskit.primitives import BackendSamplerV2 as Sampler
from qiskit_aer import AerSimulator

NUM_BITS = 16
SEED = 18620123

COMPUTATIONAL = 0
HADAMARD = 1
BASIS_SYMBOLS = {COMPUTATIONAL: "Z", HADAMARD: "X"}


@dataclass(frozen=True)
class Transmission:
    alice_bits: list[int]
    alice_bases: list[int]
    bob_bases: list[int]
    bob_results: list[int]


def random_bits(size: int) -> list[int]:
    return [random.randint(0, 1) for _ in range(size)]


def build_circuit(bit: int, alice_basis: int, bob_basis: int) -> QuantumCircuit:
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


def measure(sampler: Sampler, circuit: QuantumCircuit) -> int:
    result = sampler.run([circuit], shots=1).result()[0]
    return int(result.data.meas.get_bitstrings()[0])


def transmit(sampler: Sampler, size: int) -> Transmission:
    alice_bits = random_bits(size)
    alice_bases = random_bits(size)
    bob_bases = random_bits(size)
    bob_results = [
        measure(sampler, build_circuit(bit, alice_basis, bob_basis))
        for bit, alice_basis, bob_basis in zip(alice_bits, alice_bases, bob_bases)
    ]
    return Transmission(alice_bits, alice_bases, bob_bases, bob_results)


def sift_keys(transmission: Transmission) -> tuple[list[int], list[int]]:
    matching = [
        i
        for i, (alice_basis, bob_basis) in enumerate(zip(transmission.alice_bases, transmission.bob_bases))
        if alice_basis == bob_basis
    ]
    alice_key = [transmission.alice_bits[i] for i in matching]
    bob_key = [transmission.bob_results[i] for i in matching]
    return alice_key, bob_key


def as_bases(bases: list[int]) -> str:
    return " ".join(BASIS_SYMBOLS[basis] for basis in bases)


def as_bits(bits: list[int]) -> str:
    return " ".join(str(bit) for bit in bits)


def print_transmission(transmission: Transmission) -> None:
    print(f"Alice bits:  {as_bits(transmission.alice_bits)}")
    print(f"Alice bases: {as_bases(transmission.alice_bases)}")
    print(f"Bob bases:   {as_bases(transmission.bob_bases)}")
    print(f"Bob results: {as_bits(transmission.bob_results)}")


def print_keys(alice_key: list[int], bob_key: list[int], total_bits: int) -> None:
    print(f"Alice key:   {as_bits(alice_key)}")
    print(f"Bob key:     {as_bits(bob_key)}")
    print(f"Key length:  {len(alice_key)}/{total_bits}")
    print(f"Keys match:  {alice_key == bob_key}")


def create_sampler(seed: int) -> Sampler:
    random.seed(seed)
    return Sampler(backend=AerSimulator(seed_simulator=seed))


def main() -> None:
    sampler = create_sampler(SEED)
    transmission = transmit(sampler, NUM_BITS)
    alice_key, bob_key = sift_keys(transmission)
    print_transmission(transmission)
    print()
    print_keys(alice_key, bob_key, NUM_BITS)


if __name__ == "__main__":
    main()
