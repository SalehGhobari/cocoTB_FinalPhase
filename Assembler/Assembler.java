import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
public class Assembler {
    private HashMap<String, String> opcodes;
    private HashMap<String, String> functCodes;
    private HashMap<String, Integer> labelAddresses;
    private int currentAddress;
    private ArrayList<String> instructions;

    public Assembler() {
        init();
        reset();
    }

    public void reset() {
        labelAddresses = new HashMap<>();
        currentAddress = 0;
        instructions = new ArrayList<>();
    }

    public void init() {
        // Existing opcode and functCode initialization remains the same
        opcodes = new HashMap<>();
        opcodes.put("add", "000000");
        opcodes.put("sub", "000000");
        opcodes.put("and", "000000");
        opcodes.put("or", "000000");
        opcodes.put("slt", "000000");
        opcodes.put("sgt", "000000");
        opcodes.put("nor", "000000");
        opcodes.put("xor", "000000");
        opcodes.put("jr", "000000");
        opcodes.put("sll", "000000");
        opcodes.put("srl", "000000");
        opcodes.put("addi", "001000");
        opcodes.put("lw", "100011");
        opcodes.put("sw", "101011");
        opcodes.put("beq", "000100");
        opcodes.put("bne", "000101");
        opcodes.put("j", "000010");
        opcodes.put("jal", "000011");
        opcodes.put("ori", "001101");
        opcodes.put("xori", "010110");
        opcodes.put("andi", "001100");
        opcodes.put("slti", "001010");
        opcodes.put("nop", "000000");

        functCodes = new HashMap<>();
        functCodes.put("add", "100000");
        functCodes.put("sub", "100010");
        functCodes.put("and", "100100");
        functCodes.put("or", "100101");
        functCodes.put("slt", "101010");
        functCodes.put("sgt", "010100");
        functCodes.put("sll", "000000");
        functCodes.put("srl", "000010");
        functCodes.put("nor", "100111");
        functCodes.put("xor", "010101");
        functCodes.put("jr", "001000");
        functCodes.put("nop", "000000");
    }

    // First pass: collect all labels and their addresses
    public void firstPass(String[] programLines) {
        currentAddress = 0;
        for (String line : programLines) {
            line = line.trim();
            if (line.isEmpty() || line.startsWith("#")) {
                continue;
            }

            // Check if line contains a label
            if (line.contains(":")) {
                String[] labelParts = line.split(":", 2);
                String label = labelParts[0].trim();
                labelAddresses.put(label, currentAddress);

                // If there's an instruction after the label, store it
                if (labelParts.length > 1 && !labelParts[1].trim().isEmpty()) {
                    String instruction = labelParts[1].trim();
                    instructions.add(instruction);

                    // Check if it's a pseudo-instruction
                    if (instruction.startsWith("bltz") || instruction.startsWith("bgez")
                            || instruction.startsWith("BLTZ") || instruction.startsWith("BGEZ")) {
                        currentAddress += 2; // Increment by 2 for expanded pseudo-instruction
                    } else {
                        currentAddress += 1; // Increment by 1 for regular instruction
                    }
                }
            } else {
                instructions.add(line);

                // Check if it's a pseudo-instruction
                if (line.startsWith("bltz") || line.startsWith("bgez") ||
                        line.startsWith("BLTZ") || line.startsWith("BGEZ")) {
                    currentAddress += 2; // Increment by 2 for expanded pseudo-instruction
                } else {
                    currentAddress += 1; // Increment by 1 for regular instruction
                }
            }
        }
    }

    // Second pass: assemble instructions with resolved labels
    public ArrayList<String> secondPass() throws Exception {
        ArrayList<String> machineCode = new ArrayList<>();
        currentAddress = 0;

        for (String instruction : instructions) {
            if (instruction.startsWith("bltz") || instruction.startsWith("bgez")
                    || instruction.startsWith("BLTZ") || instruction.startsWith("BGEZ")) {
                machineCode.addAll(expandPseudoInstruction(instruction, true));
            } else {
                String assembled = assemble(instruction, false);
                machineCode.add(assembled);
                currentAddress += 1; // Increment by 1 for word-addressable memory
            }
        }

        return machineCode;
    }

