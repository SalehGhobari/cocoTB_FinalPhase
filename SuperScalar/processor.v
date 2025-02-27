module processor(clk, rst, PC, enable);

//inputs
input clk, rst, enable;

//outputs
output [7:0] PC;

//FETCH AND RANDOM WIRES
wire StallOut;
wire Branch1, MemReadEn1, MemWriteEn1, RegWriteEn1, ALUSrc1, Jump1, PcSrc1, ForwardBranchA, ForwardBranchB;
wire Branch2, MemReadEn2, MemWriteEn2, RegWriteEn2, ALUSrc2, Jump2, PcSrc2;
wire prediction1, prediction2, CPCSignal1, CPCSignal2, branch_taken1, branch_taken2,EnablePCIFID, IFID1Reset, ID21Reset, ID22Reset, EX2Reset, Stall;
wire Stall11, Stall12, Stall21, Stall22, StallJr, FlushIFID1, FlushEX,FlushMEM2, overflow1, overflow2, zero1, zero2, xnorOut1, xnorOut2;
wire [2:0] ForwardA1, ForwardA2, ForwardB1, ForwardB2;
wire [1:0] MemtoReg1, RegDst1, MemtoReg2, RegDst2;
wire [3:0] ALUOp1, ALUOp2;
wire [4:0] readRegister1, readRegister2, readRegister3, readRegister4;
wire [4:0] writeRegister1, writeRegister2, rd1, rd2, rs1, rs2, rt1, rt2, shamt1, shamt2;
wire [5:0] opCode1, opCode2, funct1, funct2;
wire [15:0] imm1, imm2;
wire [31:0] writeData1, writeData2, readData1, readData2, readData3, readData4;
wire [31:0] extImm1, extImm2, instr1, instr2;
wire [31:0] memoryReadData1, memoryReadData2;
wire [7:0] PCPlus1, PCPlus2,PCPlus1D1,PCPlus1D,PCPlus1E, branchAdderResult1, branchAdderResult2, nextPCP1;
wire [7:0] CorrectedPC1, CorrectedPC2,  branchAdderPC, instMemMuxOut, predictedTarget1, predictedTarget2, instMemTarget;

//DECODE WIRES
wire RegWriteEn1D, RegWriteEn2D, bit26_1, bit26_2, CPCSig;
wire Branch1D, MemReadEn1D, MemWriteEn1D, ALUSrc1D, Jump1D, PcSrc1D;
wire Branch2D, MemReadEn2D, MemWriteEn2D, ALUSrc2D, Jump2D, PcSrc2D;
wire prediction1D1, prediction2D1, prediction1D, prediction2D, prediction1New, prediction2New;
wire [1:0] MemtoReg1D, RegDst1D, MemtoReg2D, RegDst2D;
wire [3:0] ALUOp1D, ALUOp2D;
wire [31:0] instr1D, instr2D;
wire [7:0] PCPlus2D1, PCD1, branchAdderResult1D1, branchAdderResult2D1;
wire [7:0] PCPlus2D, PCD, branchAdderResult1D, branchAdderResult2D;

//EXECUTE WIRES
wire Branch1E, Branch2E, prediction1E, prediction2E, bit26_1E, bit26_2E;
wire MemReadEn1E, MemWriteEn1E, RegWriteEn1E, ALUSrc1E;
wire MemReadEn2E, MemWriteEn2E, RegWriteEn2E, ALUSrc2E;
wire [1:0] MemToReg1E, RegDst1E, MemToReg2E, RegDst2E;
wire [3:0] ALUOp1E, ALUOp2E;
wire [4:0] writeRegister1E, writeRegister2E;
wire [7:0] PCPlus2E,PCE, branchAdderResult1E, branchAdderResult2E;
wire [31:0] extImm1E, extImm2E;
wire [4:0] rs1E, rt1E, rd1E, shamt1E;
wire [4:0] rs2E, rt2E, rd2E, shamt2E;
wire [31:0] readData1E, readData2E, readData3E, readData4E;
wire [31:0] ForwardAMuxOut1, ForwardBMuxOut1, ForwardAMuxOut2, ForwardBMuxOut2;
wire [31:0] ALUin1, ALUin2, ALUResult1, ALUResult2;

