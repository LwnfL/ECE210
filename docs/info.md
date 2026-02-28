<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

`UM LIF Counter` implements an 8-bit synchronous counter (`tt_um_counter`) with an integrated
leaky integrate-and-fire (LIF) neuron (`lif`). On each rising clock edge the counter increments
and `uo_out` reports the 8-bit value. The most-significant bit (`uo_out[7]`) is used as the
LIF spike output. The `lif` module performs a simple leaky integration:

- `next_state = current + (state >> 1)`
- On `!rst_n` the neuron `state` is cleared and the internal threshold initializes to 200.
- `spike` is asserted when `state >= threshold`.

Source modules: `tt_um_lif.v` (top) and `lif.v` (neuron implementation).

## How to test

From the `test/` directory you can run the provided simulation. Typical flows:

Shell (preferred if a Makefile is present):

```sh
cd test
make sim
```

Fallback using Icarus Verilog:

```sh
iverilog -o sim.vvp ../src/tt_um_lif.v ../src/lif.v tb.v
vvp sim.vvp
```

Waveform files are produced in `test/` (e.g., `tb.fst`) and can be inspected with GTKWave:

```sh
gtkwave test/tb.fst test/tb.gtkw
```

Key signals:
- Inputs: `ui[7:0]` — current input sample (LSB = `ui[0]`).
- Outputs: `uo[7:0]` — counter value; `uo[7]` is the LIF spike.

Use the testbench `test/tb.v` and the provided wave settings `test/tb.gtkw` to verify behavior.

## External hardware

No external hardware required. The design is purely digital and simulated in software.