    private ArrayList<String> expandPseudoInstruction(String instruction, boolean isPseudo) throws Exception {
        ArrayList<String> expandedInstructions = new ArrayList<>();
        String[] parts = instruction.replace(",", "").split("\\s+");
        String pseudoOp = parts[0].toLowerCase();
        String rs = parts[1].substring(1);
        String label = parts[2];
        String rd1 = "1"; // Using $1 as temporary register
        String rd2 = "2"; // Using $1 as temporary register

        if (pseudoOp.equals("bltz")) {
            // BLTZ (branch on less than zero):
            // Replaces with:
            // slt $1, $rs, $0
            // bne $1, $0, label
            expandedInstructions.add(assemble("slt $" + rd1 + ", $" + rs + ", $0", false));
            expandedInstructions.add(assemble("bne $" + rd1 + ", $0" + ", " + label, true));
        } else if (pseudoOp.equals("bgez")) {
            // bgez (branch on greater than zero):
            // Replaces with:
            // slt $2, $rs, $0
            // beq $2, $0, label
            expandedInstructions.add(assemble("slt $" + rd2 + ", $" + rs + ", $0", false));
            expandedInstructions.add(assemble("beq $" + rd2 + ", $0" + ", " + label, true));
        }

        // Update the current address by the number of instructions added
        currentAddress += expandedInstructions.size();
        isPseudo = true;
        return expandedInstructions;
    }

    private int calculateBranchOffset(String label, boolean isPseudo) throws Exception {
        if (!labelAddresses.containsKey(label)) {
            throw new Exception("Undefined label: " + label);
        }
        // Calculate relative offset in words
        // Subtract (currentAddress + 1) to account for the branch delay slot
        return (labelAddresses.get(label) - (currentAddress + (isPseudo ? 2 : 1)));
    }

    public String assemble(String instructionLine, boolean isPseudo) throws Exception {
        String[] parts = instructionLine.replace(",", "").split("\\s+");
        String instruction = parts[0].toLowerCase();

        if (!opcodes.containsKey(instruction)) {
            throw new Exception("Instruction " + instruction + " is not supported.");
        }

        switch (instruction) {
            case "add":
            case "sub":
            case "and":
            case "or":
            case "slt":
            case "sgt":
            case "nor":
            case "xor":
                if (parts.length != 4) {
                    throw new Exception(
                            "Invalid format for " + instruction + ". Expected: " + instruction + " $rd, $rs, $rt");
                }
                String rd = parts[1].substring(1);
                String rs = parts[2].substring(1);
                String rt = parts[3].substring(1);
                return assembleRType(instruction, rs, rt, rd);

            case "sll":
            case "srl":
                if (parts.length != 4) {
                    throw new Exception(
                            "Invalid format for " + instruction + ". Expected: " + instruction + " $rd, $rt, shamt");
                }
                String rdShift = parts[1].substring(1);
                String rtShift = parts[2].substring(1);
                int shamt = parseImmediate(parts[3]);
                return assembleRTypeShamt(instruction, rtShift, rdShift, shamt);

                case "addi":
                case "ori":
                case "xori":
                case "andi":
                case "slti":
                    if (parts.length != 4) {
                        throw new Exception("Invalid format for " + instruction + ". Expected: " + instruction
                                + " $rt, $rs, immediate/label");
                    }
                    String rt2 = parts[1].substring(1);
                    String rs2 = parts[2].substring(1);
                    
                    // Use a try-catch block to handle both numeric values and labels
                    int immediate;
                    String immOrLabel = parts[3];
                    try {
                        // Try to parse as a number first
                        if (immOrLabel.startsWith("0x")) {
                            immediate = Integer.parseInt(immOrLabel.substring(2), 16);
                        } else if (immOrLabel.startsWith("0b")) {
                            immediate = Integer.parseInt(immOrLabel.substring(2), 2);
                        } else if (immOrLabel.length() > 1 && immOrLabel.startsWith("0")) {
                            immediate = Integer.parseInt(immOrLabel.substring(1), 8);
                        } else {
                            immediate = Integer.parseInt(immOrLabel);
                        }
                    } catch (NumberFormatException e) {
                        // If parsing as a number fails, check if it's a valid label
                        if (labelAddresses.containsKey(immOrLabel)) {
                            immediate = labelAddresses.get(immOrLabel);
                        } else {
                            throw new Exception("Invalid immediate value or undefined label: " + immOrLabel);
                        }
                    }
                    return assembleIType(instruction, rs2, rt2, immediate);

            case "beq":
            case "bne":
                if (parts.length != 4) {
                    throw new Exception(
                            "Invalid format for " + instruction + ". Expected: " + instruction + " $rs, $rt, label");
                }
                String rs3 = parts[1].substring(1);
                String rt3 = parts[2].substring(1);
                int offset = calculateBranchOffset(parts[3], isPseudo);
                return assembleIType(instruction, rs3, rt3, offset);

            case "lw":
            case "sw":
                if (parts.length != 3) {
                    throw new Exception(
                            "Invalid format for " + instruction + ". Expected: " + instruction + " $rt, offset($rs)");
                }
                String rt4 = parts[1].substring(1);
                String[] offsetAndReg = parts[2].split("\\(");
                if (offsetAndReg.length != 2) {
                    throw new Exception("Invalid memory access format for " + instruction);
                }
                int offset2 = parseImmediate(offsetAndReg[0]);
                String rs4 = offsetAndReg[1].substring(1, offsetAndReg[1].length() - 1);
                return assembleIType(instruction, rs4, rt4, offset2);

            case "jal":
            case "j":
                if (parts.length != 2) {
                    throw new Exception("Invalid format for " + instruction + ". Expected: " + instruction + " label");
                }
                if (!labelAddresses.containsKey(parts[1])) {
                    throw new Exception("Undefined label: " + parts[1]);
                }
                // For J-type instructions, we use the absolute address directly
                int address = labelAddresses.get(parts[1]);
                return assembleJType(instruction, address);

            case "jr":
                if (parts.length != 2) {
                    throw new Exception("Invalid format for jr. Expected: jr $rs");
                }
                String rsJr = parts[1].substring(1);
                return assembleRType(instruction, rsJr, "0", "0");
            case "nop":
                return assembleRTypeShamt(instruction, "0", "0", 0);

            default:
                throw new Exception("Instruction " + instruction + " is not supported.");
        }
    }

