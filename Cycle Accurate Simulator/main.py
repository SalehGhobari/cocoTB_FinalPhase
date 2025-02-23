import logging
from copy import deepcopy

INS_MEM_SIZE = 512
DATA_MEM_SIZE = 4096
DATA_MEM_READ = 50

logger = logging.getLogger(__name__)
logfile_handler = logging.FileHandler("cas_out.txt", mode='w')
logger.addHandler(logfile_handler)


class MEM_WB:
    def __init__(self):
        self.pc_plus_2 = 0
        self.reg_write = 0
        self.mem_to_reg = 0
        self.alu_result = 0
        self.memory_read_data = 0
        self.write_register = 0
        self.instruction = '00000000000000000000000000000000'

    def flush(self, flush):
        if flush: 
            self.__init__()


class EX_MEM:
    def __init__(self):
        self.pc = 0
        self.pc_plus_1 = 0
        self.pc_plus_2 = 0
        self.branch_adder_result = 0
        self.reg_write = 0
        self.mem_to_reg = 0
        self.mem_write = 0
        self.mem_read = 0
        self.rs = 0
        self.rt = 0
        self.branch = 0
        self.I_26 = 0
        self.prediction = 0
        self.alu_result = 0
        self.forward_A_mux_out = 0
        self.forward_B_mux_out = 0
        self.write_register = 0
        self.instruction = '00000000000000000000000000000000'

    def flush(self, flush):
        if flush: 
            self.__init__()


class ID_EX:
    def __init__(self):
        self.pc = 0
        self.pc_plus_1 = 0
        self.pc_plus_2 = 0
        self.branch_adder_result = 0
        self.I_26 = 0
        self.branch = 0
        self.mem_read = 0
        self.mem_write = 0
        self.mem_to_reg = 0
        self.reg_write = 0
        self.alu_op = 0
        self.reg_dst = 0
        self.alu_src = 0
        self.read_data1 = 0
        self.read_data2 = 0
        self.ext_imm = 0
        self.rs = 0
        self.rt = 0
        self.rd = 0
        self.shamt = 0
        self.prediction = 0
        self.instruction = '00000000000000000000000000000000'

    def flush(self, flush):
        if flush: 
            self.__init__()


class IF_ID:
    def __init__(self):
        self.pc = 0
        self.pc_plus_1 = 0
        self.pc_plus_2 = 0
        self.branch_adder_result1 = 0
        self.branch_adder_result2 = 0
        self.prediction1 = 0
        self.prediction2 = 0
        self.instruction1 = '00000000000000000000000000000000'
        self.instruction2 = '00000000000000000000000000000000'

    def flush(self, flush):
        if flush: 
            self.__init__()


class State:
    def __init__(self):
        self.if_id = IF_ID()
        self.id_ex1 = ID_EX()
        self.id_ex2 = ID_EX()
        self.ex_mem1 = EX_MEM()
        self.ex_mem2 = EX_MEM()
        self.mem_wb1 = MEM_WB()
        self.mem_wb2 = MEM_WB()

    def print(self):
        pass


class RF:
    def __init__(self):
        self.registers = []
        for i in range(32):
            self.registers.append(0)

    def read_rf(self, reg_num):
        return int(self.registers[reg_num])

    def write_rf(self, reg_num, write_data):
        if reg_num != 0:
            self.registers[reg_num] = write_data

    def out_rf(self):
        with open('rf_result.txt', 'w') as f:
            for i in range(32):
                f.write(str(self.registers[i]) + '\n')

    def print_rf(self):
        logger.warning(f'RF: {self.registers}')


class DataMem:
    def __init__(self):
        # with open('data_mem.txt', 'w') as f:
        #     for _ in range(DATA_MEM_SIZE):
        #         f.write(str(0) + '\n')
        pass

    @staticmethod
    def write_dm(address, data):
        with open('data_mem.txt', 'r') as f:
            read_data = f.read().split('\n')
        read_data[address] = str(data)
        with open('data_mem.txt', 'w') as f:
            for idx, line in enumerate(read_data):
                if idx < DATA_MEM_SIZE - 1:
                    f.write(f'{line}\n')
                else:
                    f.write(line)

    @staticmethod
    def read_dm(address):
        with open('data_mem.txt', 'r') as f:
            read_data = f.readlines()
        return int(read_data[address])

    @staticmethod
    def print_dm():
        with open('data_mem.txt', 'r') as f:
            read_data = f.readlines()
        logger.warning(f'DM: {list(map(int, read_data[0:DATA_MEM_READ]))}')


