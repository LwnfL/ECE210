<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements a single Leaky Integrate-and-Fire (LIF) neuron in Verilog.

- Module: `lif` (`src/lif.v`).
- Inputs: `current[7:0]` (input sample), `clk`, `rst_n` (active low reset).
- Outputs: `state[7:0]` (internal membrane potential/state), `spike` (pulse when state >= threshold).

Behavior summary:

- next_state = current + (state >> 1) (simple leaky integration).
- On reset (`!rst_n`) the neuron `state` is cleared and the internal `threshold` is initialized.
- `spike` is asserted when `state >= threshold`.

Source module: `lif.v` (neuron implementation).

## How to test

From the `test/` directory you can run the simulation. Typical flows:

Shell (preferred if a Makefile is present):

```sh
cd test
make sim
```

Fallback using Icarus Verilog:

```sh
iverilog -o sim.vvp ../src/lif.v tb.v
vvp sim.vvp
```

Waveform files are produced in `test/` (e.g., `tb.fst`) and can be inspected with GTKWave:

```sh
gtkwave test/tb.fst test/tb.gtkw
```

Key signals:
- Input: `current[7:0]` — input sample driving the neuron.
- Outputs: `state[7:0]` — membrane state; `spike` — neuron spike output.

Use the testbench `test/tb.v` and the provided wave settings `test/tb.gtkw` to verify behavior.

## External hardware

No external hardware required. The design is purely digital and simulated in software.

If you prefer, I can also update `info.yaml` (project title/top_module/source_files) and `test/Makefile` to reflect that this is a single-`lif` project.