    // Existing helper methods remain the same
    public String regToBinary(String reg) {
        int regNumber = Integer.parseInt(reg);
        return toBinary(regNumber, 5);
    }

    public static String toBinary(int value, int bits) {
        String binaryString = Integer.toBinaryString(value);
        if (binaryString.length() > bits) {
            return binaryString.substring(binaryString.length() - bits);
        }
        return String.format("%" + bits + "s", binaryString).replace(' ', '0');
    }

    public String assembleRType(String instruction, String rs, String rt, String rd) {
        String opcode = opcodes.get(instruction);
        String funct = functCodes.get(instruction);
        return opcode + regToBinary(rs) + regToBinary(rt) + regToBinary(rd) + "00000" + funct;
    }

    public String assembleRTypeShamt(String instruction, String rt, String rd, int shamt) {
        String opcode = opcodes.get(instruction);
        String funct = functCodes.get(instruction);
        return opcode + "00000" + regToBinary(rt) + regToBinary(rd) + toBinary(shamt, 5) + funct;
    }

    public String assembleIType(String instruction, String rs, String rt, int immediate) {
        String opcode = opcodes.get(instruction);
        return opcode + regToBinary(rs) + regToBinary(rt) + toBinary(immediate, 16);
    }

    public String assembleJType(String instruction, int address) {
        String opcode = opcodes.get(instruction);
        return opcode + toBinary(address, 26);
    }

