import heapq
import re
from collections import defaultdict

R_TYPE = ['ADD', 'SUB', 'AND', 'OR', 'XOR', 'NOR', 'SLT', 'SGT', 'SLL', 'SRL']
I_TYPE = ['LW', 'SW', 'ADDI', 'ORI', 'XORI', 'ANDI', 'SLTI']
BRANCH = ['BEQ', 'BNE']
JUMP = ['J', 'JR', 'JAL']


class Instruction:
    def __init__(self, instruction_str, inst_type, dest=None, src1=None, 
                 src2=None, is_label=False):
        self.instruction_str = instruction_str
        self.inst_type = inst_type
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.is_label = is_label

    @property
    def is_branch_jump(self):
        return self.inst_type in BRANCH or self.inst_type in JUMP

    @classmethod
    def from_str(cls, instruction_str):
        split_inst = [
            item.strip(' ,').upper() 
            for item in instruction_str.split()
        ]

        label = re.compile(r'[A-Z_0-9]+\:')
        if label.match(instruction_str.upper()) is not None:
            return cls(instruction_str, inst_type='LABEL', is_label=True)

        if split_inst[0] == 'NOP':
            return cls(instruction_str, inst_type='NOP')

        if split_inst[0] in BRANCH:
            return cls(instruction_str, inst_type=split_inst[0], 
                       src1=split_inst[1], src2=split_inst[2])

        if split_inst[0] in JUMP:
            if split_inst[0] == 'JR':
                return cls(instruction_str, inst_type=split_inst[0], src1=split_inst[1])
            if split_inst[0] == 'JAL':
                return cls(instruction_str, inst_type=split_inst[0], dest='$31')
            return cls(instruction_str, inst_type=split_inst[0])

        if split_inst[0] in R_TYPE:
            if split_inst[0] == 'SLL' or split_inst[0] == 'SRL':
                return cls(instruction_str, inst_type=split_inst[0], 
                           dest=split_inst[1], src1=split_inst[2])
            return cls(instruction_str, inst_type=split_inst[0], 
                       dest=split_inst[1], src1=split_inst[2], 
                       src2=split_inst[3])

        elif split_inst[0] in I_TYPE:
            if split_inst[0] == 'LW' or split_inst[0] == 'SW':
                pattern = re.compile(r'\((.+)\)')
                match = pattern.search(instruction_str).group(1)
                if split_inst[0] == 'LW':
                    return cls(instruction_str, inst_type=split_inst[0], 
                               dest=split_inst[1], src1=match)
                return cls(instruction_str, inst_type=split_inst[0], 
                           src1=split_inst[1], src2=match)
            return cls(instruction_str, inst_type=split_inst[0], 
                       dest=split_inst[1], src1=split_inst[2])
    
    @staticmethod
    def are_dependent(inst1, inst2):
        return any((inst1.dest == inst2.dest  # dest1 == dest2
                    and inst1.dest != '$0' 
                    and inst1.dest is not None,
                    inst1.dest == inst2.src1  # dest1 == inst2_src1
                    and inst1.dest != '$0' 
                    and inst1.dest is not None,
                    inst1.dest == inst2.src2  # dest1 == inst2_src2
                    and inst1.dest != '$0' 
                    and inst1.dest is not None,
                    inst2.dest == inst1.src1  # dest2 == inst1_src1
                    and inst2.dest != '$0' 
                    and inst2.dest is not None,
                    inst2.dest == inst1.src2  # dest2 == inst1_src2
                    and inst2.dest != '$0' 
                    and inst2.dest is not None,
                    (inst1.inst_type == 'SW'         # SW -> SW or SW -> LW or LW -> SW
                    or inst1.inst_type == 'LW')
                    and (inst2.inst_type == 'SW'
                         or (inst2.inst_type == 'LW' and
                              inst1.inst_type != 'LW'))))

    @staticmethod
    def should_nop(inst1, inst2):
        return (
            inst1.is_branch_jump and inst2.is_branch_jump or  # branches/jumps possibly in the same packet
            Instruction.is_raw(inst1, inst2) and not inst2.inst_type in BRANCH or 
            inst1.inst_type == 'LW' and Instruction.is_raw(inst1, inst2) or
            (inst1.inst_type == 'SW'
            or inst1.inst_type == 'LW')
            and (inst2.inst_type == 'SW'
                    or (inst2.inst_type == 'LW' and
                        inst1.inst_type != 'LW'))
        )

    @staticmethod
    def is_war_waw(inst1, inst2):
        return any((inst1.dest == inst2.dest  # dest1 == dest2
                    and inst1.dest != '$0' 
                    and inst1.dest is not None,
                    inst2.dest == inst1.src1  # dest2 == inst1_src1
                    and inst2.dest != '$0' 
                    and inst2.dest is not None,
                    inst2.dest == inst1.src2  # dest2 == inst1_src2
                    and inst2.dest != '$0' 
                    and inst2.dest is not None)) and not Instruction.is_raw(inst1, inst2)
    
    @staticmethod
    def is_raw(inst1, inst2):
        return any((inst1.dest == inst2.src1  # dest1 == inst2_src1
                    and inst1.dest != '$0' 
                    and inst1.dest is not None,
                    inst1.dest == inst2.src2  # dest1 == inst2_src2
                    and inst1.dest != '$0' 
                    and inst1.dest is not None))

    def __repr__(self):
        return self.instruction_str


