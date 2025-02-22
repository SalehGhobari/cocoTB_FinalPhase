import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.result import TestSuccess

@cocotb.test()
async def test_program_counter(dut):
    """Testbench for programCounter module."""

    # Start a clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    async def reset_counter():
        dut.rst.value = 0  # Active low reset
        await FallingEdge(dut.clk)  # Wait for one clock cycle
        dut.rst.value = 1  # Deactivate reset
        await RisingEdge(dut.clk)

    # Initialize signals
    dut.enable.value = 0
    dut.PCin.value = 0
    await reset_counter()  # Reset the counter

    # Debug: Print initial state
    dut._log.info(f"After reset: PCout = {dut.PCout.value}")

    # Test 1: Check reset behavior
    assert dut.PCout.value == 2046, f"Reset failed: expected 2046, got {dut.PCout.value}"

    # Test 2: Check counter hold when enable is low
    dut.enable.value = 0
    dut.PCin.value = 100
    await RisingEdge(dut.clk)
    dut._log.info(f"After hold: PCout = {dut.PCout.value}")
    assert dut.PCout.value == 2046, f"Hold failed: expected 2046, got {dut.PCout.value}"
    

    # Test 3: Check counter update when enable is high
    dut.enable.value = 1
    dut.PCin.value = 100
    await Timer(1, units="ns")
    await RisingEdge(dut.clk)
    await Timer(1, units = "ns")
    dut._log.info(f"After update: PCout = {dut.PCout.value}")
    assert dut.PCout.value == 100, f"Update failed: expected 100, got {dut.PCout.value}"

    # Test 4: Check counter hold again
    dut.enable.value = 0
    dut.PCin.value = 200
    await Timer(1, units="ns")
    await RisingEdge(dut.clk)
    await Timer(1, units = "ns")
    dut._log.info(f"After hold: PCout = {dut.PCout.value}")
    assert dut.PCout.value == 100, f"Hold failed: expected 100, got {dut.PCout.value}"

    # Test 5: Check counter update with a new value
    dut.enable.value = 1
    dut.PCin.value = 200
    await Timer(1, units="ns")
    await RisingEdge(dut.clk)
    await Timer(1, units = "ns")
    dut._log.info(f"After update: PCout = {dut.PCout.value}")
    assert dut.PCout.value == 200, f"Update failed: expected 200, got {dut.PCout.value}"

    # Test 6: Reset again and verify
    await reset_counter()
    dut._log.info(f"After reset: PCout = {dut.PCout.value}")
    assert dut.PCout.value == 2046, f"Reset failed: expected 2046, got {dut.PCout.value}"

    raise TestSuccess("All programCounter test cases passed!")