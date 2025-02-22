import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.binary import BinaryValue
import random

async def reset_regfile(dut):
    """Helper function to reset the register file"""
    dut.rst.value = 1
    await Timer(1, units='ns')
    dut.rst.value = 0
    await Timer(1, units='ns')
    dut.rst.value = 1
    await Timer(1, units='ns')

@cocotb.test()
async def test_reset(dut):
    """Test register file reset functionality"""
    
    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset register file
    await reset_regfile(dut)
    
    # Check if all registers are zero
    for i in range(32):
        dut.readRegister1.value = i
        await Timer(1, units='ns')
        assert dut.readData1.value == 0, f"Register {i} not zero after reset"

@cocotb.test()
async def test_single_write(dut):
    """Test single port write functionality"""
    
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_regfile(dut)
    
    # Write to a single register
    test_data = 0xDEADBEEF
    test_reg = 5
    
    # Initialize write control signals
    dut.we1.value = 1
    dut.we2.value = 0
    dut.writeRegister1.value = test_reg
    dut.writeRegister2.value = 0  # Set to different register
    dut.writeData1.value = test_data
    
    # Wait for negative edge where write occurs
    await FallingEdge(dut.clk)
    # Wait a bit after the negedge
    await Timer(2, units='ns')
    
    # Set up read
    dut.readRegister1.value = test_reg
    await Timer(2, units='ns')
    
    assert dut.readData1.value == test_data, f"Written data doesn't match read data. Expected {test_data:X}, got {dut.readData1.value:X}"

@cocotb.test()
async def test_dual_write(dut):
    """Test dual port write functionality"""
    
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_regfile(dut)
    
    # Write to two different registers
    test_data1 = 0xDEADBEEF
    test_data2 = 0xCAFEBABE
    test_reg1 = 5
    test_reg2 = 10
    
    dut.we1.value = 1
    dut.we2.value = 1
    dut.writeRegister1.value = test_reg1
    dut.writeRegister2.value = test_reg2
    dut.writeData1.value = test_data1
    dut.writeData2.value = test_data2
    
    await FallingEdge(dut.clk)
    await Timer(2, units='ns')
    
    # Read and verify both registers
    dut.readRegister1.value = test_reg1
    dut.readRegister2.value = test_reg2
    await Timer(2, units='ns')
    
    assert dut.readData1.value == test_data1, f"First write failed. Expected {test_data1:X}, got {dut.readData1.value:X}"
    assert dut.readData2.value == test_data2, f"Second write failed. Expected {test_data2:X}, got {dut.readData2.value:X}"

@cocotb.test()
async def test_write_zero_register(dut):
    """Test writing to register 0 (should remain 0)"""
    
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_regfile(dut)
    
    # Try to write to register 0
    dut.we1.value = 1
    dut.writeRegister1.value = 0
    dut.writeData1.value = 0xDEADBEEF
    
    await FallingEdge(dut.clk)
    await Timer(2, units='ns')
    
    # Verify register 0 remains 0
    dut.readRegister1.value = 0
    await Timer(2, units='ns')
    
    assert dut.readData1.value == 0, "Register 0 was modified"

@cocotb.test()
async def test_four_port_read(dut):
    """Test all four read ports simultaneously"""
    
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_regfile(dut)
    
    # Write test data to four registers
    test_values = {
        5: 0xDEADBEEF,
        10: 0xCAFEBABE,
        15: 0x12345678,
        20: 0x87654321
    }
    
    # Initialize write control signals
    dut.we1.value = 0
    dut.we2.value = 0
    
    # Write the test values using both write ports to speed up the process
    regs = list(test_values.items())
    for i in range(0, len(regs), 2):
        # Clear previous write enables
        dut.we1.value = 0
        dut.we2.value = 0
        await RisingEdge(dut.clk)
        
        # Setup first write port
        dut.we1.value = 1
        dut.writeRegister1.value = regs[i][0]
        dut.writeData1.value = regs[i][1]
        
        # Setup second write port if there's a second value to write
        if i + 1 < len(regs):
            dut.we2.value = 1
            dut.writeRegister2.value = regs[i+1][0]
            dut.writeData2.value = regs[i+1][1]
        
        # Wait for write to complete
        await FallingEdge(dut.clk)
        await Timer(2, units='ns')
    
    # Clear write enables
    dut.we1.value = 0
    dut.we2.value = 0
    
    # Wait an extra cycle to ensure writes are complete
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    
    # Setup all read ports
    dut.readRegister1.value = 5
    dut.readRegister2.value = 10
    dut.readRegister3.value = 15
    dut.readRegister4.value = 20
    
    # Wait for reads to propagate
    await Timer(5, units='ns')
    
    # Verify each read port individually with detailed error messages
    try:
        assert dut.readData1.value == test_values[5], \
            f"Read port 1 failed. Expected 0x{test_values[5]:08X}, got 0x{int(dut.readData1.value):08X}"
    except AssertionError as e:
        print(f"Port 1 read value: 0x{int(dut.readData1.value):08X}")
        raise e

    try:
        assert dut.readData2.value == test_values[10], \
            f"Read port 2 failed. Expected 0x{test_values[10]:08X}, got 0x{int(dut.readData2.value):08X}"
    except AssertionError as e:
        print(f"Port 2 read value: 0x{int(dut.readData2.value):08X}")
        raise e

    try:
        assert dut.readData3.value == test_values[15], \
            f"Read port 3 failed. Expected 0x{test_values[15]:08X}, got 0x{int(dut.readData3.value):08X}"
    except AssertionError as e:
        print(f"Port 3 read value: 0x{int(dut.readData3.value):08X}")
        raise e

    try:
        assert dut.readData4.value == test_values[20], \
            f"Read port 4 failed. Expected 0x{test_values[20]:08X}, got 0x{int(dut.readData4.value):08X}"
    except AssertionError as e:
        print(f"Port 4 read value: 0x{int(dut.readData4.value):08X}")
        raise e 
@cocotb.test()
async def test_write_conflict(dut):
    """Test write conflict resolution (same register, different ports)"""
    
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset_regfile(dut)
    
    test_reg = 5
    test_data1 = 0xDEADBEEF
    test_data2 = 0xCAFEBABE
    
    # Try to write to same register from both ports
    dut.we1.value = 1
    dut.we2.value = 1
    dut.writeRegister1.value = test_reg
    dut.writeRegister2.value = test_reg
    dut.writeData1.value = test_data1
    dut.writeData2.value = test_data2
    
    await FallingEdge(dut.clk)
    await Timer(2, units='ns')
    
    # Read and verify (should have test_data2 as per implementation)
    dut.readRegister1.value = test_reg
    await Timer(2, units='ns')
    
    assert dut.readData1.value == test_data2, f"Write conflict not resolved correctly. Expected {test_data2:X}, got {dut.readData1.value:X}"