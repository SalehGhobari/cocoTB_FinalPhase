import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestSuccess
import random

# Define opCode and funct parameters based on the Verilog module
OPCODES = {
    "_RType": 0x00,
    "_addi": 0x08,
    "_lw": 0x23,
    "_sw": 0x2B,
    "_beq": 0x04,
    "_bne": 0x05,
    "_jal": 0x03,
    "_ori": 0x0D,
    "_xori": 0x16,
    "_andi": 0x0C,
    "_slti": 0x0A,
    "_j": 0x02,
}

FUNCTS = {
    "_add_": 0x20,
    "_sub_": 0x22,
    "_and_": 0x24,
    "_or_": 0x25,
    "_slt_": 0x2A,
    "_sgt_": 0x14,
    "_nor_": 0x27,
    "_xor_": 0x15,
    "_sll_": 0x00,
    "_srl_": 0x02,
    "_jr_": 0x08,
}

# Define expected control signals for each opCode and funct
EXPECTED_SIGNALS = {
    # R-Type instructions
    (OPCODES["_RType"], FUNCTS["_add_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0000},
    (OPCODES["_RType"], FUNCTS["_sub_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0001},
    (OPCODES["_RType"], FUNCTS["_and_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0010},
    (OPCODES["_RType"], FUNCTS["_or_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                          "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0011},
    (OPCODES["_RType"], FUNCTS["_slt_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0100},
    (OPCODES["_RType"], FUNCTS["_sgt_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0101},
    (OPCODES["_RType"], FUNCTS["_nor_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0110},
    (OPCODES["_RType"], FUNCTS["_xor_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0111},
    (OPCODES["_RType"], FUNCTS["_sll_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b1000},
    (OPCODES["_RType"], FUNCTS["_srl_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b1001},
    (OPCODES["_RType"], FUNCTS["_jr_"]): {"RegDst": 0b01, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                                          "MemWriteEn": 0, "RegWriteEn": 0, "ALUSrc": 0, "Jump": 0, "PcSrc": 1, "ALUOp": 0b0000},

    # I-Type and J-Type instructions
    (OPCODES["_addi"], 0): {"RegDst": 0b00, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                            "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 1, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0000},
    (OPCODES["_lw"], 0): {"RegDst": 0b00, "Branch": 0, "MemReadEn": 1, "MemtoReg": 0b01,
                          "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 1, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0000},
    (OPCODES["_sw"], 0): {"RegDst": 0b00, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                          "MemWriteEn": 1, "RegWriteEn": 0, "ALUSrc": 1, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0000},
    (OPCODES["_beq"], 0): {"RegDst": 0b00, "Branch": 1, "MemReadEn": 0, "MemtoReg": 0b00,
                           "MemWriteEn": 0, "RegWriteEn": 0, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0001},
    (OPCODES["_bne"], 0): {"RegDst": 0b00, "Branch": 1, "MemReadEn": 0, "MemtoReg": 0b00,
                           "MemWriteEn": 0, "RegWriteEn": 0, "ALUSrc": 0, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0001},
    (OPCODES["_jal"], 0): {"RegDst": 0b10, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b10,
                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 0, "Jump": 1, "PcSrc": 1, "ALUOp": 0b0000},
    (OPCODES["_ori"], 0): {"RegDst": 0b00, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                           "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 1, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0011},
    (OPCODES["_xori"], 0): {"RegDst": 0b00, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                            "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 1, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0111},
    (OPCODES["_andi"], 0): {"RegDst": 0b00, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                            "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 1, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0010},
    (OPCODES["_slti"], 0): {"RegDst": 0b00, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b00,
                            "MemWriteEn": 0, "RegWriteEn": 1, "ALUSrc": 1, "Jump": 0, "PcSrc": 0, "ALUOp": 0b0100},
    (OPCODES["_j"], 0): {"RegDst": 0b10, "Branch": 0, "MemReadEn": 0, "MemtoReg": 0b10,
                         "MemWriteEn": 0, "RegWriteEn": 0, "ALUSrc": 0, "Jump": 1, "PcSrc": 1, "ALUOp": 0b0000},
}

@cocotb.test()
async def test_control_unit_randomized(dut):
    """Randomized testbench for controlUnit module."""

    # Helper function to set inputs and check outputs
    async def test_case(opCode, funct, expected_signals):
        dut.opCode.value = opCode
        dut.funct.value = funct
        await Timer(1, units="ns")  # Wait for signals to propagate

        # Compare each output signal with the expected value
        for signal, expected_value in expected_signals.items():
            actual_value = getattr(dut, signal).value
            assert actual_value == expected_value, (
                f"Signal {signal} failed: opCode={hex(opCode)}, funct={hex(funct)}, "
                f"expected={expected_value}, got={actual_value}"
            )

    # Number of random test cases
    num_random_tests = 100000

    # List of (opCode, funct) pairs
    test_cases = list(EXPECTED_SIGNALS.keys())

    # Run random test cases
    for _ in range(num_random_tests):
        opCode, funct = random.choice(test_cases)
        expected_signals = EXPECTED_SIGNALS[(opCode, funct)]
        await test_case(opCode, funct, expected_signals)


    raise TestSuccess("All controlUnit test cases passed!")
