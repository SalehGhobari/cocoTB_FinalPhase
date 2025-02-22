import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
import random

@cocotb.test()
async def test_hazard_detection_unit(dut):
    """Test Hazard Detection Unit"""

    # function to set inputs and wait for a small delay
    async def set_inputs(takenBranch1, takenBranch2, pcSrc1, pcSrc2, memReadE1, memReadE2,
                         branch1, branch2, predictionE1, predictionE2, writeRegisterE1, writeRegisterE2,
                         rsD1, rtD1, rsD2, rtD2):
        dut.takenBranch1.value = takenBranch1
        dut.takenBranch2.value = takenBranch2
        dut.pcSrc1.value = pcSrc1
        dut.pcSrc2.value = pcSrc2
        dut.memReadE1.value = memReadE1
        dut.memReadE2.value = memReadE2
        dut.branch1.value = branch1
        dut.branch2.value = branch2
        dut.predictionE1.value = predictionE1
        dut.predictionE2.value = predictionE2
        dut.writeRegisterE1.value = writeRegisterE1
        dut.writeRegisterE2.value = writeRegisterE2
        dut.rsD1.value = rsD1
        dut.rtD1.value = rtD1
        dut.rsD2.value = rsD2
        dut.rtD2.value = rtD2
        await Timer(1, units="ns")

    # Test 1: No hazards, no branches
    await set_inputs(
        takenBranch1=0, takenBranch2=0, pcSrc1=0, pcSrc2=0,
        memReadE1=0, memReadE2=0, branch1=0, branch2=0,
        predictionE1=0, predictionE2=0, writeRegisterE1=0, writeRegisterE2=0,
        rsD1=0, rtD1=0, rsD2=0, rtD2=0
    )
    assert dut.Stall11.value == 0, "Stall11 should be 0"
    assert dut.Stall21.value == 0, "Stall21 should be 0"
    assert dut.Stall12.value == 0, "Stall12 should be 0"
    assert dut.Stall22.value == 0, "Stall22 should be 0"
    assert dut.FlushIFID1.value == 0, "FlushIFID1 should be 0"
    assert dut.FlushEX.value == 0, "FlushEX should be 0"
    assert dut.FlushMEM2.value == 0, "FlushMEM2 should be 0"
    assert dut.CPCSignal1.value == 0, "CPCSignal1 should be 0"
    assert dut.CPCSignal2.value == 0, "CPCSignal2 should be 0"

    # Test 2: Branch misprediction for instruction 1
    await set_inputs(
        takenBranch1=1, takenBranch2=0, pcSrc1=0, pcSrc2=0,
        memReadE1=0, memReadE2=0, branch1=1, branch2=0,
        predictionE1=0, predictionE2=0, writeRegisterE1=0, writeRegisterE2=0,
        rsD1=0, rtD1=0, rsD2=0, rtD2=0
    )
    assert dut.FlushIFID1.value == 1, "FlushIFID1 should be 1"
    assert dut.FlushEX.value == 1, "FlushEX should be 1"
    assert dut.FlushMEM2.value == 1, "FlushMEM2 should be 1"
    assert dut.CPCSignal1.value == 1, "CPCSignal1 should be 1"
    assert dut.CPCSignal2.value == 0, "CPCSignal2 should be 0"

    # Test 3: Data hazard for instruction 1 (memReadE1 and rsD1 match)
    await set_inputs(
        takenBranch1=0, takenBranch2=0, pcSrc1=0, pcSrc2=0,
        memReadE1=1, memReadE2=0, branch1=0, branch2=0,
        predictionE1=0, predictionE2=0, writeRegisterE1=5, writeRegisterE2=0,
        rsD1=5, rtD1=0, rsD2=0, rtD2=0
    )
    assert dut.Stall11.value == 1, "Stall11 should be 1"
    assert dut.Stall21.value == 0, "Stall21 should be 0"
    assert dut.Stall12.value == 0, "Stall12 should be 0"
    assert dut.Stall22.value == 0, "Stall22 should be 0"

    # Test 4: Data hazard for instruction 2 (memReadE2 and rsD2 match)
    await set_inputs(
        takenBranch1=0, takenBranch2=0, pcSrc1=0, pcSrc2=0,
        memReadE1=0, memReadE2=1, branch1=0, branch2=0,
        predictionE1=0, predictionE2=0, writeRegisterE1=0, writeRegisterE2=6,
        rsD1=0, rtD1=0, rsD2=6, rtD2=0
    )
    assert dut.Stall11.value == 0, "Stall11 should be 0"
    assert dut.Stall21.value == 0, "Stall21 should be 0"
    assert dut.Stall12.value == 0, "Stall12 should be 0"
    assert dut.Stall22.value == 1, "Stall22 should be 1"

    # Test 5: Branch misprediction for instruction 2
    await set_inputs(
        takenBranch1=0, takenBranch2=1, pcSrc1=0, pcSrc2=0,
        memReadE1=0, memReadE2=0, branch1=0, branch2=1,
        predictionE1=0, predictionE2=0, writeRegisterE1=0, writeRegisterE2=0,
        rsD1=0, rtD1=0, rsD2=0, rtD2=0
    )
    assert dut.FlushIFID1.value == 1, "FlushIFID1 should be 1"
    assert dut.FlushEX.value == 1, "FlushEX should be 1"
    assert dut.FlushMEM2.value == 0, "FlushMEM2 should be 0"
    assert dut.CPCSignal1.value == 0, "CPCSignal1 should be 0"
    assert dut.CPCSignal2.value == 1, "CPCSignal2 should be 1"

    # Test 6: Multiple hazards (branch misprediction and data hazard)
    await set_inputs(
        takenBranch1=1, takenBranch2=0, pcSrc1=0, pcSrc2=0,
        memReadE1=1, memReadE2=0, branch1=1, branch2=0,
        predictionE1=0, predictionE2=0, writeRegisterE1=5, writeRegisterE2=0,
        rsD1=5, rtD1=0, rsD2=0, rtD2=0
    )
    assert dut.Stall11.value == 1, "Stall11 should be 1"
    assert dut.FlushIFID1.value == 1, "FlushIFID1 should be 1"
    assert dut.FlushEX.value == 1, "FlushEX should be 1"
    assert dut.FlushMEM2.value == 1, "FlushMEM2 should be 1"
    assert dut.CPCSignal1.value == 1, "CPCSignal1 should be 1"

    # Randomized Inputs Test
    for _ in range(10000    ):
        takenBranch1 = random.randint(0, 1)
        takenBranch2 = random.randint(0, 1)
        pcSrc1 = random.randint(0, 1)
        pcSrc2 = random.randint(0, 1)
        memReadE1 = random.randint(0, 1)
        memReadE2 = random.randint(0, 1)
        branch1 = random.randint(0, 1)
        branch2 = random.randint(0, 1)
        predictionE1 = random.randint(0, 1)
        predictionE2 = random.randint(0, 1)
        writeRegisterE1 = random.randint(0, 31)
        writeRegisterE2 = random.randint(0, 31)
        rsD1 = random.randint(0, 31)
        rtD1 = random.randint(0, 31)
        rsD2 = random.randint(0, 31)
        rtD2 = random.randint(0, 31)

        await set_inputs(
            takenBranch1, takenBranch2, pcSrc1, pcSrc2, memReadE1, memReadE2,
            branch1, branch2, predictionE1, predictionE2, writeRegisterE1, writeRegisterE2,
            rsD1, rtD1, rsD2, rtD2
        )

        # Verify outputs based on inputs
        if (memReadE1 and ((writeRegisterE1 == rsD1 or writeRegisterE1 == rtD1) and writeRegisterE1 != 0)):
            assert dut.Stall11.value == 1, f"Stall11 should be 1 for inputs: {locals()}"
        if (memReadE2 and ((writeRegisterE2 == rsD1 or writeRegisterE2 == rtD1) and writeRegisterE2 != 0) and not memReadE1):
            assert dut.Stall21.value == 1, f"Stall21 should be 1 for inputs: {locals()}"
        if (memReadE1 and ((writeRegisterE1 == rsD2 or writeRegisterE1 == rtD2) and writeRegisterE1 != 0)):
            assert dut.Stall12.value == 1, f"Stall12 should be 1 for inputs: {locals()}"
        if (memReadE2 and ((writeRegisterE2 == rsD2 or writeRegisterE2 == rtD2) and writeRegisterE2 != 0) and not memReadE1):
            assert dut.Stall22.value == 1, f"Stall22 should be 1 for inputs: {locals()}"

        if (branch1 and (predictionE1 != takenBranch1)) or (branch2 and (predictionE2 != takenBranch2)):
            assert dut.FlushIFID1.value == 1, f"FlushIFID1 should be 1 for inputs: {locals()}"
            assert dut.FlushEX.value == 1, f"FlushEX should be 1 for inputs: {locals()}"
            if (branch1 and (predictionE1 != takenBranch1)):
                assert dut.FlushMEM2.value == 1, f"FlushMEM2 should be 1 for inputs: {locals()}"
            else:
                assert dut.FlushMEM2.value == 0, f"FlushMEM2 should be 0 for inputs: {locals()}"

        if (branch1 and (predictionE1 != takenBranch1)):
            assert dut.CPCSignal1.value == 1, f"CPCSignal1 should be 1 for inputs: {locals()}"
        if (branch2 and (predictionE2 != takenBranch2)):
            assert dut.CPCSignal2.value == 1, f"CPCSignal2 should be 1 for inputs: {locals()}"

    print("All tests passed, including randomized inputs!")