# First Qubit

Runs a single-qubit circuit (`X` then `H`) on real IBM Quantum hardware.

- Picks the least busy operational backend
- Transpiles the circuit for that backend
- Samples 100 shots and plots the transpiled circuit

Expected result: roughly 50/50 counts between `0` and `1`, since `H|1⟩ = |−⟩`.

## Requirements

An IBM Quantum token in `.env` (see `.env.example` at the repo root).

## Run

```bash
uv run examples/01-first-qubit/main.py
```
