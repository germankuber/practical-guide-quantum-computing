# BB84

BB84 quantum key distribution protocol, run on `AerSimulator` and then on real IBM Quantum hardware with the same Alice/Bob choices.

1. Alice generates random bits and random bases (`Z` or `X`) and encodes each bit into a qubit.
2. Bob measures each qubit in a random basis.
3. Both publicly compare bases and keep only the positions where the bases match (sifting).

With no eavesdropper, the sifted keys are identical. Around half of the bits survive sifting.

Alice/Bob choices and the simulator are seeded with `SEED`, so simulator runs are reproducible. On real hardware noise can make `Keys match` report `False`.

## Requirements

`IBM_QUANTUM_API_KEY` exported or set in `.env` (see `.env.example` at the repo root) for the hardware run.

## Run

```bash
uv run examples/02-bb84/main.py
```
