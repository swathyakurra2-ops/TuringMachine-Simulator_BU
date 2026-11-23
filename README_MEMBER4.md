# Member 4 — Simulation Execution Engine

This is a small extension to the original TMsimulator project. The original
machine, tape, parser and example transition definitions are retained. The
new `TMsim/execution.py` wraps the original `TuringMachine` and adds:

- single-transition execution (`execute_step`)
- continuous execution (`run_continuously`)
- pause and resume controls
- reset to the original input configuration
- maximum-step protection
- execution status and transition history
- explicit handling of missing transitions

## Requirements

- Python 3.8 or later
- No third-party packages are required

## Run

From this directory:

```bash
python run_simulator.py
```

Press Enter at the machine-file prompt to use `codes/1tape_inverse.txt`.
Enter a binary input such as `0101`, then use these commands:

- `step` — execute one transition
- `run` — start continuous execution in the background
- `pause` — pause a running simulation
- `resume` — continue a paused simulation
- `status` — show state, step count and tape
- `history` — show recorded transitions
- `reset` — restore the initial configuration
- `quit` — exit

You can also choose another machine definition by entering its path. Relative
paths are resolved from this project directory.

## Tests

Run from this directory:

```bash
python -m unittest discover -s tests -v
```

## Integration note

The wrapper deliberately uses the existing `TuringMachine.make_step()` and
existing tape class. If the team later replaces the tape implementation or
transition manager, keep the same machine-facing methods (`make_step`,
`get_config`, `state`, `steps`, `tapes`, `_initialize`, and `load_input`) or
adapt the wrapper at that integration boundary.

## Attribution

Base project: TMsimulator by Simone Gasperini,
https://github.com/SimoneGasperini/TMsimulator . The original source files and
example machine definitions are retained; the execution wrapper, runner,
tests and this documentation are additions for the team project.

The ZIP supplied for this work did not contain a licence file. Confirm the
upstream repository's current licence and follow its terms before redistributing
the combined project publicly or submitting it as a redistributed derivative.
