import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux5to1(dut):
    """Test the 5x1 multiplexer."""
    
    # Test with multiple random values
    for _ in range(100):
        in1 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        in2 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        in3 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        in4 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        in5 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        s = random.randint(0, 7)  # Random selection (000 to 111)
        
        # Apply inputs to DUT
        dut.in1.value = in1
        dut.in2.value = in2
        dut.in3.value = in3
        dut.in4.value = in4
        dut.in5.value = in5
        dut.s.value = s
        
        await Timer(2, units="ns")  # Wait for a short time for propagation
        
        # Check output
        if s == 0:
            expected_out = in1
        elif s == 1:
            expected_out = in2
        elif s == 2:
            expected_out = in3
        elif s == 3:
            expected_out = in4
        elif s == 4:
            expected_out = in5
        else:
            expected_out = 0  # Default case for s=5,6,7
        
        assert dut.out.value == expected_out, f"Mismatch: s={s}, in1={in1}, in2={in2}, in3={in3}, in4={in4}, in5={in5}, expected={expected_out}, got={dut.out.value}"
    
    cocotb.log.info("MUX 5x1 test completed successfully.")
