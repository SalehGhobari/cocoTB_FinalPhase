import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestSuccess

@cocotb.test()
async def test_orgate4(dut):
    """Testbench for 4-input OR gate."""

    # function to set inputs and check the output
    async def test_case(in1, in2, in3, in4, expected_out):
        dut.in1.value = in1
        dut.in2.value = in2
        dut.in3.value = in3
        dut.in4.value = in4
        await Timer(1, units="ns")  # Wait for signals to propagate
        assert dut.out.value == expected_out, (
            f"Test failed: inputs={in1},{in2},{in3},{in4}, "
            f"expected={expected_out}, got={dut.out.value}"
        )

    # Test all possible input combinations (2^4 = 16 cases)
    test_cases = [
        # in1, in2, in3, in4, expected_out
        (0, 0, 0, 0, 0),
        (0, 0, 0, 1, 1),
        (0, 0, 1, 0, 1),
        (0, 0, 1, 1, 1),
        (0, 1, 0, 0, 1),
        (0, 1, 0, 1, 1),
        (0, 1, 1, 0, 1),
        (0, 1, 1, 1, 1),
        (1, 0, 0, 0, 1),
        (1, 0, 0, 1, 1),
        (1, 0, 1, 0, 1),
        (1, 0, 1, 1, 1),
        (1, 1, 0, 0, 1),
        (1, 1, 0, 1, 1),
        (1, 1, 1, 0, 1),
        (1, 1, 1, 1, 1),
    ]

    # Run all test cases
    for case in test_cases:
        await test_case(*case)

    raise TestSuccess("All ORGate4 test cases passed!")