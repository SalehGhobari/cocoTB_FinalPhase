import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
import random

@cocotb.test()
async def test_pc_correction(dut):
    """Test PC Correction Logic"""

    #function to set inputs and wait for a small delay
    async def set_inputs(PredictionM1, PredictionM2, branch_taken1, branch_taken2, PCPlus1M, PCPlus2M, branchAdderResultM1, branchAdderResultM2):
        dut.PredictionM1.value = PredictionM1
        dut.PredictionM2.value = PredictionM2
        dut.branch_taken1.value = branch_taken1
        dut.branch_taken2.value = branch_taken2
        dut.PCPlus1M.value = PCPlus1M
        dut.PCPlus2M.value = PCPlus2M
        dut.branchAdderResultM1.value = branchAdderResultM1
        dut.branchAdderResultM2.value = branchAdderResultM2
        await Timer(1, units="ns")

    # Test 1: No branch misprediction (default behavior)
    await set_inputs(
        PredictionM1=0, PredictionM2=0, branch_taken1=0, branch_taken2=0,
        PCPlus1M=100, PCPlus2M=200, branchAdderResultM1=150, branchAdderResultM2=250
    )
    assert dut.CorrectedPC1.value == 100, "CorrectedPC1 should be 100"
    assert dut.CorrectedPC2.value == 200, "CorrectedPC2 should be 200"

    # Test 2: Branch 1 mispredicted (taken but not predicted)
    await set_inputs(
        PredictionM1=0, PredictionM2=0, branch_taken1=1, branch_taken2=0,
        PCPlus1M=100, PCPlus2M=200, branchAdderResultM1=150, branchAdderResultM2=250
    )
    assert dut.CorrectedPC1.value == 150, "CorrectedPC1 should be 150"
    assert dut.CorrectedPC2.value == 200, "CorrectedPC2 should be 200"

    # Test 3: Branch 2 mispredicted (taken but not predicted)
    await set_inputs(
        PredictionM1=0, PredictionM2=0, branch_taken1=0, branch_taken2=1,
        PCPlus1M=100, PCPlus2M=200, branchAdderResultM1=150, branchAdderResultM2=250
    )
    assert dut.CorrectedPC1.value == 100, "CorrectedPC1 should be 100"
    assert dut.CorrectedPC2.value == 250, "CorrectedPC2 should be 250"

    # Test 4: Both branches mispredicted (taken but not predicted)
    await set_inputs(
        PredictionM1=0, PredictionM2=0, branch_taken1=1, branch_taken2=1,
        PCPlus1M=100, PCPlus2M=200, branchAdderResultM1=150, branchAdderResultM2=250
    )
    assert dut.CorrectedPC1.value == 150, "CorrectedPC1 should be 150"
    assert dut.CorrectedPC2.value == 250, "CorrectedPC2 should be 250"

    # Test 5: Branch 1 predicted correctly (taken and predicted)
    await set_inputs(
        PredictionM1=1, PredictionM2=0, branch_taken1=1, branch_taken2=0,
        PCPlus1M=100, PCPlus2M=200, branchAdderResultM1=150, branchAdderResultM2=250
    )
    assert dut.CorrectedPC1.value == 100, "CorrectedPC1 should be 100"
    assert dut.CorrectedPC2.value == 200, "CorrectedPC2 should be 200"

    # Test 6: Branch 2 predicted correctly (taken and predicted)
    await set_inputs(
        PredictionM1=0, PredictionM2=1, branch_taken1=0, branch_taken2=1,
        PCPlus1M=100, PCPlus2M=200, branchAdderResultM1=150, branchAdderResultM2=250
    )
    assert dut.CorrectedPC1.value == 100, "CorrectedPC1 should be 100"
    assert dut.CorrectedPC2.value == 200, "CorrectedPC2 should be 200"

    # Randomized Inputs Test
    for _ in range(10000):  # Run 100 random tests
        PredictionM1 = random.randint(0, 1)
        PredictionM2 = random.randint(0, 1)
        branch_taken1 = random.randint(0, 1)
        branch_taken2 = random.randint(0, 1)
        PCPlus1M = random.randint(0, 2047)  # 11-bit address
        PCPlus2M = random.randint(0, 2047)  # 11-bit address
        branchAdderResultM1 = random.randint(0, 2047)  # 11-bit address
        branchAdderResultM2 = random.randint(0, 2047)  # 11-bit address

        await set_inputs(
            PredictionM1, PredictionM2, branch_taken1, branch_taken2,
            PCPlus1M, PCPlus2M, branchAdderResultM1, branchAdderResultM2
        )

        # Verify CorrectedPC1 logic
        if branch_taken1 and not PredictionM1:
            assert dut.CorrectedPC1.value == branchAdderResultM1, f"CorrectedPC1 should be {branchAdderResultM1} for inputs: {locals()}"
        else:
            assert dut.CorrectedPC1.value == PCPlus1M, f"CorrectedPC1 should be {PCPlus1M} for inputs: {locals()}"

        # Verify CorrectedPC2 logic
        if branch_taken2 and not PredictionM2:
            assert dut.CorrectedPC2.value == branchAdderResultM2, f"CorrectedPC2 should be {branchAdderResultM2} for inputs: {locals()}"
        else:
            assert dut.CorrectedPC2.value == PCPlus2M, f"CorrectedPC2 should be {PCPlus2M} for inputs: {locals()}"

    print("All tests passed, including randomized inputs!")
