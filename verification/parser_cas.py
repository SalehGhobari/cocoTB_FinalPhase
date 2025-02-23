import re


class Library:
    def __init__(self, path_str):
        self.cycles = []
        self.parse(path_str)

    def parse(self, path_str):
        in_cycle = False
        start_pattern = re.compile(r'CYCLE_START')
        end_pattern = re.compile(r'CYCLE_END')

        cycle_block = []
        with open(path_str, 'r') as file_handler:
            for line in file_handler:
                match = start_pattern.match(line)
                if match is not None:
                    in_cycle = True
                if in_cycle:
                    cycle_block.append(line)
                match = end_pattern.match(line)
                if match is not None and in_cycle:
                    in_cycle = False
                    self.cycles.append(Cycle(cycle_block))
                    cycle_block = []


class Cycle:
    def __init__(self, cycle_block):
        self.parse(cycle_block)
    
    def parse(self, cycle_block: list[str]):
        self.cycle = self.pc = self.instruction1 = self.instruction2 = self.rf = self.dm = ''
        cycle_pc_pattern = re.compile(r'cycle:\s(\d+),\sPC:\s(\d+)$')
        instruction1_pattern = re.compile(r'Instruction1\(Fetch\):\s(\S+)$')
        instruction2_pattern = re.compile(r'Instruction2\(Fetch\):\s(\S+)$')
        rf_pattern = re.compile(r'RF:\s(.+)$')
        dm_pattern = re.compile(r'DM:\s(.+)$')

        for line in cycle_block:
            match = cycle_pc_pattern.search(line)
            if match is not None:
                self.cycle = match.group(1)
                self.pc = match.group(2)

            match = instruction1_pattern.match(line)
            if match is not None:
                self.instruction1 = match.group(1)
            
            match = instruction2_pattern.match(line)
            if match is not None:
                self.instruction2 = match.group(1)

            match = rf_pattern.match(line)
            if match is not None:
                self.rf = match.group(1)
                
            match = dm_pattern.match(line)
            if match is not None:
                self.dm = match.group(1)
                
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f'PC: {self.pc}, I1: {self.instruction1}, I2: {self.instruction2}\nRF: {self.rf}\nDM: {self.dm}'


def main():
    lib = Library(path_str='cas_out.txt')
    print('\n'.join(list(map(str, lib.cycles))))


if __name__ == '__main__':
    main()