class InsMem:
    def __init__(self):
        with open('ins_mem.txt', 'r') as f:
            read_data = f.read().split('\n')
        self.instructions = read_data

    def get_instruction(self, address):
        return self.instructions[address]

    def get_offsets(self):
        offsets = {}
        for pc, instruction in enumerate(self.instructions):
            op_code = instruction[:6]
            op_code = hex(int(op_code, 2))
            if op_code == '0x4' or op_code == '0x5':
                offsets[str(pc)] = instruction[-8:]
        return offsets


class PC:
    def __init__(self):
        self.cur_pc = 0

    def update_pc(self, new_pc, EN):
        self.cur_pc = new_pc if EN else self.cur_pc


class HDU:
    def __init__(
            self, branch1M, branch2M, prediction_M1, prediction_M2, 
            branch_taken1, branch_taken2, pc_src1, pc_src2):
        self.branch1M = branch1M
        self.branch2M = branch2M
        self.prediction_M1 = prediction_M1
        self.prediction_M2 = prediction_M2
        self.branch_taken1 = branch_taken1
        self.branch_taken2 = branch_taken2
        self.pc_src1 = pc_src1
        self.pc_src2 = pc_src2


    @property
    def flush_MEM2(self):
        return (self.branch_taken1 ^ self.prediction_M1) & self.branch1M

    @property
    def flush_EX(self):
        return (((self.branch_taken1 ^ self.prediction_M1) & self.branch1M) | 
                ((self.branch_taken2 ^ self.prediction_M2) & self.branch2M))
    
    @property
    def flush_IF_ID(self):
        return (((self.branch_taken1 ^ self.prediction_M1) & self.branch1M) | 
                ((self.branch_taken2 ^ self.prediction_M2) & self.branch2M) | 
                self.pc_src1 | self.pc_src2)


class BPU:
    def __init__(self):
        self.cpc_signal1 = 0
        self.cpc_signal2 = 0
        self.BHT = [1 for _ in range(INS_MEM_SIZE)]
        self.BTB = [0 for _ in range(64)]
        self.BTB_valid = [0] * 64

    def predict(self, pc):
        match self.BHT[pc]:
            case 0:
                return 0
            case 1:
                return 0
            case 2:
                return 1
            case 3:
                return 1

    def update(self, pc, branch_taken, target):
        match self.BHT[pc]:
            case 0:
                self.BHT[pc] = 1 if branch_taken else 0
            case 1:
                self.BHT[pc] = 2 if branch_taken else 0
            case 2:
                self.BHT[pc] = 3 if branch_taken else 1
            case 3:
                self.BHT[pc] = 3 if branch_taken else 2

        if branch_taken:
            self.BTB[pc & 63] = target
            self.BTB_valid[pc & 63] = 1

    def set_corrected_pc(
            self, predictionM1, predictionM2, branch_taken1, branch_taken2,
            pc_plus_1M1, pc_plus_2M1, branch_adder_resultM1,
            branch_adder_resultM2, branchM1, branchM2
        ):
        self.cpc_signal1 = 0
        self.cpc_signal2 = 0
        self.corrected_pc1 = pc_plus_1M1
        self.corrected_pc2 = pc_plus_2M1
        
        if branchM1:
            if branch_taken1 and not predictionM1:
                self.corrected_pc1 = branch_adder_resultM1
                self.cpc_signal1 = 1
            if not branch_taken1 and predictionM1:
                self.corrected_pc1 = pc_plus_1M1
                self.cpc_signal1 = 1

        if branchM2:
            if branch_taken2 and not predictionM2:
                self.corrected_pc2 = branch_adder_resultM2
                self.cpc_signal2 = 1
            if not branch_taken2 and predictionM2:
                self.corrected_pc2 = pc_plus_2M1
                self.cpc_signal2 = 1
        
    @property
    def cpc_signal(self):
        return self.cpc_signal1 | self.cpc_signal2
        

def mux(sel, in1, in2, in3=None, in4=None, in5=None):
    if sel == 0:
        return in1
    elif sel == 1:
        return in2
    elif sel == 2:
        return in3
    elif sel == 3:
        return in4
    elif sel == 4:
        return in5


def alu(operand1, operand2, alu_shamt, op_sel):
    result = 0
    _overflow = 0

    match op_sel:
        case 0:  # add
            result = operand1 + operand2
        case 1:  # sub
            result = operand1 - operand2
        case 2:  # and
            result = operand1 & operand2
        case 3:  # or
            result = operand1 | operand2
        case 4:  # slt
            result = 1 if operand1 < operand2 else 0
        case 5:  # sgt
            result = 1 if operand1 > operand2 else 0
        case 6:  # nor
            result = ~(operand1 | operand2)
        case 7:  # xor
            result = operand1 ^ operand2
        case 8:  # sll
            result = (operand2 << alu_shamt) & (2 ** 32 - 1)
        case 9:  # srl
            result = operand2 >> alu_shamt
    zero = int(result == 0)

    return result, _overflow, zero


