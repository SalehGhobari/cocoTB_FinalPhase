import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestSuccess

@cocotb.test()
async def test_xnor_gate(dut):
    """Testbench for XNORGate module."""

    async def test_case(in1, in2, expected_out):
        dut.in1.value = in1
        dut.in2.value = in2
        await Timer(1, units="ns")
        assert dut.out.value == expected_out, (
            f"Test failed: in1={in1}, in2={in2}, expected={expected_out}, got={dut.out.value}"
        )

    # Test all possible input combinations (2^2 = 4 cases)
    test_cases = [
        # in1, in2, expected_out
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
        (1, 1, 1),
    ]

    # Run all test cases
    for case in test_cases:
        await test_case(*case)

    # If all assertions pass, the test is successful
    raise TestSuccess("All XNORGate test cases passed!")
