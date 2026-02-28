# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test counter behavior")

    # After reset, counter should be 0
    assert int(dut.uo_out.value) == 0, f"Expected 0 after reset, got {int(dut.uo_out.value)}"

    # Count up for 10 cycles and verify it increments by 1 each cycle
    prev = int(dut.uo_out.value)
    for _ in range(10):
        await ClockCycles(dut.clk, 1)
        curr = int(dut.uo_out.value)
        expected = (prev + 1) & 0xFF
        assert curr == expected, f"Expected {expected}, got {curr}"
        prev = curr

    dut._log.info("Counter counts correctly for 10 cycles")

    # Test wrap-around: advance until a wrap (255 -> 0) is observed
    # Speed up by advancing until near the top of the range
    while int(dut.uo_out.value) < 250:
        await ClockCycles(dut.clk, 1)

    prev = int(dut.uo_out.value)
    # Allow a few cycles to observe the wrap
    for _ in range(20):
        await ClockCycles(dut.clk, 1)
        curr = int(dut.uo_out.value)
        if curr < prev:
            assert curr == 0, f"Expected wrap to 0, got {curr}"
            break
        prev = curr
    else:
        assert False, "Counter did not wrap within expected cycles"

    dut._log.info("Counter wraps around correctly")
