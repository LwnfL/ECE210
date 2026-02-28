# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


async def tick(dut, n=1):
    """Advance n clock cycles and let NBA / GL delays settle before sampling."""
    await ClockCycles(dut.clk, n)
    await Timer(100, units="ns")


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # ---- Reset ----
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await tick(dut, 10)
    dut.rst_n.value = 1

    dut._log.info("Check state after reset")

    # After reset, neuron 0 state (uo_out[5:0]) and spikes (uo_out[7:6]) should be 0
    assert int(dut.uo_out.value) == 0, f"Expected 0 after reset, got {int(dut.uo_out.value)}"

    # ---- Test neuron 0 integration ----
    # Feed a moderate current; neuron 0 updates every other clock (sel toggles).
    # With current=50 and threshold=200, neuron 0 should integrate up and
    # eventually spike within ~10 update cycles.
    dut._log.info("Test neuron 0 integration and spike")
    dut.ui_in.value = 50
    dut.uio_in.value = 0

    saw_spike0 = False
    prev_state = 0
    state_increased = False

    for i in range(30):
        await tick(dut)
        uo = int(dut.uo_out.value)
        state = uo & 0x3F          # uo_out[5:0]
        spike0 = (uo >> 6) & 1     # uo_out[6]

        # Check that membrane potential is increasing (at least once)
        if state > prev_state:
            state_increased = True
        prev_state = state

        if spike0:
            saw_spike0 = True
            dut._log.info(f"Neuron 0 spiked at cycle {i+1}, state reset to {state}")
            break

    assert state_increased, "Neuron 0 state never increased — integration not working"
    assert saw_spike0, "Neuron 0 never spiked within 30 cycles"

    dut._log.info("Neuron 0 integration and spike OK")

    # ---- Test neuron 1 spike ----
    # Drive a large current so neuron 1 spikes quickly.
    dut._log.info("Test neuron 1 spike")
    dut.ui_in.value = 0
    dut.uio_in.value = 250

    saw_spike1 = False
    for i in range(30):
        await tick(dut)
        uo = int(dut.uo_out.value)
        spike1 = (uo >> 7) & 1     # uo_out[7]
        if spike1:
            saw_spike1 = True
            dut._log.info(f"Neuron 1 spiked at cycle {i+1}")
            break

    assert saw_spike1, "Neuron 1 never spiked within 30 cycles"

    dut._log.info("Neuron 1 spike OK")

    # ---- Test both neurons simultaneously ----
    dut._log.info("Test both neurons with simultaneous input")
    dut.ui_in.value = 250
    dut.uio_in.value = 250
    saw_spike0 = False
    saw_spike1 = False
    for i in range(30):
        await tick(dut)
        uo = int(dut.uo_out.value)
        if (uo >> 6) & 1:
            saw_spike0 = True
        if (uo >> 7) & 1:
            saw_spike1 = True
        if saw_spike0 and saw_spike1:
            break

    assert saw_spike0, "No neuron 0 spike during dual-input test"
    assert saw_spike1, "No neuron 1 spike during dual-input test"

    dut._log.info("Both neurons spike correctly — time-mux LIF verified")