//MEMORY WIRES
wire RegWriteEn1M, RegWriteEn2M, Branch1M, Branch2M, bit26_1M, bit26_2M, prediction1M, prediction2M;
wire MemWriteEn1M, MemReadEn1M, MemWriteEn2M, MemReadEn2M;
wire [1:0] MemToReg1M, MemToReg2M;
wire [7:0] PCPlus2M, PCM, PCPlus1M, branchAdderResult1M, branchAdderResult2M;
wire [31:0] ALUResult1M, ALUResult2M;
wire [31:0] ForwardBMuxOut1M, ForwardBMuxOut2M, ForwardAMuxOut1M, ForwardAMuxOut2M, comp2MuxAout, comp2MuxBout;
wire [4:0] writeRegister1M, writeRegister2M, rs2M, rt2M;

//WRITEBACK WIRES
wire RegWriteEn1W, RegWriteEn2W, instMemPred;
wire [1:0] MemToReg1W, MemToReg2W;
wire [7:0] PCPlus2W, PCPlus1W;
wire [31:0] ALUResult1W, ALUResult2W;
wire [31:0] memoryReadData1W, memoryReadData2W;
wire [4:0] writeRegister1W, writeRegister2W;


assign opCode1 = instr1D[31:26];
assign rd1 = instr1D[15:11]; 
assign rs1 = instr1D[25:21];  
assign shamt1 = instr1D[10:6];
assign rt1 = instr1D[20:16];  
assign imm1 = instr1D[15:0];
assign funct1 = instr1D[5:0];
assign bit26_1 =instr1D[26];

assign opCode2 = instr2D[31:26];
assign rd2 = instr2D[15:11]; 
assign rs2 = instr2D[25:21];  
assign shamt2 = instr2D[10:6];
assign rt2 = instr2D[20:16];  
assign imm2 = instr2D[15:0];
assign funct2 = instr2D[5:0];
assign bit26_2 =instr2D[26];

/**************************************************************FETCH STAGE*********************************************/

reg [7:0] jumpMuxOut1, jumpMuxOut2, jumpMuxOut;
reg [7:0] branchMuxOut1, branchMuxOut2, branchMuxOut;
reg [7:0] BJPC, CPC, nextPC;

// === Jump MUXes ===

// jump1Mux: selects between readData1 and instr1D based on Jump1
always @(*) begin
    if (Jump1)
        jumpMuxOut1 = instr1D[7:0];
    else
        jumpMuxOut1 = readData1[7:0];
end

// jump2Mux: selects between readData3 and instr2D based on Jump2
always @(*) begin
    if (Jump2)
        jumpMuxOut2 = instr2D[7:0];
    else
        jumpMuxOut2 = readData3[7:0];
end

// jumpMux: selects between jumpMuxOut1 and jumpMuxOut2 based on Jump2
always @(*) begin
    if (PcSrc2)
        jumpMuxOut = jumpMuxOut2;
    else
        jumpMuxOut = jumpMuxOut1;
end

// === Branch MUXes ===

// branch1Mux: selects between PCPlus2 and branchAdderPC based on prediction1
always @(*) begin
    if (prediction1)
        branchMuxOut1 = branchAdderPC;
    else
        branchMuxOut1 = PCPlus2;
end

// branch2Mux: selects between PCPlus2 and branchAdderResult2 based on prediction2
always @(*) begin
    if (prediction2)
        branchMuxOut2 = branchAdderResult2;
    else
        branchMuxOut2 = PCPlus2;
end

// branchMux: selects between branchMuxOut1 and branchMuxOut2 based on prediction2
always @(*) begin
    if (prediction2)
        branchMuxOut = branchMuxOut2;
    else
        branchMuxOut = branchMuxOut1;
end

// pcMux: selects between branchMuxOut and jumpMuxOut based on (PcSrc1 | PcSrc2)
always @(*) begin
    if ((PcSrc1 | PcSrc2))
        BJPC = jumpMuxOut;
    else
        BJPC = branchMuxOut;
end

// cpcMux: selects between CorrectedPC1 and CorrectedPC2 based on CPCSignal2
always @(*) begin
    if (CPCSignal2)
        CPC = CorrectedPC2;
    else
        CPC = CorrectedPC1;
end

// nexPcMux: selects between BJPC and CPC based on (CPCSignal1 | CPCSignal2)
always @(*) begin
    if (CPCSignal1 | CPCSignal2)
        nextPC = CPC;
    else
        nextPC = BJPC;
