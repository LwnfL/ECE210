![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# Time-Multiplexed LIF Neuron — Tiny Tapeout

A time-multiplexed dual **Leaky Integrate-and-Fire (LIF)** neuron circuit designed for [Tiny Tapeout](https://tinytapeout.com).

## Overview

Two LIF neurons share a single sequential update path, alternating on even/odd clock ticks. This demonstrates **time-multiplexing** — a common technique in neuromorphic hardware to trade clock cycles for silicon area.

| Feature | Detail |
|---------|--------|
| Neurons | 2 (time-multiplexed) |
| Precision | 8-bit unsigned |
| Leak | subtract 1, clamp to 0 |
| Threshold | 200 (fires + resets to 0) |
| Top module | `tt_um_lif` |
| Core module | `tm_lif2` |

## Pin mapping

| Pin | Direction | Signal |
|-----|-----------|--------|
| `ui_in[7:0]` | Input | Neuron 0 input current |
| `uio_in[7:0]` | Input | Neuron 1 input current |
| `uo_out[5:0]` | Output | Neuron 0 membrane state (6 bits) |
| `uo_out[6]` | Output | Neuron 0 spike |
| `uo_out[7]` | Output | Neuron 1 spike |

## How to test

```sh
# Using the project Docker image
docker run --rm -it -v "$(pwd)":/workspace jeshragh/ece183-293 bash
cd /workspace/test && make sim

# Or with Icarus Verilog locally
cd test
iverilog -g2012 -o sim.vvp ../src/tt_um_lif.v ../src/tm_lif2.v tb.v
vvp sim.vvp
gtkwave tb.fst tb.gtkw
```

## Project structure

```
src/
  tt_um_lif.v   # TT IO wrapper
  tm_lif2.v     # Time-multiplexed dual LIF core
test/
  tb.v          # Verilog testbench
  test.py       # cocotb test
  Makefile      # simulation driver
docs/
  info.md       # Datasheet content
```

## Documentation

- [Project datasheet](docs/info.md)
- [Tiny Tapeout FAQ](https://tinytapeout.com/faq/)
- [Digital design lessons](https://tinytapeout.com/digital_design/)
- [Learn how semiconductors work](https://tinytapeout.com/siliwiz/)
- [Join the community](https://tinytapeout.com/discord)
- [Build your design locally](https://www.tinytapeout.com/guides/local-hardening/)

## What next?

- [Submit your design to the next shuttle](https://app.tinytapeout.com/).
- Edit [this README](README.md) and explain your design, how it works, and how to test it.
- Share your project on your social network of choice:
  - LinkedIn [#tinytapeout](https://www.linkedin.com/search/results/content/?keywords=%23tinytapeout) [@TinyTapeout](https://www.linkedin.com/company/100708654/)
  - Mastodon [#tinytapeout](https://chaos.social/tags/tinytapeout) [@matthewvenn](https://chaos.social/@matthewvenn)
  - X (formerly Twitter) [#tinytapeout](https://twitter.com/hashtag/tinytapeout) [@tinytapeout](https://twitter.com/tinytapeout)
  - Bluesky [@tinytapeout.com](https://bsky.app/profile/tinytapeout.com)

This README.md was written with the assistance of ChatGPT

### Archived Stuff

# Tiny Tapeout Verilog Project Template

- [Read the documentation for project](docs/info.md)

## What is Tiny Tapeout?

Tiny Tapeout is an educational project that aims to make it easier and cheaper than ever to get your digital and analog designs manufactured on a real chip.

To learn more and get started, visit https://tinytapeout.com.

## Set up your Verilog project

1. Add your Verilog files to the `src` folder.
2. Edit the [info.yaml](info.yaml) and update information about your project, paying special attention to the `source_files` and `top_module` properties. If you are upgrading an existing Tiny Tapeout project, check out our [online info.yaml migration tool](https://tinytapeout.github.io/tt-yaml-upgrade-tool/).
3. Edit [docs/info.md](docs/info.md) and add a description of your project.
4. Adapt the testbench to your design. See [test/README.md](test/README.md) for more information.

The GitHub action will automatically build the ASIC files using [LibreLane](https://www.zerotoasiccourse.com/terminology/librelane/).

## Enable GitHub actions to build the results page

- [Enabling GitHub Pages](https://tinytapeout.com/faq/#my-github-action-is-failing-on-the-pages-part)

## Resources

- [FAQ](https://tinytapeout.com/faq/)