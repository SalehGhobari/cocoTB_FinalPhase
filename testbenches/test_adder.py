import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_adder(dut):
    """Test the adder module with 10-bit inputs and 11-bit output"""
    dut._log.info("Starting adder test")

    
    input_size = 10
    output_size = 11

    # Test with 10 random input combinations
    for _ in range(10000):
        # Generate random inputs (10-bit values)
        in1 = random.randint(0, (1 << input_size) - 1)  # Max value = 1023
        in2 = random.randint(0, (1 << input_size) - 1)  # Max value = 1023
        
        # Assign input values to the DUT
        dut.in1.value = in1
        dut.in2.value = in2

        
        await Timer(10, units="ns")

        # Calculate expected output
        expected = in1 + in2

        # Get the output from the DUT and convert it to an integer
        actual = dut.out.value.integer  # Convert BinaryValue to integer

        # Ensure the result fits in the 11-bit range
        expected &= (1 << output_size) - 1  # Mask to 11-bit max value

        # Check if the output is correct
        assert actual == expected, f"Adder failed for {in1} + {in2}, got {actual}, expected {expected}"

    dut._log.info("Adder test completed successfully")