end

programCounter pc(.clk(clk), .rst(rst), .enable(EnablePCIFID), .PCin(nextPC), .PCout(PC));

adder #(8)	branchPcAdder(.in1(predictedTarget1),.in2(8'd1),.out(branchAdderPC));
adder #(8) nextPcAdder(.in1(nextPC), .in2(8'd1), .out(nextPCP1));
adder #(8) pcAdder(.in1(PC), .in2(8'd2), .out(PCPlus2));
adder #(8) pcAdder2(.in1(PC), .in2(8'd1), .out(PCPlus1));

mux2x1En #(8) instMemMux(.in1(nextPCP1), .in2(instMemTarget), .s(instMemPred),.en(EnablePCIFID), .out(instMemMuxOut));

dual_issue_inst_mem instMem(.address_a(nextPC),
							.address_b(instMemMuxOut),
							.addressstall_a(~EnablePCIFID),
							.addressstall_b(~EnablePCIFID),
							.enable (EnablePCIFID),
							.clock(clk),
							.q_a(instr1),
							.q_b(instr2));

adder #(8) branchAdder1(.in1(PCPlus1), .in2(instr1[7:0]), .out(branchAdderResult1));
adder #(8) branchAdder2(.in1(PCPlus2), .in2(instr2[7:0]), .out(branchAdderResult2));

BranchPredictionUnit BPU (
   .clk(clk), .reset(rst), .branch1(Branch1M), .branch2(Branch2M), .branch_taken1(branch_taken1), .branch_taken2(branch_taken2), 
    .pc1(PC), .pc2(PCPlus1), .pcM1(PCM), .pcM2(PCPlus1M), .targetM1(branchAdderResult1M), .targetM2(branchAdderResult2M), .prediction1(prediction1), .prediction2(prediction2), 
	 .nextPC(nextPC), .instMemPred(instMemPred), .predictedTarget1(predictedTarget1), .instMemTarget(instMemTarget)
);


pipe #(106) IF_ID(.D({PCPlus2,PCPlus1,PC,branchAdderResult1,branchAdderResult2, prediction1, prediction2, instr1, instr2}), 
		.Q({PCPlus2D,PCPlus1D,PCD,branchAdderResult1D,branchAdderResult2D, prediction1New, prediction2New, instr1D, instr2D}), 
		.clk(clk), .reset(rst), .enable(EnablePCIFID), .flush(FlushIFID1)); 




/***********************************************************************DECODE STAGE*************************************************************/


controlUnit CU1(.opCode(opCode1), .funct(funct1),
				    .Branch(Branch1D), .MemReadEn(MemReadEn1D), .MemWriteEn(MemWriteEn1D), .RegWriteEn(RegWriteEn1D),
					 .ALUSrc(ALUSrc1D), .Jump(Jump1D), .PcSrc(PcSrc1D),  .MemtoReg(MemtoReg1D), .RegDst(RegDst1D), .ALUOp(ALUOp1D));
				   
mux2x1 #(16) CUMux1(.in1({PcSrc1D,Jump1D,RegWriteEn1D, MemtoReg1D, MemWriteEn1D, MemReadEn1D, ALUOp1D, RegDst1D, ALUSrc1D, Branch1D, prediction1New}), .in2(16'b0), .s(Stall),
						  .out({PcSrc1,Jump1,RegWriteEn1, MemtoReg1, MemWriteEn1, MemReadEn1, ALUOp1, RegDst1, ALUSrc1, Branch1, prediction1D}));
 
controlUnit CU2 (
					  .opCode(opCode2), .funct(funct2),
					  .Branch(Branch2D), .MemReadEn(MemReadEn2D), .MemWriteEn(MemWriteEn2D), .RegWriteEn(RegWriteEn2D), 
					  .ALUSrc(ALUSrc2D), .Jump(Jump2D), .PcSrc(PcSrc2D), .MemtoReg(MemtoReg2D), .RegDst(RegDst2D), .ALUOp(ALUOp2D));
					  

mux2x1 #(16) CUMux2(.in1({PcSrc2D,Jump2D,RegWriteEn2D, MemtoReg2D, MemWriteEn2D, MemReadEn2D, ALUOp2D, RegDst2D, ALUSrc2D, Branch2D, prediction2New}), .in2(16'b0), .s(Stall),
						  .out({PcSrc2,Jump2,RegWriteEn2, MemtoReg2, MemWriteEn2, MemReadEn2, ALUOp2, RegDst2, ALUSrc2, Branch2, prediction2D}));
					  
