import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux2x1(dut):
    """Test the 2x1 multiplexer."""
    
    # Test with multiple random values
    for _ in range(10):
        in1 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        in2 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        s = random.randint(0, 1)  # Random selection bit
        
        # Apply inputs to DUT
        dut.in1.value = in1
        dut.in2.value = in2
        dut.s.value = s
        
        await Timer(2, units="ns")
        
        # Check output
        expected_out = in1 if s == 0 else in2
        assert dut.out.value == expected_out, f"Mismatch: s={s}, in1={in1}, in2={in2}, expected={expected_out}, got={dut.out.value}"
    
    cocotb.log.info("MUX 2x1 test completed successfully.")
