# Practical Guide to Quantum Computing

<img src="https://content.packt.com/B31331/cover_image_large.jpg?version=1754997372" alt="Book Cover" width="300"/>

Code examples and implementations from the book **"A Practical Guide to Quantum Computing"** by Elías F. Combarro and Samuel González Castillo.

**Book:** [A Practical Guide to Quantum Computing - Packt](https://www.packtpub.com/en-us/product/a-practical-guide-to-quantum-computing-9781835885956)

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync

# Run a script
uv run <script.py>
```

## Examples

| File | Description |
|------|-------------|
| `first_qubit.py` | Basic quantum circuit with X and H gates |
| `bb84.py` | BB84 Quantum Key Distribution Protocol |

## Requirements

- Python 3.12+
- Qiskit 2.x
- qiskit-aer
- qiskit-ibm-runtime (for running on real quantum computers)
