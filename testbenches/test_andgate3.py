import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestSuccess

@cocotb.test()
async def test_and3gate(dut):
    """Testbench for 3-input AND gate."""

    # function to set inputs and check the output
    async def test_case(in1, in2, in3, expected_out):
        dut.in1.value = in1
        dut.in2.value = in2
        dut.in3.value = in3
        await Timer(1, units="ns")  # Wait for signals to propagate
        assert dut.out.value == expected_out, (
            f"Test failed: inputs={in1},{in2},{in3}, "
            f"expected={expected_out}, got={dut.out.value}"
        )

    # Test all possible input combinations (2^3 = 8 cases)
    test_cases = [
        # in1, in2, in3, expected_out
        (0, 0, 0, 0),
        (0, 0, 1, 0),
        (0, 1, 0, 0),
        (0, 1, 1, 0),
        (1, 0, 0, 0),
        (1, 0, 1, 0),
        (1, 1, 0, 0),
        (1, 1, 1, 1),
    ]

    # Run all test cases
    for case in test_cases:
        await test_case(*case)

    # If all assertions pass, the test is successful
    raise TestSuccess("All AND3Gate test cases passed!")