registerFile RegFile (
     .clk(clk), .rst(rst), .we1(RegWriteEn1W), .we2(RegWriteEn2W), .readRegister1(rs1), .readRegister2(rt1), .readRegister3(rs2)
	  , .readRegister4(rt2),.writeRegister1(writeRegister1W), .writeRegister2(writeRegister2W), 
	  .writeData1(writeData1), .writeData2(writeData2), .readData1(readData1), .readData2(readData2), .readData3(readData3), .readData4(readData4));


signextender SignExtend1(.in1(imm1), .out(extImm1));
signextender SignExtend2(.in1(imm2), .out(extImm2));


HazardDetectionUnit HDU(
    .takenBranch1(branch_taken1), .takenBranch2(branch_taken2), .pcSrc1(PcSrc1), .pcSrc2(PcSrc2), .opcode1(opCode1), .opcode2(opCode2), .funct1(funct1), .funct2(funct2), .memReadE1(MemReadEn1E), .memReadE2(MemReadEn2E), 
    .branch1(Branch1M), .branch2(Branch2M), .predictionE1(prediction1M), .predictionE2(prediction2M), .writeRegisterE1(writeRegister1E), .writeRegisterE2(writeRegister2E), .writeRegisterM1(writeRegister1M), .writeRegisterM2(writeRegister2M), 
    .rsD1(rs1), .rtD1(rt1), .rsD2(rs2), .rtD2(rt2), .Stall11(Stall11), .Stall21(Stall21), .StallJr(StallJr), .Stall12(Stall12), .Stall22(Stall22), 
	 .FlushIFID1(FlushIFID1), .FlushEX(FlushEX),.FlushMEM2(FlushMEM2), .CPCSignal1(CPCSignal1), .CPCSignal2(CPCSignal2)
);

ORGate CPCGate(.in1(CPCSignal1), .in2(CPCSignal2), .out(CPCSig));
ORGate5 hold(.in1(Stall21), .in2(Stall22), .in3(Stall12), .in4(Stall11), .in5(StallJr), .out(Stall));
ANDGate holdGate(.in1(~Stall), .in2(enable), .out(StallOut));
ORGate enableGate(.in1(StallOut), .in2(CPCSig), .out(EnablePCIFID));

pipe #(163) ID_EX_1(
    .D({
        PCD,PCPlus1D, PCPlus2D, branchAdderResult1D, bit26_1, Branch1, MemReadEn1, MemWriteEn1, MemtoReg1, RegWriteEn1, ALUOp1,
		  RegDst1, ALUSrc1, readData1, readData2,extImm1, rs1, rt1, rd1, shamt1, prediction1D
    }),
    .Q({
        PCE,PCPlus1E, PCPlus2E, branchAdderResult1E, bit26_1E, Branch1E, MemReadEn1E, MemWriteEn1E, MemToReg1E, RegWriteEn1E, ALUOp1E, 
		  RegDst1E, ALUSrc1E, readData1E, readData2E, extImm1E, rs1E, rt1E, rd1E, shamt1E, prediction1E 
    }), 
    .clk(clk), .reset(rst), .enable(enable), .flush(FlushEX)
);

pipe #(139) ID_EX_2(
    .D({
         branchAdderResult2D, bit26_2, Branch2, MemReadEn2, MemWriteEn2, MemtoReg2, RegWriteEn2, ALUOp2,
		  RegDst2, ALUSrc2, readData3, readData4, extImm2, rs2, rt2, rd2, shamt2, prediction2D
    }),
    .Q({
         branchAdderResult2E,bit26_2E, Branch2E, MemReadEn2E, MemWriteEn2E, MemToReg2E, RegWriteEn2E, ALUOp2E,
		  RegDst2E, ALUSrc2E, readData3E, readData4E, extImm2E, rs2E, rt2E, rd2E, shamt2E, prediction2E
    }), 
    .clk(clk), .reset(rst), .enable(enable), .flush(FlushEX|PcSrc1)
);


/**************************************************************EXECUTE STAGE*********************************************/