def cu(cu_op_code, cu_funct, cu_stall):
    control_unit = {'reg_dst': 0,
                    'branch': 0,
                    'mem_read': 0,
                    'mem_to_reg': 0,
                    'alu_op': 0,
                    'mem_write': 0,
                    'reg_write': 0,
                    'alu_src': 0,
                    'jump': 0,
                    'pc_src': 0}
    if cu_stall:
        return control_unit
    cu_op_code = hex(int(cu_op_code, 2))
    cu_funct = hex(int(cu_funct, 2))
    if cu_op_code == '0x0':  # R-TYPE
        control_unit.update({'reg_dst': 1,
                             'branch': 0,
                             'mem_read': 0,
                             'mem_to_reg': 0,
                             'alu_op': 0,
                             'mem_write': 0,
                             'reg_write': 1,
                             'alu_src': 0,
                             'jump': 0,
                             'pc_src': 0})

        if cu_funct == '0x20':  # add
            control_unit.update({'alu_op': 0})
        elif cu_funct == '0x22':  # sub
            control_unit.update({'alu_op': 1})
        elif cu_funct == '0x24':  # and
            control_unit.update({'alu_op': 2})
        elif cu_funct == '0x25':  # or
            control_unit.update({'alu_op': 3})
        elif cu_funct == '0x2a':  # slt
            control_unit.update({'alu_op': 4})
        elif cu_funct == '0x14':  # sgt
            control_unit.update({'alu_op': 5})
        elif cu_funct == '0x27':  # nor
            control_unit.update({'alu_op': 6})
        elif cu_funct == '0x15':  # xor
            control_unit.update({'alu_op': 7})
        elif cu_funct == '0x0':  # sll
            control_unit.update({'alu_op': 8})
        elif cu_funct == '0x2':  # srl
            control_unit.update({'alu_op': 9})
        elif cu_funct == '0x8':  # jr
            control_unit.update({'pc_src': 1})

    elif cu_op_code == '0x8':  # addi
        control_unit.update({'reg_write': 1,
                             'alu_src': 1})

    elif cu_op_code == '0x23':  # lw
        control_unit.update({'mem_read': 1,
                             'mem_to_reg': 1,
                             'reg_write': 1,
                             'alu_src': 1})

    elif cu_op_code == '0x2b':  # sw
        control_unit.update({'mem_write': 1,
                             'alu_src': 1})

    elif cu_op_code == '0x4' or cu_op_code == '0x5':  # beq or bne
        control_unit.update({'branch': 1,
                             'alu_op': 1})

    elif cu_op_code == '0x3':  # jal
        control_unit.update({'reg_dst': 2,
                             'mem_to_reg': 2,
                             'reg_write': 1,
                             'jump': 1,
                             'pc_src': 1})

    elif cu_op_code == '0xd':  # ori
        control_unit.update({'alu_op': 3,
                             'reg_write': 1,
                             'alu_src': 1})

    elif cu_op_code == '0x16':  # xori
        control_unit.update({'alu_op': 7,
                             'reg_write': 1,
                             'alu_src': 1})

    elif cu_op_code == '0xc':  # andi
        control_unit.update({'alu_op': 2,
                             'reg_write': 1,
                             'alu_src': 1})

    elif cu_op_code == '0xa':  # slti
        control_unit.update({'alu_op': 4,
                             'reg_write': 1,
                             'alu_src': 1})

    elif cu_op_code == '0x2':  # j
        control_unit.update({'jump': 1,
                             'pc_src': 1})

    return control_unit