    // Update the parseImmediate method to handle more formats
    private int parseImmediate(String value) throws NumberFormatException {
        value = value.toLowerCase().trim();
        if (value.startsWith("0x")) {
            return Integer.parseInt(value.substring(2), 16);
        } else if (value.startsWith("0b")) {
            return Integer.parseInt(value.substring(2), 2);
        } else if (value.length() > 1 && value.startsWith("0")) {
            return Integer.parseInt(value.substring(1), 8);
        } else {
            return Integer.parseInt(value);
        }
    }
    public static int stringToInt(String input) {
        String str = input.trim().toLowerCase();
        
        try {
            //Hex number
            if (str.startsWith("0x") || str.startsWith("#")) {
                return Integer.parseInt(str.substring(2), 16);
            }
            
            //binary number 
            if (str.startsWith("0b")) {
                return Integer.parseInt(str.substring(2), 2);
            }
            
            //binary without prefix (only 0s and 1s)
            if (str.matches("[01]+")) {
                return Integer.parseInt(str, 2);
            }
            
            //octal number (starts with 0)
            if (str.startsWith("0") && str.length() > 1) {
                return Integer.parseInt(str.substring(1), 8);
            }
            
            //decimal
            return Integer.parseInt(str);
            
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Invalid number format: " + input);
        }
    }
    public static void dataMemConversion (){
        List <String> dataMemNumbers=new ArrayList<>();
        try{
        BufferedReader reader = Files.newBufferedReader(Paths.get("data_content.txt"));
        while (reader.ready()) {
            dataMemNumbers.add(reader.readLine());
        }
        reader.close();
        }catch(Exception e){
            e.printStackTrace();
        }
        List<Integer> numbers = new ArrayList<>();
        for (String string : dataMemNumbers) {
            numbers.add(stringToInt(string));
        }
        List <String> dataMemList = new ArrayList<>();
        try{
            BufferedWriter dataMemWriter = Files.newBufferedWriter(Paths.get("../Cycle Accurate Simulator/data_mem.txt"));
            int address= 0;
            for (int number : numbers) {
                dataMemWriter.write(String.valueOf(number));
                dataMemWriter.newLine();
                address++;
            }
            while (address<4096) {
                dataMemWriter.write("0");
                dataMemWriter.newLine();
                address++;
            }
            dataMemWriter.close();
        }catch(Exception e){
            e.printStackTrace();
        }
        for (int number : numbers) {
           dataMemList.add(toBinary(number, 32));
        }
        try (BufferedWriter writer = Files.newBufferedWriter(Paths.get("../testbenches/dual_issue_data_memory.mif"))) {
            writer.write("WIDTH=32;");
            writer.newLine();
            writer.write("DEPTH=4096;");
            writer.newLine();
            writer.write("ADDRESS_RADIX=UNS;");
            writer.newLine();
            writer.write("DATA_RADIX=BIN;");
            writer.newLine();
            writer.write("CONTENT BEGIN");
            writer.newLine();
            int addr = 0;
            // Write actual instructions
            for (String code : dataMemList) {
                writer.write("  "+addr +" : " +code +";");
                writer.newLine();
                addr++;
            }
            // Fill remaining lines with zeros up to 512
            if (addr < 4096) {
                writer.write(" ["+addr+"..4095] : 00000000000000000000000000000000; -- fill the rest with zeros ");
                writer.newLine();
                addr++;
            }
            writer.write("END;");
            writer.newLine();
        }
        catch(Exception e){
            e.printStackTrace();
        }
        try (BufferedWriter writer = Files.newBufferedWriter(Paths.get("../SuperScalar/dual_issue_data_memory.mif"))) {
            writer.write("WIDTH=32;");
            writer.newLine();
            writer.write("DEPTH=4096;");
            writer.newLine();
            writer.write("ADDRESS_RADIX=UNS;");
            writer.newLine();
            writer.write("DATA_RADIX=BIN;");
            writer.newLine();
            writer.write("CONTENT BEGIN");
            writer.newLine();
            int addr = 0;
            // Write actual instructions
            for (String code : dataMemList) {
                writer.write("  "+addr +" : " +code +";");
                writer.newLine();
                addr++;
            }
            // Fill remaining lines with zeros up to 512
            if (addr < 4096) {
                writer.write(" ["+addr+"..4095] : 00000000000000000000000000000000; -- fill the rest with zeros ");
                writer.newLine();
                addr++;
            }
            writer.write("END;");
            writer.newLine();
        }
        catch(Exception e){
            e.printStackTrace();
        }

    }
    public static void main(String[] args) {
        try {
            dataMemConversion();
            Assembler assembler = new Assembler();
            List<String> lines = Files.readAllLines(Paths.get("scheduled_output.txt"));
            String[] scheduledProgram = lines.toArray(new String[0]);
           
            assembler.firstPass(scheduledProgram);
            ArrayList<String> machineCode = assembler.secondPass();

            try (BufferedWriter writer = Files.newBufferedWriter(Paths.get("../Cycle Accurate Simulator/ins_mem.txt"))) {
                int addr = 0;
                // Write actual instructions
                for (String code : machineCode) {
                    writer.write(code);
                    writer.newLine();
                    addr++;
                }
                
                // Fill remaining lines with zeros up to 512
                String zeros = "00000000000000000000000000000000";
                while (addr < 512) {
                    writer.write(zeros);
                    writer.newLine();
                    addr++;
                }
            }

            // System.out.println("Label Addresses:");
            // for (String label : assembler.labelAddresses.keySet()) {
            //     int address = assembler.getLabelAddress(label);
            //     System.out.printf("Label %s : Address %d\n", label, address);
            // }
            // System.out.println("*****************************************************");
            System.out.println("WIDTH=32;");
            System.out.println("DEPTH=512;");
            System.out.println("ADDRESS_RADIX=UNS;");
            System.out.println("DATA_RADIX=BIN;");
            System.out.println("CONTENT BEGIN");

            int addr = 0;
            for (String code : machineCode) {
                System.out.printf("    %d   : %s;\n", addr++, code);
            }

            if (addr < 512) {
                System.out.printf("    [%d..511] : %s;  -- fill the rest with zeros\n",
                        addr, "00000000000000000000000000000000");
            }

            System.out.println("END;");

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }

    public int getLabelAddress(String label) {
        return labelAddresses.getOrDefault(label, -1);
    }
}
