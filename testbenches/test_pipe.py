import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.result import TestSuccess
import random

@cocotb.test()
async def test_pipe(dut):
    """Testbench for pipe module."""

    # Start a clock
    clock = Clock(dut.clk, 10, units="ns")  # 10 ns clock period
    cocotb.start_soon(clock.start())


    async def reset_pipeline():
        dut.reset.value = 0  # Active low reset
        await FallingEdge(dut.clk)
        dut.reset.value = 1  # Deactivate reset
        await RisingEdge(dut.clk)

    # Initialize signals
    dut.enable.value = 0
    dut.flush.value = 0
    dut.D.value = 0
    await reset_pipeline()

    # Test 1: Check reset behavior
    assert dut.Q.value == 0, f"Reset failed: expected 0, got {dut.Q.value}"

    # Test 2: Check hold behavior when enable is low
    dut.enable.value = 0
    dut.D.value = 0x123456789ABCDEF012345678
    await RisingEdge(dut.clk)
    await Timer(1, units="ns") 
    assert dut.Q.value == 0, f"Hold failed: expected 0, got {dut.Q.value}"

    # Test 3: Check data propagation when enable is high
    dut.enable.value = 1
    dut.D.value = 0x123456789ABCDEF012345678
    await RisingEdge(dut.clk)
    await Timer(1, units="ns") 
    assert dut.Q.value == 0x123456789ABCDEF012345678, f"Data propagation failed: expected 0x123456789ABCDEF012345678, got {dut.Q.value}"

    # Test 4: Check hold behavior again
    dut.enable.value = 0
    dut.D.value = 0xDEADBEEFDEADBEEFDEADBEEF
    await RisingEdge(dut.clk)
    await Timer(1, units="ns") 
    assert dut.Q.value == 0x123456789ABCDEF012345678, f"Hold failed: expected 0x123456789ABCDEF012345678, got {dut.Q.value}"

    # Test 5: Check flush behavior
    dut.enable.value = 1
    dut.flush.value = 1
    dut.D.value = 0xDEADBEEFDEADBEEFDEADBEEF
    await RisingEdge(dut.clk)
    await Timer(1, units="ns") 
    assert dut.Q.value == 0, f"Flush failed: expected 0, got {dut.Q.value}"

    # Test 6: Reset again and verify
    await reset_pipeline()
    assert dut.Q.value == 0, f"Reset failed: expected 0, got {dut.Q.value}"

    # Test 7: Random data propagation
    for _ in range(100):
        data = random.randint(0, 2**96 - 1)  # Random 96-bit value
        dut.enable.value = 1
        dut.flush.value = 0
        dut.D.value = data
        await RisingEdge(dut.clk)
        await Timer(1, units="ns") 
        assert dut.Q.value == data, f"Data propagation failed: expected {data}, got {dut.Q.value}"

    # If all assertions pass, the test is successful
    raise TestSuccess("All pipe test cases passed!")