def forward(rs_E1, rt_E1, rs_E2, rt_E2, rs_M2, rt_M2, write_register_M1, 
            write_register_M2, write_register_W1, write_register_W2, 
            reg_write_M1, reg_write_M2, reg_write_W1, reg_write_W2, branch_M2):
    forwardA1 = 0
    forwardB1 = 0
    forwardA2 = 0
    forwardB2 = 0
    forward_branch_A = 0
    forward_branch_B = 0

    if (reg_write_M1 and (write_register_M1 == rs_E1) and (write_register_M1 != 0)):
        forwardA1 = 1
    elif (reg_write_M2 and (write_register_M2 == rs_E1) and (write_register_M2 != 0) and (write_register_M1 != rs_E1)):
        forwardA1 = 2
    elif (reg_write_W1 and (write_register_W1 == rs_E1) and (write_register_W1 != 0) and
            ((write_register_M1 != rs_E1 or not reg_write_M1) and (write_register_M2 != rs_E1 or not reg_write_M2))):
        forwardA1 = 3
    elif (reg_write_W2 and (write_register_W2 == rs_E1) and (write_register_W2 != 0) and
            ((write_register_M1 != rs_E1 or not reg_write_M1) and (write_register_M2 != rs_E1 or not reg_write_M2)) and (write_register_M1 != rs_E1)):
        forwardA1 = 4

    if (reg_write_M1 and (write_register_M1 == rt_E1) and (write_register_M1 != 0)):
        forwardB1 = 1
    elif (reg_write_M2 and (write_register_M2 == rt_E1) and (write_register_M2 != 0) and (write_register_M1 != rt_E1)):
        forwardB1 = 2
    elif (reg_write_W1 and (write_register_W1 == rt_E1) and (write_register_W1 != 0) and
            ((write_register_M1 != rt_E1 or not reg_write_M1) and (write_register_M2 != rt_E1 or not reg_write_M2))):
        forwardB1 = 3
    elif (reg_write_W2 and (write_register_W2 == rt_E1) and (write_register_W2 != 0) and
            ((write_register_M1 != rt_E1 or not reg_write_M1) and (write_register_M2 != rt_E1 or not reg_write_M2)) and (write_register_M1 != rt_E1)):
        forwardB1 = 4

    if (reg_write_M1 and (write_register_M1 == rs_E2) and (write_register_M1 != 0)):
        forwardA2 = 1
    elif (reg_write_M2 and (write_register_M2 == rs_E2) and (write_register_M2 != 0) and (write_register_M1 != rs_E2)):
        forwardA2 = 2
    elif (reg_write_W1 and (write_register_W1 == rs_E2) and (write_register_W1 != 0) and
            ((write_register_M1 != rs_E2 or not reg_write_M1) and (write_register_M2 != rs_E2 or not reg_write_M2))):
        forwardA2 = 3
    elif (reg_write_W2 and (write_register_W2 == rs_E2) and (write_register_W2 != 0) and
            ((write_register_M1 != rs_E2 or not reg_write_M1) and (write_register_M2 != rs_E2 or not reg_write_M2)) and (write_register_M1 != rs_E2)):
        forwardA2 = 4

    if (reg_write_M1 and (write_register_M1 == rt_E2) and (write_register_M1 != 0)):
        forwardB2 = 1
    elif (reg_write_M2 and (write_register_M2 == rt_E2) and (write_register_M2 != 0) and (write_register_M1 != rt_E2)):
        forwardB2 = 2
    elif (reg_write_W1 and (write_register_W1 == rt_E2) and (write_register_W1 != 0) and
            ((write_register_M1 != rt_E2 or not reg_write_M1) and (write_register_M2 != rt_E2 or not reg_write_M2))):
        forwardB2 = 3
    elif (reg_write_W2 and (write_register_W2 == rt_E2) and (write_register_W2 != 0) and
            ((write_register_M1 != rt_E2 or not reg_write_M1) and (write_register_M2 != rt_E2 or not reg_write_M2)) and (write_register_M1 != rt_E2)):
        forwardB2 = 4
            
    if(reg_write_M1 & branch_M2 and((write_register_M1 == rs_M2))):
        forward_branch_A = 1
    if(reg_write_M1 & branch_M2 and((write_register_M1 == rt_M2))):
        forward_branch_B = 1

    return {
        'forwardA1': forwardA1,
        'forwardB1': forwardB1,
        'forwardA2': forwardA2,
        'forwardB2': forwardB2,
        'forward_branch_A': forward_branch_A,
        'forward_branch_B': forward_branch_B,
    }


def hdu_stall(mem_read_E, write_register_E, rs_D, rt_D):
    return (
        mem_read_E 
        and (write_register_E == rs_D or write_register_E == rt_D) 
        and write_register_E != 0
    )