def read_instructions(path_str: str) -> list[str]:
    with open(path_str, 'r') as file_handler:
        return [item.split("#", 1)[0] for item in file_handler.read().strip().split('\n')]


def topo_sort(start: int, num_of_nodes: int, 
              adj: list[list[int]]) -> list[int]:
    """Performs topological sort on graph and returns sorted instructions"""
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    for idx in range(start, start + num_of_nodes):
        out_degree[idx] = len(adj[idx])
        for end_node in adj[idx]:
            in_degree[end_node] += 1
            
    max_heap = []
    for idx in range(start, start + num_of_nodes):
        if in_degree[idx] == 0:
            heapq.heappush(max_heap, (-out_degree[idx], idx))

    instruction_order = []
    while max_heap:
        _, inst1 = heapq.heappop(max_heap)
        inst2 = -1
        if max_heap:
            _, inst2 = heapq.heappop(max_heap)

        for end_node in adj[inst1]:
            in_degree[end_node] -= 1
            if in_degree[end_node] == 0:
                heapq.heappush(max_heap, (-out_degree[end_node], end_node))

        if inst2 != -1:
            for end_node in adj[inst2]:
                in_degree[end_node] -= 1
                if in_degree[end_node] == 0:
                    heapq.heappush(max_heap, (-out_degree[end_node], end_node))

        instruction_order.append(inst1)
        if inst2 != -1:
            instruction_order.append(inst2)

    # if instruction_order and instruction_order[-1] == -1:
    #     instruction_order.pop()

    return instruction_order


def schedule(instruction_list: list[Instruction]) -> list[str]:
    splits = [-1]
    for idx, instruction in enumerate(instruction_list):
        if (instruction.is_label or 
            instruction.inst_type in BRANCH or 
            instruction.inst_type in JUMP
        ):
            splits.append(idx)
    splits.append(len(instruction_list))

    ins_ranges = []
    for idx in range(len(splits)-1):
        ins_ranges.append((splits[idx] + 1, splits[idx + 1] - 1))

    scheduled_instructions = []
    for ins_range in ins_ranges:
        instruction_count = ins_range[1] - ins_range[0] + 1
        adj = {}
        for i in range(instruction_count):
            adj[ins_range[0] + i] = []
        for inst1_idx in range(ins_range[0], ins_range[1] + 1):
            inst1 = instruction_list[inst1_idx]
            for inst2_idx in range(inst1_idx + 1, ins_range[1] + 1):
                inst2 = instruction_list[inst2_idx]
                if Instruction.are_dependent(inst1, inst2):
                    adj[inst1_idx].append(inst2_idx)

        scheduled_instructions.extend([
            instruction_list[idx] if idx != -1
            else Instruction('NOP', inst_type='NOP')
            for idx in topo_sort(ins_range[0], instruction_count, adj)
        ])

        if ins_range[1] + 1 < len(instruction_list):
            scheduled_instructions.append(instruction_list[ins_range[1] + 1])

    final_schedule = []
    idx = 0
    while idx < len(scheduled_instructions) - 1:
        inst1 = scheduled_instructions[idx]
        inst2 = scheduled_instructions[idx + 1]

        final_schedule.append(repr(inst1))

        labels = []
        while inst2.is_label:
            labels.append(repr(inst2))
            idx += 1
            if idx >= len(scheduled_instructions) - 1:
                break
            inst2 = scheduled_instructions[idx + 1]

        if idx >= len(scheduled_instructions) - 1:
            break

        while inst2.inst_type == 'NOP':
            idx += 1
            if idx >= len(scheduled_instructions) - 1:
                break
            inst2 = scheduled_instructions[idx + 1]

        if idx >= len(scheduled_instructions) - 1:
            break

        if Instruction.should_nop(inst1, inst2):
            final_schedule.append('NOP')
        
        final_schedule.extend(labels)
        idx += 1
    
    final_schedule.append(repr(scheduled_instructions[-1]))
    return final_schedule


def main():
    instruction_strings = read_instructions('instructions.txt')
    
    updated_strings = []
    for inst_str in instruction_strings:
        split_inst_str = inst_str.split()
        temp_reg1 = 1
        temp_reg2 = 2
        if split_inst_str[0].upper() == 'BLTZ':
            updated_strings.append(f'SLT ${temp_reg1}, {split_inst_str[1]} $0')
            updated_strings.append(f'BNE ${temp_reg1}, $0, {split_inst_str[2]}')
        elif split_inst_str[0].upper() == 'BGEZ':
            updated_strings.append(f'SLT ${temp_reg2}, {split_inst_str[1]} $0')
            updated_strings.append(f'BEQ ${temp_reg2}, $0, {split_inst_str[2]}')
        else:
            updated_strings.append(inst_str)

    instruction_list = [
        Instruction.from_str(instruction_str) 
        for instruction_str in updated_strings
    ]
    scheduled_instructions = schedule(instruction_list)
    with open('scheduled_output.txt', 'w') as file_handler:
        file_handler.write('\n'.join(scheduled_instructions))


if __name__ == '__main__':
    main()
