# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


async def tick(dut, n=1):
    """Advance n clock cycles and let NBA settle before sampling."""
    await ClockCycles(dut.clk, n)
    await Timer(100, unit="ns")


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await tick(dut, 10)
    dut.rst_n.value = 1

    dut._log.info("Test counter behavior")

    # After reset, counter should be 0
    assert int(dut.uo_out.value) == 0, f"Expected 0 after reset, got {int(dut.uo_out.value)}"

    # Count up for 10 cycles and verify it increments by 1 each cycle
    prev = int(dut.uo_out.value)
    for _ in range(10):
        await tick(dut)
        curr = int(dut.uo_out.value)
        expected = (prev + 1) & 0xFF
        assert curr == expected, f"Expected {expected}, got {curr}"
        prev = curr

    dut._log.info("Counter counts correctly for 10 cycles")

    # Test wrap-around: advance until a wrap (255 -> 0) is observed
    # Speed up by advancing until near the top of the range
    while int(dut.uo_out.value) < 250:
        await tick(dut)

    prev = int(dut.uo_out.value)
    # Allow a few cycles to observe the wrap
    for _ in range(20):
        await tick(dut)
        curr = int(dut.uo_out.value)
        if curr < prev:
            assert curr == 0, f"Expected wrap to 0, got {curr}"
            break
        prev = curr
    else:
        assert False, "Counter did not wrap within expected cycles"

    dut._log.info("Counter wraps around correctly")
    dut._log.info("Test time-mux spikes on uio_out[0] and uio_out[7]")

    dut.ui_in.value = 250
    dut.uio_in.value = 250
    saw_spike0 = False  # uio_out[0]
    saw_spike1 = False  # uio_out[7]
    for _ in range(40):
        await tick(dut)
        uio = int(dut.uio_out.value)
        if (uio & 0x01) != 0:
            saw_spike0 = True
        if (uio & 0x80) != 0:
            saw_spike1 = True
        if saw_spike0 and saw_spike1:
            break

    assert saw_spike0, "No neuron0 spike on uio_out[0]"
    assert saw_spike1, "No neuron1 spike on uio_out[7]"

    dut._log.info("Observed spikes from both time-mux neurons")

