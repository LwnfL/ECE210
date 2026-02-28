<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works


Both neurons take turns with the same update logic.

- **Even ticks (`sel = 0`):** neuron 0 state and spike registers are updated.
- **Odd ticks (`sel = 1`):** neuron 1 state and spike registers are updated.

So only 1 neuron's state gets written each clock and the neurons updates at half the clock freq.

1. **Leak:** `s = max(state - 1, 0)`
2. **Integrate:** `s = s + current`
3. **Fire:** if `s >= 200` then `spike = 1, state = 0`, else `spike = 0, state = s`

`ui_in[7:0]` → Neuron 0 input current
`uio_in[7:0]` → Neuron 1 input current (all bidirectional pins configured as inputs)
`uo_out[5:0]` → Neuron 0 membrane state (lower 6 bits)
`uo_out[6]` → Neuron 0 spike
`uo_out[7]` → Neuron 1 spike

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

- `ui_in[7:0]` — neuron 0 input current.
- `uio_in[7:0]` — neuron 1 input current.
- `uo_out[5:0]` — neuron 0 membrane state (6 bits).
- `uo_out[6]` — neuron 0 spike.
- `uo_out[7]` — neuron 1 spike.

Use the testbench `test/tb.v` and the provided wave settings `test/tb.gtkw` to verify behavior.

## External hardware

No external hardware required. The design is purely digital and simulated in software.

