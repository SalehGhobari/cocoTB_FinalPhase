import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
import random

@cocotb.test()
async def test_forwarding_unit(dut):
    """Test Forwarding Unit"""

    # function to set inputs and wait for a small delay
    async def set_inputs(rsE1, rtE1, rsE2, rtE2, rsM2, rtM2, writeRegisterM1, writeRegisterM2, writeRegisterW1, writeRegisterW2,
                         regWriteM1, regWriteM2, regWriteW1, regWriteW2, branch2M):
        dut.rsE1.value = rsE1
        dut.rtE1.value = rtE1
        dut.rsE2.value = rsE2
        dut.rtE2.value = rtE2
        dut.rsM2.value = rsM2
        dut.rtM2.value = rtM2
        dut.writeRegisterM1.value = writeRegisterM1
        dut.writeRegisterM2.value = writeRegisterM2
        dut.writeRegisterW1.value = writeRegisterW1
        dut.writeRegisterW2.value = writeRegisterW2
        dut.regWriteM1.value = regWriteM1
        dut.regWriteM2.value = regWriteM2
        dut.regWriteW1.value = regWriteW1
        dut.regWriteW2.value = regWriteW2
        dut.branch2M.value = branch2M
        await Timer(1, units="ns")

    # Test 1: No forwarding (all inputs zero)
    await set_inputs(
        rsE1=0, rtE1=0, rsE2=0, rtE2=0, rsM2=0, rtM2=0,
        writeRegisterM1=0, writeRegisterM2=0, writeRegisterW1=0, writeRegisterW2=0,
        regWriteM1=0, regWriteM2=0, regWriteW1=0, regWriteW2=0, branch2M=0
    )
    assert dut.ForwardA1.value == 0, "ForwardA1 should be 0"
    assert dut.ForwardB1.value == 0, "ForwardB1 should be 0"
    assert dut.ForwardA2.value == 0, "ForwardA2 should be 0"
    assert dut.ForwardB2.value == 0, "ForwardB2 should be 0"
    assert dut.ForwardBranchA.value == 0, "ForwardBranchA should be 0"
    assert dut.ForwardBranchB.value == 0, "ForwardBranchB should be 0"

    # Test 2: Forward from Memory Stage 1 (M1) to Execute Stage 1 (E1)
    await set_inputs(
        rsE1=5, rtE1=0, rsE2=0, rtE2=0, rsM2=0, rtM2=0,
        writeRegisterM1=5, writeRegisterM2=0, writeRegisterW1=0, writeRegisterW2=0,
        regWriteM1=1, regWriteM2=0, regWriteW1=0, regWriteW2=0, branch2M=0
    )
    assert dut.ForwardA1.value == 1, "ForwardA1 should be 1 (M1 to E1)"
    assert dut.ForwardB1.value == 0, "ForwardB1 should be 0"

    # Test 3: Forward from Memory Stage 2 (M2) to Execute Stage 1 (E1)
    await set_inputs(
        rsE1=6, rtE1=0, rsE2=0, rtE2=0, rsM2=0, rtM2=0,
        writeRegisterM1=0, writeRegisterM2=6, writeRegisterW1=0, writeRegisterW2=0,
        regWriteM1=0, regWriteM2=1, regWriteW1=0, regWriteW2=0, branch2M=0
    )
    assert dut.ForwardA1.value == 2, "ForwardA1 should be 2 (M2 to E1)"
    assert dut.ForwardB1.value == 0, "ForwardB1 should be 0"

    # Test 4: Forward from Writeback Stage 1 (W1) to Execute Stage 1 (E1)
    await set_inputs(
        rsE1=7, rtE1=0, rsE2=0, rtE2=0, rsM2=0, rtM2=0,
        writeRegisterM1=0, writeRegisterM2=0, writeRegisterW1=7, writeRegisterW2=0,
        regWriteM1=0, regWriteM2=0, regWriteW1=1, regWriteW2=0, branch2M=0
    )
    assert dut.ForwardA1.value == 3, "ForwardA1 should be 3 (W1 to E1)"
    assert dut.ForwardB1.value == 0, "ForwardB1 should be 0"

    # Test 5: Forward from Writeback Stage 2 (W2) to Execute Stage 1 (E1)
    await set_inputs(
        rsE1=8, rtE1=0, rsE2=0, rtE2=0, rsM2=0, rtM2=0,
        writeRegisterM1=0, writeRegisterM2=0, writeRegisterW1=0, writeRegisterW2=8,
        regWriteM1=0, regWriteM2=0, regWriteW1=0, regWriteW2=1, branch2M=0
    )
    assert dut.ForwardA1.value == 4, "ForwardA1 should be 4 (W2 to E1)"
    assert dut.ForwardB1.value == 0, "ForwardB1 should be 0"

    # Test 6: Forward for branch instructions
    await set_inputs(
        rsE1=0, rtE1=0, rsE2=0, rtE2=0, rsM2=9, rtM2=0,
        writeRegisterM1=9, writeRegisterM2=0, writeRegisterW1=0, writeRegisterW2=0,
        regWriteM1=1, regWriteM2=0, regWriteW1=0, regWriteW2=0, branch2M=1
    )
    assert dut.ForwardBranchA.value == 1, "ForwardBranchA should be 1"
    assert dut.ForwardBranchB.value == 0, "ForwardBranchB should be 0"

    # Randomized Inputs Test
    for _ in range(100):
        rsE1 = random.randint(0, 31)
        rtE1 = random.randint(0, 31)
        rsE2 = random.randint(0, 31)
        rtE2 = random.randint(0, 31)
        rsM2 = random.randint(0, 31)
        rtM2 = random.randint(0, 31)
        writeRegisterM1 = random.randint(0, 31)
        writeRegisterM2 = random.randint(0, 31)
        writeRegisterW1 = random.randint(0, 31)
        writeRegisterW2 = random.randint(0, 31)
        regWriteM1 = random.randint(0, 1)
        regWriteM2 = random.randint(0, 1)
        regWriteW1 = random.randint(0, 1)
        regWriteW2 = random.randint(0, 1)
        branch2M = random.randint(0, 1)

        await set_inputs(
            rsE1, rtE1, rsE2, rtE2, rsM2, rtM2,
            writeRegisterM1, writeRegisterM2, writeRegisterW1, writeRegisterW2,
            regWriteM1, regWriteM2, regWriteW1, regWriteW2, branch2M
        )

        # Verify ForwardA1 logic
        if regWriteM1 and (writeRegisterM1 == rsE1) and (writeRegisterM1 != 0):
            assert dut.ForwardA1.value == 1, f"ForwardA1 should be 1 for inputs: {locals()}"
        elif regWriteM2 and (writeRegisterM2 == rsE1) and (writeRegisterM2 != 0) and (writeRegisterM1 != rsE1):
            assert dut.ForwardA1.value == 2, f"ForwardA1 should be 2 for inputs: {locals()}"
        elif regWriteW1 and (writeRegisterW1 == rsE1) and (writeRegisterW1 != 0) and \
             ((writeRegisterM1 != rsE1 or not regWriteM1) and (writeRegisterM2 != rsE1 or not regWriteM2)):
            assert dut.ForwardA1.value == 3, f"ForwardA1 should be 3 for inputs: {locals()}"
        elif regWriteW2 and (writeRegisterW2 == rsE1) and (writeRegisterW2 != 0) and \
             ((writeRegisterM1 != rsE1 or not regWriteM1) and (writeRegisterM2 != rsE1 or not regWriteM2)) and \
             (writeRegisterW1 != rsE1):
            assert dut.ForwardA1.value == 4, f"ForwardA1 should be 4 for inputs: {locals()}"
        else:
            assert dut.ForwardA1.value == 0, f"ForwardA1 should be 0 for inputs: {locals()}"

        # Verify ForwardBranchA logic
        if regWriteM1 and branch2M and (writeRegisterM1 == rsM2):
            assert dut.ForwardBranchA.value == 1, f"ForwardBranchA should be 1 for inputs: {locals()}"
        else:
            assert dut.ForwardBranchA.value == 0, f"ForwardBranchA should be 0 for inputs: {locals()}"

    print("All tests passed, including randomized inputs!")
