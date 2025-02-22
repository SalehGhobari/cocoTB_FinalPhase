module controlUnit_tb;

    // Inputs
    reg [5:0] opCode1, funct1, opCode2, funct2;

    // Outputs
    wire Branch1, MemReadEn1, MemWriteEn1, RegWriteEn1, ALUSrc1, Jump1, PcSrc1;
    wire Branch2, MemReadEn2, MemWriteEn2, RegWriteEn2, ALUSrc2, Jump2, PcSrc2;
    wire [1:0] MemtoReg1, RegDst1, MemtoReg2, RegDst2;
    wire [3:0] ALUOp1, ALUOp2;

    // Instantiate the control unit
    controlUnit uut (
        .opCode1(opCode1), .funct1(funct1),
        .opCode2(opCode2), .funct2(funct2),
        .Branch1(Branch1), .MemReadEn1(MemReadEn1), .MemWriteEn1(MemWriteEn1), .RegWriteEn1(RegWriteEn1),
        .ALUSrc1(ALUSrc1), .Jump1(Jump1), .PcSrc1(PcSrc1),
        .Branch2(Branch2), .MemReadEn2(MemReadEn2), .MemWriteEn2(MemWriteEn2), .RegWriteEn2(RegWriteEn2),
        .ALUSrc2(ALUSrc2), .Jump2(Jump2), .PcSrc2(PcSrc2),
        .MemtoReg1(MemtoReg1), .RegDst1(RegDst1),
        .MemtoReg2(MemtoReg2), .RegDst2(RegDst2),
        .ALUOp1(ALUOp1), .ALUOp2(ALUOp2)
    );
function [128*8:1] get_instruction_name(input [5:0] opCode, input [5:0] funct);
    case (opCode)
        6'h0: case (funct)
            6'h20: get_instruction_name = "add     ";
            6'h22: get_instruction_name = "sub     ";
            6'h24: get_instruction_name = "and     ";
            default: get_instruction_name = "R-type  ";
        endcase
        6'h8: get_instruction_name = "addi    ";
        6'h23: get_instruction_name = "lw      ";
        6'h2b: get_instruction_name = "sw      ";
        6'h4: get_instruction_name = "beq     ";
        6'h5: get_instruction_name = "bne     ";
        6'h2: get_instruction_name = "j       ";
        6'h3: get_instruction_name = "jal     ";
        6'hd: get_instruction_name = "ori     ";
        default: get_instruction_name = "unknown ";
    endcase
endfunction

initial begin
    $monitor(
        "Time = %0t: Instruction1 = %-8s (opCode1 = %02h, funct1 = %02h), Instruction2 = %-8s (opCode2 = %02h, funct2 = %02h)\n\
        Branch1 = %d, MemReadEn1 = %d, MemWriteEn1 = %d, RegWriteEn1 = %d, ALUSrc1 = %d, Jump1 = %d, PcSrc1 = %d\n\
        Branch2 = %d, MemReadEn2 = %d, MemWriteEn2 = %d, RegWriteEn2 = %d, ALUSrc2 = %d, Jump2 = %d, PcSrc2 = %d\n\
        MemtoReg1 = %2d, RegDst1 = %2d, MemtoReg2 = %2d, RegDst2 = %2d\n\
        ALUOp1 = %4b, ALUOp2 = %4b",
        $time, 
        get_instruction_name(opCode1, funct1), opCode1, funct1,
        get_instruction_name(opCode2, funct2), opCode2, funct2,
        Branch1, MemReadEn1, MemWriteEn1, RegWriteEn1, 
        ALUSrc1, Jump1, PcSrc1,
        Branch2, MemReadEn2, MemWriteEn2, RegWriteEn2, 
        ALUSrc2, Jump2, PcSrc2,
        MemtoReg1, RegDst1, MemtoReg2, RegDst2,
        ALUOp1, ALUOp2
    );


        // Test case 1: R-type (add) and I-type (addi)
        opCode1 = 6'h0; funct1 = 6'h20; // add
        opCode2 = 6'h8; funct2 = 6'h0;  // addi
        #10;

        // Test case 2: Load (lw) and Store (sw)
        opCode1 = 6'h23; funct1 = 6'h0; // lw
        opCode2 = 6'h2b; funct2 = 6'h0; // sw
        #10;

        // Test case 3: Branch (beq) and Jump (j)
        opCode1 = 6'h4; funct1 = 6'h0;  // beq
        opCode2 = 6'h2; funct2 = 6'h0;  // j
        #10;

        // Test case 4: R-type (sub) and I-type (ori)
        opCode1 = 6'h0; funct1 = 6'h22; // sub
        opCode2 = 6'h0d; funct2 = 6'h0; // ori
        #10;

        // Test case 5: Jump and Link (jal) and R-type (and)
        opCode1 = 6'h3; funct1 = 6'h0;  // jal
        opCode2 = 6'h0; funct2 = 6'h24; // and
        #10;

        // End simulation
        $finish;
    end

endmodule
