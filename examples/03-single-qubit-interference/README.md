# Single Qubit Interference

Shows how the relative phase between `|0>` and `|1>` is invisible to a single measurement but decides the outcome once the amplitudes interfere.

| Step | Gate | State | Z-basis measurement |
|------|------|-------|---------------------|
| 0 | — | `\|0>` | always `0` |
| 1 | `H` | `\|+> = (\|0> + \|1>)/√2` | 50/50 |
| 2 | `Z` | `\|-> = (\|0> - \|1>)/√2` | 50/50 |
| 3 | `H` | `\|1>` | always `1` |

`|+>` and `|->` produce the same statistics in the Z basis: they differ only in the sign of the `|1>` amplitude. The final `H` makes the amplitudes interfere:

- `H|+> = |0>`: the `|1>` contributions cancel (destructive interference).
- `H|-> = |1>`: the `|0>` contributions cancel.

So `H·H|0> = |0>`, but `H·Z·H|0> = |1>`. The phase flip introduced by `Z` only becomes observable through interference.

For each step the script prints the exact statevector amplitudes and the counts of 1000 shots on `AerSimulator`, then draws the final circuit. The simulator is seeded with `SEED`, so runs are reproducible.

## Run

```bash
uv run examples/03-single-qubit-interference/main.py
```