mux3to1 #(5) RFMux1(.in1(rt1E), .in2(rd1E), .in3(5'b11111), .s(RegDst1E), .out(writeRegister1E));
mux3to1 #(5) RFMux2(.in1(rt2E), .in2(rd2E), .in3(5'b11111), .s(RegDst2E), .out(writeRegister2E));

ForwardingUnit FU (.rsE1(rs1E), .rtE1(rt1E), .rsE2(rs2E), .rtE2(rt2E), .rsM2(rs2M), .rtM2(rt2M), .writeRegisterM1(writeRegister1M),
						 .writeRegisterM2(writeRegister2M), .writeRegisterW1(writeRegister1W), .writeRegisterW2(writeRegister2W), 
						.regWriteM1(RegWriteEn1M), .regWriteM2(RegWriteEn2M), .regWriteW1(RegWriteEn1W), .regWriteW2(RegWriteEn2W), .branch2M(Branch2M),
						.ForwardA1(ForwardA1), .ForwardB1(ForwardB1), .ForwardA2(ForwardA2), .ForwardB2(ForwardB2), .ForwardBranchA(ForwardBranchA), .ForwardBranchB(ForwardBranchB));


mux5to1 #(32) ForwardA1Mux(.in1(readData1E), .in2(ALUResult1M),.in3(ALUResult2M), .in4(writeData1),.in5(writeData2), .s(ForwardA1), .out(ForwardAMuxOut1));
mux5to1 #(32) ForwardB1Mux(.in1(readData2E), .in2(ALUResult1M),.in3(ALUResult2M), .in4(writeData1),.in5(writeData2), .s(ForwardB1), .out(ForwardBMuxOut1));
mux2x1 #(32) ALUMux1(.in1(ForwardBMuxOut1), .in2(extImm1E), .s(ALUSrc1E), .out(ALUin1));
ALU alu1(.operand1(ForwardAMuxOut1), .operand2(ALUin1), .shamt(shamt1E) ,.opSel(ALUOp1E), .result(ALUResult1));

mux5to1 #(32) ForwardA2Mux(.in1(readData3E),  .in2(ALUResult1M),.in3(ALUResult2M), .in4(writeData1),.in5(writeData2), .s(ForwardA2), .out(ForwardAMuxOut2));
mux5to1 #(32) ForwardB2Mux(.in1(readData4E),  .in2(ALUResult1M),.in3(ALUResult2M), .in4(writeData1),.in5(writeData2), .s(ForwardB2), .out(ForwardBMuxOut2));
mux2x1 #(32) ALUMux2(.in1(ForwardBMuxOut2), .in2(extImm2E), .s(ALUSrc2E), .out(ALUin2));
ALU alu2(.operand1(ForwardAMuxOut2), .operand2(ALUin2), .shamt(shamt2E) ,.opSel(ALUOp2E), .result(ALUResult2));

  
pipe #(117) EX_MEM(
    .D({branchAdderResult1E, RegWriteEn1E, MemToReg1E, MemWriteEn1E, MemReadEn1E, 
        Branch1E, bit26_1E, prediction1E, ALUResult1, ForwardBMuxOut1,ForwardAMuxOut1, writeRegister1E
    }),
    .Q({branchAdderResult1M, RegWriteEn1M, MemToReg1M, MemWriteEn1M, MemReadEn1M, 
		  Branch1M, bit26_1M, prediction1M, ALUResult1M, ForwardBMuxOut1M, ForwardAMuxOut1M, writeRegister1M
    }), 
    .clk(clk), 
    .reset(rst), 
    .enable(enable),
	 .flush(FlushEX)
);

pipe #(151) EX_MEM_2(
	 .D({PCE, PCPlus1E, branchAdderResult2E, RegWriteEn2E, MemToReg2E, MemWriteEn2E, MemReadEn2E, rs2E, rt2E,
        PCPlus2E, Branch2E, bit26_2E,prediction2E, ALUResult2, ForwardBMuxOut2, ForwardAMuxOut2, writeRegister2E
    }),
    .Q({PCM, PCPlus1M, branchAdderResult2M, RegWriteEn2M, MemToReg2M, MemWriteEn2M, MemReadEn2M, rs2M, rt2M,
        PCPlus2M, Branch2M, bit26_2M, prediction2M, ALUResult2M, ForwardBMuxOut2M, ForwardAMuxOut2M, writeRegister2M
    }), 
    .clk(clk), 
    .reset(rst), 
    .enable(enable),
	 .flush(FlushEX));


