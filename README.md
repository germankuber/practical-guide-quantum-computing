# Practical Guide to Quantum Computing

<img src="https://content.packt.com/B31331/cover_image_large.jpg?version=1754997372" alt="Book Cover" width="300"/>

Code examples and implementations from the book **"A Practical Guide to Quantum Computing"** by Elías F. Combarro and Samuel González Castillo.

**Book:** [A Practical Guide to Quantum Computing - Packt](https://www.packtpub.com/en-us/product/a-practical-guide-to-quantum-computing-9781835885956)

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. All examples share one environment defined at the repo root.

```bash
uv sync
cp .env.example .env
```

Set `IBM_QUANTUM_API_KEY` in `.env` only if you want to run examples on real IBM Quantum hardware.

## Examples

| # | Example | Description | Backend | Run |
|---|---------|-------------|---------|-----|
| 01 | [First Qubit](examples/01-first-qubit/) | Single-qubit circuit with X and H gates | IBM Quantum hardware | `uv run examples/01-first-qubit/main.py` |
| 02 | [BB84](examples/02-bb84/) | BB84 Quantum Key Distribution protocol | AerSimulator + IBM Quantum hardware | `uv run examples/02-bb84/main.py` |
| 03 | [Single Qubit Interference](examples/03-single-qubit-interference/) | Relative phase made visible through H-Z-H interference | AerSimulator | `uv run examples/03-single-qubit-interference/main.py` |

## Adding a new example

1. Create `examples/NN-<name>/main.py` using the next number
2. Add a `README.md` inside the folder explaining the concept and how to run it
3. Add a row to the table above
4. Add new dependencies with `uv add <package>`

## Requirements

- Python 3.12+
- Qiskit 2.x
- qiskit-aer
- qiskit-ibm-runtime (for running on real quantum computers)
