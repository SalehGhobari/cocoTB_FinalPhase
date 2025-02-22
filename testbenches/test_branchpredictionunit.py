import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.binary import BinaryValue
import random

class BranchScenario:
    def __init__(self, pc, is_branch, is_taken, target):
        self.pc = pc
        self.is_branch = is_branch
        self.is_taken = is_taken
        self.target = target

@cocotb.test()
async def test_bpu_initialization(dut):
    """Test the initialization of BPU after reset"""
    
    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0
    await RisingEdge(dut.clk)
    dut.reset.value = 1
    
    # Check initial state - should predict not taken
    dut.pc1.value = 0
    dut.pc2.value = 1
    dut.nextPC.value = 2
    await RisingEdge(dut.clk)
    
    assert dut.prediction1.value == 0, "Initial prediction should be not taken"
    assert dut.prediction2.value == 0, "Initial prediction should be not taken"
    assert dut.instMemPred.value == 0, "Initial instMemPred should be not taken"

@cocotb.test()
async def test_single_branch_learning(dut):
    """Test BPU learning behavior for a single branch instruction"""
    
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0
    await RisingEdge(dut.clk)
    dut.reset.value = 1
    
    # Train the predictor with a branch that's always taken
    pc_val = 16
    target_val = 32
    
    for _ in range(4):
        # Execute branch
        dut.pc1.value = pc_val
        dut.pcM1.value = pc_val
        dut.branch1.value = 1
        dut.branch_taken1.value = 1
        dut.targetM1.value = target_val
        
        initial_pred = dut.prediction1.value
        await RisingEdge(dut.clk)
        
        if _ >= 2:
            assert dut.prediction1.value == 1, f"Prediction should be taken after training (iteration {_})"
            assert dut.predictedTarget1.value == target_val, f"Target prediction should match (iteration {_})"

@cocotb.test()
async def test_two_branch_scenario(dut):
    """Test BPU handling two branches simultaneously"""
    
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0
    await RisingEdge(dut.clk)
    dut.reset.value = 1
    
    # Setup two different branches
    branch1_pc = 20
    branch1_target = 40
    branch2_pc = 24
    branch2_target = 48
    
    # Train both branches
    for _ in range(4):
        dut.pc1.value = branch1_pc
        dut.pc2.value = branch2_pc
        dut.pcM1.value = branch1_pc
        dut.pcM2.value = branch2_pc
        dut.branch1.value = 1
        dut.branch2.value = 1
        dut.branch_taken1.value = 1
        dut.branch_taken2.value = 1
        dut.targetM1.value = branch1_target
        dut.targetM2.value = branch2_target
        
        await RisingEdge(dut.clk)
        
        if _ >= 2:
            assert dut.prediction1.value == 1, f"Branch 1 prediction should be taken (iteration {_})"
            assert dut.prediction2.value == 1, f"Branch 2 prediction should be taken (iteration {_})"
            assert dut.predictedTarget1.value == branch1_target, f"Branch 1 target should match (iteration {_})"

@cocotb.test()
async def test_pattern_learning(dut):
    """Test BPU learning a specific taken/not-taken pattern"""
    
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0
    await RisingEdge(dut.clk)
    dut.reset.value = 1
    
    pc_val = 28
    target_val = 56
    
    # Pattern: Taken, Not Taken, Taken, Not Taken
    pattern = [1, 0, 1, 0]
    
    # Train the pattern multiple times
    for _ in range(3):
        for taken in pattern:
            dut.pc1.value = pc_val
            dut.pcM1.value = pc_val
            dut.branch1.value = 1
            dut.branch_taken1.value = taken
            dut.targetM1.value = target_val
            
            await RisingEdge(dut.clk)

@cocotb.test()
async def test_btb_behavior(dut):
    """Test Branch Target Buffer behavior"""
    
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0
    await RisingEdge(dut.clk)
    dut.reset.value = 1
    
    # Test BTB update and prediction
    pc_val = 32
    target_val = 64
    
    # First access should predict PC+1 (BTB miss)
    dut.pc1.value = pc_val
    await RisingEdge(dut.clk)
    assert dut.predictedTarget1.value == pc_val + 1, "BTB miss should predict PC+1"
    
    # Train the BTB
    dut.pcM1.value = pc_val
    dut.branch1.value = 1
    dut.branch_taken1.value = 1
    dut.targetM1.value = target_val
    await RisingEdge(dut.clk)
    
    # Next access should hit in BTB
    dut.pc1.value = pc_val
    await RisingEdge(dut.clk)
    assert dut.predictedTarget1.value == target_val, "BTB hit should predict correct target"

# Optional: Add this to your conftest.py
def pytest_configure(config):
    config.option.tb_logs = True