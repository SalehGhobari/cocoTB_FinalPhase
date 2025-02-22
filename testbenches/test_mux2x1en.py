import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue
import random

async def check_mux_output(dut, in1, in2, select, enable, expected):
    """Helper function to check mux output for given inputs"""
    dut.in1.value = in1
    dut.in2.value = in2
    dut.s.value = select
    dut.en.value = enable
    
    await Timer(2, units='ns')
    
    if enable:
        assert dut.out.value == expected, \
            f"Mux output wrong. Got: {dut.out.value}, Expected: {expected} for in1={in1}, in2={in2}, s={select}, en={enable}"
    else:
        # Output should be high impedance/undefined when enable is 0
        assert dut.out.value.is_z, \
            f"Output should be high impedance when enable is 0, got {dut.out.value}"

@cocotb.test()
async def test_basic_operation(dut):
    """Test basic multiplexer operation with enable"""
    
    # Test all basic combinations with enable=1
    test_cases = [
        # in1,    in2,      s,  en, expected
        (0x0000,  0xFFFF,   0,  1,  0x0000),  # Select in1
        (0x0000,  0xFFFF,   1,  1,  0xFFFF),  # Select in2
        (0xAAAA,  0x5555,   0,  1,  0xAAAA),  # Select in1
        (0xAAAA,  0x5555,   1,  1,  0x5555),  # Select in2
    ]
    
    for in1, in2, s, en, expected in test_cases:
        await check_mux_output(dut, in1, in2, s, en, expected)

@cocotb.test()
async def test_enable_behavior(dut):
    """Test enable functionality"""

    # Capture initial output value (in case it's not zero)
    await Timer(2, units="ns")
    previous_out = dut.out.value.integer  # Read initial output

    # Test with enable=0 for various inputs
    test_cases = [
        (0x0000, 0xFFFF, 0, 0),
        (0x0000, 0xFFFF, 1, 0),
        (0xAAAA, 0x5555, 0, 0),
        (0xAAAA, 0x5555, 1, 0),
    ]

    for in1, in2, s, en in test_cases:
        # Set inputs
        dut.in1.value = in1
        dut.in2.value = in2
        dut.s.value = s
        dut.en.value = en

        await Timer(2, units="ns")

        if en == 0:
            # Output should hold previous value
            assert dut.out.value == previous_out, \
                f"Output should hold previous value {previous_out} when enable is 0, got {dut.out.value.integer}"
        else:
            # If enable is 1, update previous output value
            previous_out = dut.out.value.integer

    
    # Test with enable=1 to verify normal mux behavior
    test_cases_enabled = [
        # in1,    in2,      s,  en
        (0x0000,  0xFFFF,   0,  1),
        (0x0000,  0xFFFF,   1,  1),
        (0xAAAA,  0x5555,   0,  1),
        (0xAAAA,  0x5555,   1,  1),
    ]
    
    for in1, in2, s, en in test_cases_enabled:
        # Set inputs
        dut.in1.value = in1
        dut.in2.value = in2
        dut.s.value = s
        dut.en.value = en
        
        # Wait for signals to propagate
        await Timer(2, units='ns')
        
        if s == 0:
            # When s=0, output should be in1
            assert dut.out.value == in1, \
                f"Output should be {in1} when s=0 and en=1, got {dut.out.value}"
        else:
            # When s=1, output should be in2
            assert dut.out.value == in2, \
                f"Output should be {in2} when s=1 and en=1, got {dut.out.value}"
        
        # Update previous output value
        previous_out = dut.out.value

@cocotb.test()
async def test_random_values(dut):
    """Test multiplexer with random input values"""
    
    for _ in range(20):
        # Generate random 32-bit values
        in1 = random.randint(0, 0xFFFFFFFF)
        in2 = random.randint(0, 0xFFFFFFFF)
        select = random.randint(0, 1)
        enable = 1  # Keep enable active for random testing
        
        expected = in2 if select else in1
        
        await check_mux_output(dut, in1, in2, select, enable, expected)

@cocotb.test()
async def test_timing_behavior(dut):
    """Test multiplexer timing behavior with rapid input changes"""
    
    # Test rapid changes to all inputs
    for i in range(10):  # Run 10 quick changes
        in1 = random.randint(0, 0xFFFFFFFF)
        in2 = random.randint(0, 0xFFFFFFFF)
        select = i % 2
        enable = 1
        
        expected = in2 if select else in1
        
        await check_mux_output(dut, in1, in2, select, enable, expected)
        await Timer(1, units='ns')  # Quick timing between changes

@cocotb.test()
async def test_edge_cases(dut):
    """Test multiplexer edge cases"""
    
    test_cases = [
        # in1,         in2,         s,  en, expected
        (0x00000000,  0x00000000,  0,  1,  0x00000000),  # All zeros
        (0xFFFFFFFF,  0xFFFFFFFF,  1,  1,  0xFFFFFFFF),  # All ones
        (0xAAAAAAAA,  0x55555555,  0,  1,  0xAAAAAAAA),  # Alternating patterns
        (0x55555555,  0xAAAAAAAA,  1,  1,  0xAAAAAAAA),  # Alternating patterns
        (0x00000001,  0x80000000,  0,  1,  0x00000001),  # Single bits
        (0x80000000,  0x00000001,  1,  1,  0x00000001),  # Single bits
    ]
    
    for in1, in2, s, en, expected in test_cases:
        await check_mux_output(dut, in1, in2, s, en, expected)

# Optional: Add this to your conftest.py
def pytest_configure(config):
    config.option.tb_logs = True