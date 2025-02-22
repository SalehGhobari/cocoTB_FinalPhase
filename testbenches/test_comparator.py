import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestSuccess
import random

@cocotb.test()
async def test_comparator(dut):
    """Testbench for Comparator module with only random inputs."""

    # Define a helper function to set inputs and check the output
    async def test_case(a, b, expected_equal):
        dut.a.value = a
        dut.b.value = b
        await Timer(1, units="ns")  # Wait for signals to propagate
        assert dut.equal.value == expected_equal, (
            f"Test failed: a={a}, b={b}, "
            f"expected_equal={expected_equal}, got={dut.equal.value}"
        )

    # Random test cases
    num_random_tests = 200000  # Number of random test cases to generate
    for _ in range(num_random_tests):
        a = random.randint(-2**31, 2**31 - 1)  # Random 32-bit value for a
        b = random.randint(-2**31, 2**31 - 1)  # Random 32-bit value for b
        expected_equal = 1 if a == b else 0  # Expected output
        await test_case(a, b, expected_equal)


    raise TestSuccess("All Comparator test cases passed!")