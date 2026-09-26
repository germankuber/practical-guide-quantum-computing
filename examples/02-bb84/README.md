# BB84

Simulation of the BB84 quantum key distribution protocol on `AerSimulator`.

1. Alice generates random bits and random bases (`Z` or `X`) and encodes each bit into a qubit.
2. Bob measures each qubit in a random basis.
3. Both publicly compare bases and keep only the positions where the bases match (sifting).

With no eavesdropper, the sifted keys are identical. Around half of the bits survive sifting.

Runs are reproducible: both Python's `random` and the simulator are seeded with `SEED`.

## Run

```bash
uv run examples/02-bb84/main.py
```
