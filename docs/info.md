<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements a Tiny Tapeout wrapper (`tt_um_lif`) around a time-multiplexed
dual-neuron LIF core (`tm_lif2`).

- Top module: `tt_um_lif` (`src/tt_um_lif.v`)
- Core module: `tm_lif2` (`src/tm_lif2.v`)

Behavior summary:

- `ui_in[7:0]` is routed as neuron 0 input current.
- `uio_in[7:0]` is routed as neuron 1 input current.
- A free-running 8-bit counter is shown on `uo_out[7:0]`.
- The dual LIF core updates two neuron states and emits spike pulses.
- Spike outputs are exposed on bidirectional outputs (`uio_out`), with output enable set high.

## How to test

From the `test/` directory you can run the simulation.

Shell (preferred if a Makefile is present):

```sh
cd test
make sim
```

Fallback using Icarus Verilog:

```sh
iverilog -o sim.vvp ../src/tt_um_lif.v ../src/tm_lif2.v tb.v
vvp sim.vvp
```

Waveform files are produced in `test/` (e.g., `tb.fst`) and can be inspected with GTKWave:

```sh
gtkwave test/tb.fst test/tb.gtkw
```

Key signals:

- `ui_in[7:0]` and `uio_in[7:0]` — two neuron input currents.
- `uo_out[7:0]` — counter output.
- `uio_out` — includes spike outputs from the LIF core.
- `uio_oe` — driven high so `uio_out` actively drives outputs.

Use the testbench `test/tb.v` and the provided wave settings `test/tb.gtkw` to verify behavior.

## External hardware

No external hardware required. The design is purely digital and simulated in software.