/* ********************************************** MEMORY STAGE ******************************************* */
Comparator #(32) comp1(.equal(zero1), .a(ForwardBMuxOut1M), .b(ForwardAMuxOut1M));
XNORGate branchXnor1(.out(xnorOut1), .in1(bit26_1M), .in2(~zero1));
ANDGate branchAnd1(.in1(xnorOut1), .in2(Branch1M), .out(branch_taken1));

mux2x1 #(32) comp2MuxA (.in1(ForwardAMuxOut2M), .in2(ALUResult1M), .s(ForwardBranchA), .out(comp2MuxAout));
mux2x1 #(32) comp2MuxB (.in1(ForwardBMuxOut2M), .in2(ALUResult1M), .s(ForwardBranchB), .out(comp2MuxBout));
Comparator #(32) comp2(.equal(zero2), .a(comp2MuxAout), .b(comp2MuxBout));
XNORGate branchXnor2(.out(xnorOut2), .in1(bit26_2M), .in2(~zero2));
ANDGate branchAnd2(.in1(xnorOut2), .in2(Branch2M), .out(branch_taken2)); 

pcCorrection PCC (
    .PredictionM1(prediction1M), .PredictionM2(prediction2M), .branch_taken1(branch_taken1), .branch_taken2(branch_taken2), 
    .PCPlus1M(PCPlus1M), .PCPlus2M(PCPlus2M), .branchAdderResultM1(branchAdderResult1M), .branchAdderResultM2(branchAdderResult2M), 
    .CorrectedPC1(CorrectedPC1), .CorrectedPC2(CorrectedPC2)
);
dual_issue_data_memory DM (
	.address_a(ALUResult1M[11:0]),
	.address_b(ALUResult2M[11:0]),
	.clock(~clk),
	.data_a(ForwardBMuxOut1M),
	.data_b(ForwardBMuxOut2M),
	.rden_a(MemReadEn1M),
	.rden_b(MemReadEn2M),
	.wren_a(MemWriteEn1M),
	.wren_b(MemWriteEn2M & ~MemWriteEn1M),
	.q_a(memoryReadData1),
	.q_b(memoryReadData2)
	);

pipe #(80) MEM_WB1( 
    .D({
		  RegWriteEn1M, MemToReg1M,
		  PCPlus2M,
        ALUResult1M,
        memoryReadData1,
        writeRegister1M
    }),
    .Q({
        RegWriteEn1W, MemToReg1W,
		  PCPlus2W,  
        ALUResult1W,
        memoryReadData1W, 
        writeRegister1W
    }), 
    .clk(clk), 
    .reset(rst),      
    .enable(enable),
	 .flush(1'b0)
);
pipe #(72) MEM_WB2( 
    .D({
        RegWriteEn2M, MemToReg2M,
        ALUResult2M,
        memoryReadData2,
        writeRegister2M
    }),
    .Q({
        RegWriteEn2W, MemToReg2W, 
        ALUResult2W, 
        memoryReadData2W, 
        writeRegister2W
    }), 
    .clk(clk), 
    .reset(rst),      
    .enable(enable),
	 .flush(FlushMEM2)
);


/* ********************************************** WRITE BACK STAGE ******************************************* */


// Write-back for Instruction 1
mux3to1 #(32) WBMux1(.in1(ALUResult1W), .in2(memoryReadData1W), .in3({{24{1'b0}}, PCPlus2W-8'd1}), .s(MemToReg1W), .out(writeData1));


//assign writeData1 = (MemToReg1W == 2'b00) ? ALUResult1W : 
//                    (MemToReg1W == 2'b01) ? memoryReadData1W : 
//                    (MemToReg1W == 2'b10) ? {{21{1'b0}}, PCPlus2W-9'd1} : 
//                    32'b0;

// Write-back for Instruction 2
mux3to1 #(32) WBMux2(.in1(ALUResult2W), .in2(memoryReadData2W), .in3({{24{1'b0}}, PCPlus2W}), .s(MemToReg2W), .out(writeData2));


//assign writeData2 = (MemToReg2W == 2'b00) ? ALUResult2W : 
//                    (MemToReg2W == 2'b01) ? memoryReadData2W : 
//                    (MemToReg2W == 2'b10) ? {{21{1'b0}}, PCPlus2W} : 
//                    32'b0;



endmodule 