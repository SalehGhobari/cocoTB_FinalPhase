import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestSuccess
import random

# Define ALU operations based on the Verilog parameters
ALU_OPS = {
    "_ADD": 0b0000,
    "_SUB": 0b0001,
    "_AND": 0b0010,
    "_OR": 0b0011,
    "_SLT": 0b0100,
    "_SGT": 0b0101,
    "_NOR": 0b0110,
    "_XOR": 0b0111,
    "_SLL": 0b1000,
    "_SRL": 0b1001,
}

@cocotb.test()
async def test_alu_randomized(dut):
    """Randomized testbench for ALU module."""

    # function to perform ALU operations
    async def perform_operation(op, a, b, shamt=0):
        dut.operand1.value = a
        dut.operand2.value = b
        dut.shamt.value = shamt
        dut.opSel.value = ALU_OPS[op]
        await Timer(1, units="ns")

    # Number of random test cases per operation
    num_random_tests = 100000

    # Test ADD operation
    for _ in range(num_random_tests):
        a = random.randint(0, 2**32 - 1)
        b = random.randint(0, 2**32 - 1)
        await perform_operation("_ADD", a, b)
        expected_result = (a + b) & 0xFFFFFFFF  # Mask to 32 bits
        assert dut.result.value == expected_result, f"ADD failed: a={a}, b={b}, expected={expected_result}, got={dut.result.value}"

    # Test SUB operation
    for _ in range(num_random_tests):
        a = random.randint(0, 2**32 - 1)
        b = random.randint(0, 2**32 - 1)
        await perform_operation("_SUB", a, b)
        expected_result = (a - b) & 0xFFFFFFFF  # Mask to 32 bits
        assert dut.result.value == expected_result, f"SUB failed: a={a}, b={b}, expected={expected_result}, got={dut.result.value}"

    # Test AND operation
    for _ in range(num_random_tests):
        a = random.randint(0, 2**32 - 1)
        b = random.randint(0, 2**32 - 1)
        await perform_operation("_AND", a, b)
        expected_result = a & b
        assert dut.result.value == expected_result, f"AND failed: a={a}, b={b}, expected={expected_result}, got={dut.result.value}"

    # Test OR operation
    for _ in range(num_random_tests):
        a = random.randint(0, 2**32 - 1)
        b = random.randint(0, 2**32 - 1)
        await perform_operation("_OR", a, b)
        expected_result = a | b
        assert dut.result.value == expected_result, f"OR failed: a={a}, b={b}, expected={expected_result}, got={dut.result.value}"

    # Test NOR operation
    for _ in range(num_random_tests):
        a = random.randint(0, 2**32 - 1)
        b = random.randint(0, 2**32 - 1)
        await perform_operation("_NOR", a, b)
        expected_result = ~(a | b) & 0xFFFFFFFF  # Mask to 32 bits
        assert dut.result.value == expected_result, f"NOR failed: a={a}, b={b}, expected={expected_result}, got={dut.result.value}"

    # Test XOR operation
    for _ in range(num_random_tests):
        a = random.randint(0, 2**32 - 1)
        b = random.randint(0, 2**32 - 1)
        await perform_operation("_XOR", a, b)
        expected_result = a ^ b
        assert dut.result.value == expected_result, f"XOR failed: a={a}, b={b}, expected={expected_result}, got={dut.result.value}"

    # Test SLT operation (signed less than)
    for _ in range(num_random_tests):
        a = random.randint(-2**31, 2**31 - 1)  # Signed 32-bit range
        b = random.randint(-2**31, 2**31 - 1)
        await perform_operation("_SLT", a, b)
        expected_result = 1 if a < b else 0
        assert dut.result.value == expected_result, f"SLT failed: a={a}, b={b}, expected={expected_result}, got={dut.result.value}"

    # Test SGT operation (signed greater than)
    for _ in range(num_random_tests):
        a = random.randint(-2**31, 2**31 - 1)  # Signed 32-bit range
        b = random.randint(-2**31, 2**31 - 1)
        await perform_operation("_SGT", a, b)
        expected_result = 1 if a > b else 0
        assert dut.result.value == expected_result, f"SGT failed: a={a}, b={b}, expected={expected_result}, got={dut.result.value}"

    # Test SLL operation (shift left logical)
    for _ in range(num_random_tests):
        a = random.randint(0, 2**32 - 1)
        shamt = random.randint(0, 31)  # Shift amount between 0 and 31
        await perform_operation("_SLL", 0, a, shamt)
        expected_result = (a << shamt) & 0xFFFFFFFF  # Mask to 32 bits
        assert dut.result.value == expected_result, f"SLL failed: a={a}, shamt={shamt}, expected={expected_result}, got={dut.result.value}"

    # Test SRL operation (shift right logical)
    for _ in range(num_random_tests):
        a = random.randint(0, 2**32 - 1)
        shamt = random.randint(0, 31)  # Shift amount between 0 and 31
        await perform_operation("_SRL", 0, a, shamt)
        expected_result = (a >> shamt) & 0xFFFFFFFF  # Mask to 32 bits
        assert dut.result.value == expected_result, f"SRL failed: a={a}, shamt={shamt}, expected={expected_result}, got={dut.result.value}"


    raise TestSuccess("All ALU operations passed!")