def main(): 
    rf = RF()
    state = State()
    data_mem = DataMem()
    ins_mem = InsMem()
    pc = PC()
    branch_predictor = BPU()

    cycle = 0
    enable = 1
    
    while True:
        new_state = State()
        # --------------------WB STAGE------------------ #
        WB_data1 = WB_data2 = 0
        if state.mem_wb1.reg_write == 1:
            WB_data1 = mux(sel=state.mem_wb1.mem_to_reg,
                           in1=state.mem_wb1.alu_result,
                           in2=state.mem_wb1.memory_read_data,
                           in3=(state.mem_wb1.pc_plus_2 - 1) & (INS_MEM_SIZE - 1))

            rf.write_rf(reg_num=state.mem_wb1.write_register, write_data=WB_data1)
        if state.mem_wb2.reg_write == 1:
            WB_data2 = mux(sel=state.mem_wb2.mem_to_reg,
                           in1=state.mem_wb2.alu_result,
                           in2=state.mem_wb2.memory_read_data,
                           in3=state.mem_wb1.pc_plus_2)

            rf.write_rf(reg_num=state.mem_wb2.write_register, write_data=WB_data2)

        # --------------------FORWARDING------------------ #
        forward_signals = forward(rs_E1=state.id_ex1.rs, rt_E1=state.id_ex1.rt, 
                                  rs_E2=state.id_ex2.rs, rt_E2=state.id_ex2.rt, 
                                  rs_M2=state.ex_mem2.rs, rt_M2=state.ex_mem2.rt, 
                                  write_register_M1=state.ex_mem1.write_register, 
                                  write_register_M2=state.ex_mem2.write_register, 
                                  write_register_W1=state.mem_wb1.write_register, 
                                  write_register_W2=state.mem_wb2.write_register,
                                  reg_write_M1=state.ex_mem1.reg_write, 
                                  reg_write_M2=state.ex_mem2.reg_write, 
                                  reg_write_W1=state.mem_wb1.reg_write, 
                                  reg_write_W2=state.mem_wb2.reg_write, 
                                  branch_M2=state.ex_mem2.branch)

        # --------------------MEM STAGE------------------ #
        if state.ex_mem1.mem_write:
            data_mem.write_dm(address=state.ex_mem1.alu_result, data=state.ex_mem1.forward_B_mux_out)
        elif state.ex_mem2.mem_write:
            data_mem.write_dm(address=state.ex_mem2.alu_result, data=state.ex_mem2.forward_B_mux_out)
        if state.ex_mem1.mem_read:
            new_state.mem_wb1.memory_read_data = data_mem.read_dm(state.ex_mem1.alu_result)
        if state.ex_mem2.mem_read:
            new_state.mem_wb2.memory_read_data = data_mem.read_dm(state.ex_mem2.alu_result)

        comp_source_mux_A2 = mux(sel=forward_signals.get('forward_branch_A'), 
                                 in1=state.ex_mem2.forward_A_mux_out,
                                 in2=state.ex_mem1.alu_result)
        comp_source_mux_B2 = mux(sel=forward_signals.get('forward_branch_B'), 
                                 in1=state.ex_mem2.forward_B_mux_out,
                                 in2=state.ex_mem1.alu_result)

        zero1 = state.ex_mem1.forward_A_mux_out == state.ex_mem1.forward_B_mux_out
        zero2 = comp_source_mux_A2 == comp_source_mux_B2

        branch_taken1 = state.ex_mem1.branch & ~(state.ex_mem1.I_26 ^ ~zero1)
        branch_taken2 = state.ex_mem2.branch & ~(state.ex_mem2.I_26 ^ ~zero2)

        if state.ex_mem1.branch:
            branch_predictor.update(pc=state.ex_mem1.pc, branch_taken=branch_taken1, target=state.ex_mem1.branch_adder_result)
        if state.ex_mem2.branch:
            branch_predictor.update(pc=state.ex_mem1.pc_plus_1, branch_taken=branch_taken2, target=state.ex_mem2.branch_adder_result)

        branch_predictor.set_corrected_pc(
            predictionM1=state.ex_mem1.prediction,
            predictionM2=state.ex_mem2.prediction,
            branch_taken1=branch_taken1,
            branch_taken2=branch_taken2,
            pc_plus_1M1=state.ex_mem1.pc_plus_1,
            pc_plus_2M1=state.ex_mem1.pc_plus_2,
            branch_adder_resultM1=state.ex_mem1.branch_adder_result,
            branch_adder_resultM2=state.ex_mem2.branch_adder_result,
            branchM1=state.ex_mem1.branch,
            branchM2=state.ex_mem2.branch
        )

        new_state.mem_wb1.reg_write = state.ex_mem1.reg_write
        new_state.mem_wb1.mem_to_reg = state.ex_mem1.mem_to_reg
        new_state.mem_wb1.alu_result = state.ex_mem1.alu_result
        new_state.mem_wb1.write_register = state.ex_mem1.write_register
        new_state.mem_wb1.instruction = state.ex_mem1.instruction
        new_state.mem_wb1.pc_plus_2 = state.ex_mem1.pc_plus_2

        new_state.mem_wb2.reg_write = state.ex_mem2.reg_write
        new_state.mem_wb2.mem_to_reg = state.ex_mem2.mem_to_reg
        new_state.mem_wb2.alu_result = state.ex_mem2.alu_result
        new_state.mem_wb2.write_register = state.ex_mem2.write_register
        new_state.mem_wb2.instruction = state.ex_mem2.instruction

        # --------------------EX STAGE------------------ #
        forward_mux_A1_out = mux(sel=forward_signals.get('forwardA1'),
                                 in1=state.id_ex1.read_data1,
                                 in2=state.ex_mem1.alu_result,
                                 in3=state.ex_mem2.alu_result,
                                 in4=WB_data1,
                                 in5=WB_data2)
        forward_mux_B1_out = mux(sel=forward_signals.get('forwardB1'),
                                 in1=state.id_ex1.read_data2,
                                 in2=state.ex_mem1.alu_result,
                                 in3=state.ex_mem2.alu_result,
                                 in4=WB_data1,
                                 in5=WB_data2)
        
        forward_mux_A2_out = mux(sel=forward_signals.get('forwardA2'),
                                 in1=state.id_ex2.read_data1,
                                 in2=state.ex_mem1.alu_result,
                                 in3=state.ex_mem2.alu_result,
                                 in4=WB_data1,
                                 in5=WB_data2)
        forward_mux_B2_out = mux(sel=forward_signals.get('forwardB2'),
                                 in1=state.id_ex2.read_data2,
                                 in2=state.ex_mem1.alu_result,
                                 in3=state.ex_mem2.alu_result,
                                 in4=WB_data1,
                                 in5=WB_data2)

        alu_mux1 = mux(sel=state.id_ex1.alu_src,
                       in1=forward_mux_B1_out,
                       in2=state.id_ex1.ext_imm)
        
        alu_mux2 = mux(sel=state.id_ex2.alu_src,
                       in1=forward_mux_B2_out,
                       in2=state.id_ex2.ext_imm)

        alu_result1, _, _ = alu(operand1=forward_mux_A1_out,
                                operand2=alu_mux1,
                                alu_shamt=state.id_ex1.shamt,
                                op_sel=state.id_ex1.alu_op)
        
        alu_result2, _, _ = alu(operand1=forward_mux_A2_out,
                                operand2=alu_mux2,
                                alu_shamt=state.id_ex2.shamt,
                                op_sel=state.id_ex2.alu_op)

        reg_dst_mux1 = mux(sel=state.id_ex1.reg_dst,
                           in1=state.id_ex1.rt,
                           in2=state.id_ex1.rd,
                           in3=31)
        
        reg_dst_mux2 = mux(sel=state.id_ex2.reg_dst,
                           in1=state.id_ex2.rt,
                           in2=state.id_ex2.rd,
                           in3=31)

        new_state.ex_mem1.pc = state.id_ex1.pc
        new_state.ex_mem1.pc_plus_1 = state.id_ex1.pc_plus_1
        new_state.ex_mem1.pc_plus_2 = state.id_ex1.pc_plus_2
        new_state.ex_mem1.branch_adder_result = state.id_ex1.branch_adder_result
        new_state.ex_mem1.reg_write = state.id_ex1.reg_write
        new_state.ex_mem1.mem_to_reg = state.id_ex1.mem_to_reg
        new_state.ex_mem1.mem_write = state.id_ex1.mem_write
        new_state.ex_mem1.mem_read = state.id_ex1.mem_read
        new_state.ex_mem1.branch = state.id_ex1.branch
        new_state.ex_mem1.I_26 = state.id_ex1.I_26
        new_state.ex_mem1.prediction = state.id_ex1.prediction
        new_state.ex_mem1.alu_result = alu_result1
        new_state.ex_mem1.forward_B_mux_out = forward_mux_B1_out
        new_state.ex_mem1.forward_A_mux_out = forward_mux_A1_out
        new_state.ex_mem1.write_register = reg_dst_mux1
        new_state.ex_mem1.instruction = state.id_ex1.instruction

        new_state.ex_mem2.branch_adder_result = state.id_ex2.branch_adder_result
        new_state.ex_mem2.reg_write = state.id_ex2.reg_write
        new_state.ex_mem2.mem_to_reg = state.id_ex2.mem_to_reg
        new_state.ex_mem2.mem_write = state.id_ex2.mem_write
        new_state.ex_mem2.mem_read = state.id_ex2.mem_read
        new_state.ex_mem2.rs = state.id_ex2.rs
        new_state.ex_mem2.rt = state.id_ex2.rt
        new_state.ex_mem2.branch = state.id_ex2.branch
        new_state.ex_mem2.I_26 = state.id_ex2.I_26
        new_state.ex_mem2.prediction = state.id_ex2.prediction
        new_state.ex_mem2.alu_result = alu_result2
        new_state.ex_mem2.forward_B_mux_out = forward_mux_B2_out
        new_state.ex_mem2.forward_A_mux_out = forward_mux_A2_out
        new_state.ex_mem2.write_register = reg_dst_mux2
        new_state.ex_mem2.instruction = state.id_ex2.instruction

        # --------------------ID STAGE------------------ #
        op_code1 = state.if_id.instruction1[:6]
        funct1 = state.if_id.instruction1[-6:]
        rs1 = int(state.if_id.instruction1[6:11], 2)
        rt1 = int(state.if_id.instruction1[11:16], 2)
        rd1 = int(state.if_id.instruction1[16:21], 2)
        shamt1 = int(state.if_id.instruction1[21:26], 2)
        imm1 = int(state.if_id.instruction1[-16:], 2)
        if imm1 >> 15 == 1:
            imm1 = imm1 - 2 ** 16
        I_26_1 = int(op_code1[-1])

        op_code2 = state.if_id.instruction2[:6]
        funct2 = state.if_id.instruction2[-6:]
        rs2 = int(state.if_id.instruction2[6:11], 2)
        rt2 = int(state.if_id.instruction2[11:16], 2)
        rd2 = int(state.if_id.instruction2[16:21], 2)
        shamt2 = int(state.if_id.instruction2[21:26], 2)
        imm2 = int(state.if_id.instruction2[-16:], 2)
        if imm2 >> 15 == 1:
            imm2 = imm2 - 2 ** 16
        I_26_2 = int(op_code2[-1])

        stall = (
            hdu_stall(state.id_ex1.mem_read, reg_dst_mux1, rs1, rt1) or 
            hdu_stall(state.id_ex2.mem_read, reg_dst_mux2, rs1, rt1) or 
            hdu_stall(state.id_ex1.mem_read, reg_dst_mux1, rs2, rt2) or 
            hdu_stall(state.id_ex2.mem_read, reg_dst_mux2, rs2, rt2)
        )

        control_signals1 = cu(cu_op_code=op_code1, cu_funct=funct1, cu_stall=stall)
        control_signals2 = cu(cu_op_code=op_code2, cu_funct=funct2, cu_stall=stall)

        read_data1 = rf.read_rf(rs1)
        read_data2 = rf.read_rf(rt1)

        read_data3 = rf.read_rf(rs2)
        read_data4 = rf.read_rf(rt2)
        
        new_state.id_ex1.branch_adder_result = state.if_id.branch_adder_result1
        new_state.id_ex1.I_26 = I_26_1
        new_state.id_ex1.branch = control_signals1.get('branch')
        new_state.id_ex1.mem_read = control_signals1.get('mem_read')
        new_state.id_ex1.mem_write = control_signals1.get('mem_write')
        new_state.id_ex1.mem_to_reg = control_signals1.get('mem_to_reg')
        new_state.id_ex1.reg_write = control_signals1.get('reg_write')
        new_state.id_ex1.alu_op = control_signals1.get('alu_op')
        new_state.id_ex1.reg_dst = control_signals1.get('reg_dst')
        new_state.id_ex1.alu_src = control_signals1.get('alu_src')
        new_state.id_ex1.read_data1 = read_data1
        new_state.id_ex1.read_data2 = read_data2
        new_state.id_ex1.ext_imm = imm1
        new_state.id_ex1.rs = rs1
        new_state.id_ex1.rt = rt1
        new_state.id_ex1.rd = rd1
        new_state.id_ex1.shamt = shamt1
        new_state.id_ex1.prediction = state.if_id.prediction1
        new_state.id_ex1.instruction = state.if_id.instruction1
        new_state.id_ex1.pc = state.if_id.pc
        new_state.id_ex1.pc_plus_1 = state.if_id.pc_plus_1
        new_state.id_ex1.pc_plus_2 = state.if_id.pc_plus_2

        new_state.id_ex2.branch_adder_result = state.if_id.branch_adder_result2
        new_state.id_ex2.I_26 = I_26_2
        new_state.id_ex2.branch = control_signals2.get('branch')
        new_state.id_ex2.mem_read = control_signals2.get('mem_read')
        new_state.id_ex2.mem_write = control_signals2.get('mem_write')
        new_state.id_ex2.mem_to_reg = control_signals2.get('mem_to_reg')
        new_state.id_ex2.reg_write = control_signals2.get('reg_write')
        new_state.id_ex2.alu_op = control_signals2.get('alu_op')
        new_state.id_ex2.reg_dst = control_signals2.get('reg_dst')
        new_state.id_ex2.alu_src = control_signals2.get('alu_src')
        new_state.id_ex2.read_data1 = read_data3
        new_state.id_ex2.read_data2 = read_data4
        new_state.id_ex2.ext_imm = imm2
        new_state.id_ex2.rs = rs2
        new_state.id_ex2.rt = rt2
        new_state.id_ex2.rd = rd2
        new_state.id_ex2.shamt = shamt2
        new_state.id_ex2.prediction = state.if_id.prediction2
        new_state.id_ex2.instruction = state.if_id.instruction2

        # --------------------IF STAGE------------------ #
        pc_plus_1 = (pc.cur_pc + 1) & (INS_MEM_SIZE - 1)

        prediction1 = branch_predictor.predict(pc=pc.cur_pc)
        prediction2 = branch_predictor.predict(pc=pc_plus_1)

        instruction1 = ins_mem.get_instruction(address=pc.cur_pc)

        inst2_address = (
            branch_predictor.BTB[(pc.cur_pc) & 63]
            if prediction1 and branch_predictor.BTB_valid[(pc.cur_pc) & 63]
            else pc_plus_1
        )
        instruction2 = ins_mem.get_instruction(address=inst2_address)

        pc_plus_2 = (pc.cur_pc + 2) & (INS_MEM_SIZE - 1)
        branch_adder_result1 = (pc_plus_1 + int(instruction1[-9:], 2)) & (INS_MEM_SIZE - 1)
        branch_adder_result2 = (pc_plus_2 + int(instruction2[-9:], 2)) & (INS_MEM_SIZE - 1)

        jump_mux1 = mux(sel=control_signals1.get('jump'), in1=read_data1 & (INS_MEM_SIZE - 1), in2=int(state.if_id.instruction1[-9:], 2))
        jump_mux2 = mux(sel=control_signals2.get('jump'), in1=read_data3 & (INS_MEM_SIZE - 1), in2=int(state.if_id.instruction2[-9:], 2))
        jump_mux = mux(sel=control_signals2.get('pc_src'), in1=jump_mux1, in2=jump_mux2)

        branch_mux1 = mux(sel=prediction1, in1=pc_plus_2, in2=(inst2_address + 1) & (INS_MEM_SIZE - 1))
        branch_mux = mux(sel=prediction2, in1=branch_mux1, in2=branch_adder_result2)

        pc_mux = mux(sel=control_signals1.get('pc_src') | control_signals2.get('pc_src'), in1=branch_mux, in2=jump_mux)
        cpc_mux = mux(sel=branch_predictor.cpc_signal2, in1=branch_predictor.corrected_pc1, in2=branch_predictor.corrected_pc2)
        next_pc_mux = mux(sel=branch_predictor.cpc_signal, in1=pc_mux, in2=cpc_mux)

        logger.warning(f'CYCLE_START')
        logger.warning(f'cycle: {cycle}, PC: {pc.cur_pc}')
        
        enable_pc_IF_ID = (not stall) and enable or branch_predictor.cpc_signal
        if enable_pc_IF_ID:
            new_state.if_id.pc_plus_2 = pc_plus_2
            new_state.if_id.pc_plus_1 = pc_plus_1
            new_state.if_id.pc = pc.cur_pc
            new_state.if_id.branch_adder_result1 = branch_adder_result1
            new_state.if_id.branch_adder_result2 = branch_adder_result2
            new_state.if_id.prediction1 = prediction1
            new_state.if_id.prediction2 = prediction2
            new_state.if_id.instruction1 = instruction1
            new_state.if_id.instruction2 = instruction2
        else:
            new_state.if_id = deepcopy(state.if_id)
        pc.update_pc(next_pc_mux, enable_pc_IF_ID)

        hdu = HDU(
            branch1M=state.ex_mem1.branch,
            branch2M=state.ex_mem2.branch,
            prediction_M1=state.ex_mem1.prediction,
            prediction_M2=state.ex_mem2.prediction,
            branch_taken1=branch_taken1,
            branch_taken2=branch_taken2,
            pc_src1=control_signals1.get('pc_src'),
            pc_src2=control_signals2.get('pc_src')
        )

        new_state.if_id.flush(flush=hdu.flush_IF_ID)
        new_state.id_ex1.flush(flush=hdu.flush_EX)
        new_state.id_ex2.flush(flush=hdu.flush_EX or control_signals1.get('pc_src'))
        new_state.ex_mem1.flush(flush=hdu.flush_EX)
        new_state.ex_mem2.flush(flush=hdu.flush_EX)
        new_state.mem_wb2.flush(flush=hdu.flush_MEM2)

        logger.warning(f'Instruction1(Fetch): {hex(int(instruction1, 2))}')
        logger.warning(f'Instruction2(Fetch): {hex(int(instruction2, 2))}')
        rf.print_rf()
        data_mem.print_dm()
        logger.warning(f'CYCLE_END')
        logger.warning(f'\n')

        if pc.cur_pc >= INS_MEM_SIZE - 2:
            break

        cycle += 1
        state = deepcopy(new_state)

    rf.out_rf()


if __name__ == '__main__':
    main()
