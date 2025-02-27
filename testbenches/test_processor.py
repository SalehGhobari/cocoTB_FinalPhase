import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import ctypes

def to_signed_16bit(value):
    return ctypes.c_int16(value).value

def to_int(array):
    return [ctypes.c_int32(int(x)).value for x in array]

def decode_instruction(instruction):
    opcode = (instruction >> 26) & 0x3F
    rs = (instruction >> 21) & 0x1F
    rt = (instruction >> 16) & 0x1F
    rd = (instruction >> 11) & 0x1F
    shamt = (instruction >> 6) & 0x1F
    funct = instruction & 0x3F
    imm = instruction & 0xFFFF
    address = instruction & 0x3FFFFFF

    opcodes = {
        0x08: "addi", 0x23: "lw", 0x2B: "sw", 0x04: "beq", 0x05: "bne",
        0x03: "jal", 0x0D: "ori", 0x16: "xori", 0x0C: "andi", 0x0A: "slti",
        0x02: "j"
    }

    functs = {
        0x20: "add", 0x22: "sub", 0x24: "and", 0x25: "or", 0x2A: "slt",
        0x14: "sgt", 0x00: "sll", 0x02: "srl", 0x27: "nor", 0x15: "xor",
        0x08: "jr"
    }

    if opcode == 0:  # R-Type instruction
        if funct in functs:
            if funct in {0x00, 0x02}:  # Shift instructions
                return f"{functs[funct]} ${rd}, ${rt}, {shamt}"
            elif funct == 0x08:  # JR instruction
                return f"{functs[funct]} ${rs}"
            else:
                return f"{functs[funct]} ${rd}, ${rs}, ${rt}"
        else:
            return "Unknown R-Type instruction"
    elif opcode in opcodes:
        if opcode in {0x04, 0x05}:  # Branch instructions
            return f"{opcodes[opcode]} ${rs}, ${rt}, {to_signed_16bit(imm)}"
        elif opcode in {0x02, 0x03}:  # Jump instructions
            return f"{opcodes[opcode]} {hex(address)}"
        elif opcode in {0x23, 0x2B}:  # Load/store instructions
            return f"{opcodes[opcode]} ${rt}, {to_signed_16bit(imm)}(${rs})"
        else:  # Immediate-type instructions
            return f"{opcodes[opcode]} ${rt}, ${rs}, {to_signed_16bit(imm)}"
    else:
        return "Unknown instruction"



@cocotb.test()
async def processor_test(dut):
    """Testbench for the processor module."""
    
    # Clock with a period of 10 ns (100 MHz)
    dut.enable.value = 1
    dut.rst.value = 0
    dut.clk.value = 0
    
    await Timer(1, units="ns")
    dut.enable.value = 1
    
    await Timer(3, units="ns")
    dut.rst.value = 1
    
    await Timer(1, units="ns")  
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    nop_count = 0
    max_nops = 10  # Number of consecutive NOPs to detect program end

    total_instructions_executed = 0
    total_cycles = 0

    cycle = 0
    while True:
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        total_cycles = cycle - max_nops + 1
        instr1 = dut.instMem.q_a.value
        instr2 = dut.instMem.q_b.value
        await FallingEdge(dut.clk)
        await Timer(1, units="ns")
        registers = to_int(dut.RegFile.registers.value)
        dm_values = to_int(dut.DM.altsyncram_component.m_default.altsyncram_inst.mem_data.value)
        if cycle % 100000 == 0:
            cocotb.log.warning(f"CYCLE_START\nCycle {cycle}: PC={int(dut.PC.value)}\n\
            Instruction1(Fetch)={hex(instr1)} ({decode_instruction(instr1)})\n\
            Instruction2(Fetch)={hex(instr2)} ({decode_instruction(instr2)})\n\
            RF: {to_int(registers)}\n\
            DM: {to_int(dm_values[2600:3896])}\n\
            CYCLE_END")
        

        # Count non-NOP instructions
        if instr1 != 0x00000000:
            total_instructions_executed += 1
        if instr2 != 0x00000000:
            total_instructions_executed += 1

        # Check for NOPs
        if instr1 == 0x00000000 and instr2 == 0x00000000:
            nop_count += 1
            if nop_count >= max_nops:
                cocotb.log.info("Detected sequence of NOPs, Program ended at cycle " + str(cycle - max_nops))
                break
        else:
            nop_count = 0
        cycle += 1  # Increment cycle count manually


    if total_cycles > 0:
        ipc = total_instructions_executed / total_cycles
        cocotb.log.info(f"IPC Calculation:")
        cocotb.log.info(f"Total Instructions Executed (excluding NOPs) = {total_instructions_executed}")
        cocotb.log.info(f"Total Cycles = {total_cycles}")
        cocotb.log.info(f"IPC = {ipc:.2f}")
    else:
        cocotb.log.info("IPC Calculation: No instructions executed.")