import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestSuccess

@cocotb.test()
async def test_orgate2(dut):
    """Testbench for 2-input OR gate."""

    # function to set inputs and check the output
    async def test_case(in1, in2, expected_out):
        dut.in1.value = in1
        dut.in2.value = in2
        await Timer(1, units='ns')
        assert dut.out.value == expected_out, (
            f"Test failed: inputs={in1},{in2}, "
            f"expected={expected_out}, got={dut.out.value}"
        )

    # Test all possible input combinations (2^2 = 4 cases)
    test_cases = [
        # in1, in2, expected_out
        (0, 0, 0),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 1),
    ]

    # Run all test cases
    for case in test_cases:
        await test_case(*case)


    raise TestSuccess("All ORGate2 test cases passed!")
