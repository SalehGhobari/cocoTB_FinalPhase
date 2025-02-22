import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestSuccess, TestFailure
import random

@cocotb.test()
async def test_signextender(dut):
    """Test signextender module"""

    def check_output(input_val, expected_output):
        if int(dut.out.value) != expected_output:
            raise TestFailure(f"Error: Input = {input_val:04x}, Expected Output = {expected_output:08x}, Actual Output = {int(dut.out.value):08x}")

    # Test cases
    test_cases = [
        (0x0000, 0x00000000), 
        (0x7FFF, 0x00007FFF),
        (0x8000, 0xFFFF8000),
        (0xFFFF, 0xFFFFFFFF),
    ]

    # Add some random test cases
    for _ in range(1000):
        input_val = random.randint(0, 0xFFFF)
        expected_output = (input_val & 0x8000) and (0xFFFF0000 | input_val) or input_val
        test_cases.append((input_val, expected_output))

    # Apply test cases
    for input_val, expected_output in test_cases:
        dut.in1.value = input_val
        await Timer(1, units="ns")
        check_output(input_val, expected_output)

    # If all tests pass
    raise TestSuccess("All test cases passed!")