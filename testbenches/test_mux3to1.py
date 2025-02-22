import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux3to1(dut):
    """Test the 3x1 multiplexer."""
    
    # Test with multiple random values
    for _ in range(100000):
        in1 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        in2 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        in3 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        s = random.randint(0, 3)  # Random selection (00, 01, 10, 11)
        
        # Apply inputs to DUT
        dut.in1.value = in1
        dut.in2.value = in2
        dut.in3.value = in3
        dut.s.value = s
        
        await Timer(2, units="ns")
        
        # Check output
        if s == 0:
            expected_out = in1
        elif s == 1:
            expected_out = in2
        elif s == 2:
            expected_out = in3
        else:
            expected_out = 0  # Default case for s=3
        
        assert dut.out.value == expected_out, f"Mismatch: s={s}, in1={in1}, in2={in2}, in3={in3}, expected={expected_out}, got={dut.out.value}"
    
    cocotb.log.info("MUX 3x1 test completed successfully.")
