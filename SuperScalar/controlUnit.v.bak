module controlUnit(opCode1, funct1, opCode2, funct2, Branch1, MemReadEn1, MemWriteEn1, RegWriteEn1, ALUSrc1, Jump1, PcSrc1,
 Branch2, MemReadEn2, MemWriteEn2, RegWriteEn2, ALUSrc2, Jump2, PcSrc2, MemtoReg1, RegDst1, MemtoReg2, RegDst2, ALUOp1, ALUOp2
);


	 input  [5:0] opCode1, funct1, opCode2, funct2;
    output reg Branch1, MemReadEn1, MemWriteEn1, RegWriteEn1, ALUSrc1, Jump1, PcSrc1;
    output reg Branch2, MemReadEn2, MemWriteEn2, RegWriteEn2, ALUSrc2, Jump2, PcSrc2;
    output reg [1:0] MemtoReg1, RegDst1, MemtoReg2, RegDst2;
    output reg [3:0] ALUOp1, ALUOp2;
    // Parameters for opCodes and functions
    parameter _RType = 6'h0, _addi = 6'h8, _lw = 6'h23, _sw = 6'h2b, _beq = 6'h4, _bne = 6'h5, _jal=6'h03, _ori=6'h0d, _xori=6'h16;
    parameter _add_ = 6'h20, _sub_ = 6'h22, _and_ = 6'h24, _or_ = 6'h25, _slt_ = 6'h2a, _sgt_ = 6'h14, _sll_ = 6'h00, _srl_ = 6'h02,
	 _nor_ = 6'h27, _xor_ = 6'h15, _jr_ = 6'h08, _andi = 6'hc, _slti = 6'ha, _j = 6'h2;

    // Unit logic - generate signals for dual issue
    always @(*) begin
        // Default values
        {RegDst1, Branch1, MemReadEn1, MemtoReg1, MemWriteEn1, RegWriteEn1, ALUSrc1, Jump1, PcSrc1, ALUOp1} = 0;
        {RegDst2, Branch2, MemReadEn2, MemtoReg2, MemWriteEn2, RegWriteEn2, ALUSrc2, Jump2, PcSrc2, ALUOp2} = 0;

        // Decode first instruction
        case(opCode1)
            _RType: begin
                RegDst1 = 2'b01;
                RegWriteEn1 = 1'b1;
                case (funct1)
                    _add_: ALUOp1 = 4'b0000;
                    _sub_: ALUOp1 = 4'b0001;
                    _and_: ALUOp1 = 4'b0010;
                    _or_:  ALUOp1 = 4'b0011;
                    _slt_: ALUOp1 = 4'b0100;
                    _sgt_: ALUOp1 = 4'b0101;
                    _nor_: ALUOp1 = 4'b0110;
                    _xor_: ALUOp1 = 4'b0111;
                    _sll_: ALUOp1 = 4'b1000;
                    _srl_: ALUOp1 = 4'b1001;
                    _jr_: PcSrc1 = 1'b1;
                    default: ;
                endcase
            end
            _addi: begin
                ALUOp1 = 4'b0000;
                ALUSrc1 = 1'b1;
                RegWriteEn1 = 1'b1;
            end
            _lw: begin
                MemReadEn1 = 1'b1;
                MemtoReg1 = 2'b01;
                ALUSrc1 = 1'b1;
                RegWriteEn1 = 1'b1;
            end
            _sw: begin
                MemWriteEn1 = 1'b1;
                ALUSrc1 = 1'b1;
            end
            _beq, _bne: begin
                Branch1 = 1'b1;
                ALUOp1 = 4'b0001;
            end
            _jal: begin
                Jump1 = 1'b1;
                PcSrc1 = 1'b1;
                RegWriteEn1 = 1'b1;
                RegDst1 = 2'b10;
                MemtoReg1 = 2'b10;
            end
            _j: begin
                Jump1 = 1'b1;
                PcSrc1 = 1'b1;
            end
            default: ;
        endcase

        // Decode second instruction
        case(opCode2)
            _RType: begin
                RegDst2 = 2'b01;
                RegWriteEn2 = 1'b1;
                case (funct2)
                    _add_: ALUOp2 = 4'b0000;
                    _sub_: ALUOp2 = 4'b0001;
                    _and_: ALUOp2 = 4'b0010;
                    _or_:  ALUOp2 = 4'b0011;
                    _slt_: ALUOp2 = 4'b0100;
                    _sgt_: ALUOp2 = 4'b0101;
                    _nor_: ALUOp2 = 4'b0110;
                    _xor_: ALUOp2 = 4'b0111;
                    _sll_: ALUOp2 = 4'b1000;
                    _srl_: ALUOp2 = 4'b1001;
                    _jr_: PcSrc2 = 1'b1;
                    default: ;
                endcase
            end
            _addi: begin
                ALUOp2 = 4'b0000;
                ALUSrc2 = 1'b1;
                RegWriteEn2 = 1'b1;
            end
            _lw: begin
                MemReadEn2 = 1'b1;
                MemtoReg2 = 2'b01;
                ALUSrc2 = 1'b1;
                RegWriteEn2 = 1'b1;
            end
            _sw: begin
                MemWriteEn2 = 1'b1;
                ALUSrc2 = 1'b1;
            end
            _beq, _bne: begin
                Branch2 = 1'b1;
                ALUOp2 = 4'b0001;
            end
            _jal: begin
                Jump2 = 1'b1;
                PcSrc2 = 1'b1;
                RegWriteEn2 = 1'b1;
                RegDst2 = 2'b10;
                MemtoReg2 = 2'b10;
            end
            _j: begin
                Jump2 = 1'b1;
                PcSrc2 = 1'b1;
            end
            default: ;
        endcase
    end
endmodule