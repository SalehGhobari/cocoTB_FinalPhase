module processor(clk, rst, PC, enable);

//inputs
input clk, rst, enable;

//outputs
output [7:0] PC;

wire we1, we2, bit26_1, bit26_2, Branch1, MemReadEn1, MemWriteEn1, RegWriteEn1, ALUSrc1, Jump1, PcSrc1,
 Branch2, MemReadEn2, MemWriteEn2, RegWriteEn2, ALUSrc2, Jump2, PcSrc2;
 
wire [1:0] MemtoReg1, RegDst1, MemtoReg2, RegDst2;

wire [3:0] ALUOp1, ALUOp2;

wire [4:0] readRegister1, readRegister2, readRegister3, readRegister4, writeRegister1, writeRegister2, rd1, rd2, rs1, rs2, rt1, rt2, shamt1, shamt2;

wire [5:0] opCode1, opCode2, funct1, funct2;

wire [15:0] imm1, imm2;

wire [31:0] writeData1, writeData2, readData1, readData2, readData3, readData4, extImm1, extImm2, instr1, instr2,instr1D, instr2D;

wire [7:0] branchAdderResult1, branchAdderResult2, PCPlus2, PCPlus2D, PCD, branchAdderResult1D,branchAdderResult2D ;


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
reg [7:0]pcTest;

initial begin 
	pcTest = 0;
	end
	always @(posedge clk) begin 
		pcTest = pcTest+8'd2;
	end
programCounter pc(.clk(clk), .rst(rst), .enable(enable), .PCin(pcTest), .PCout(PC)); 

adder #(8) pcAdder(.in1(PC), .in2(8'd2), .out(PCPlus2));

//dual_issue_instr_mem (addr,instr1,instr2)
dual_issue_instr_mem  instMem(.addr(PC),.instr1(instr1),.instr2(instr2), .rst(rst), .clk(clk));


adder #(8) branchAdder1(.in1(PC+1), .in2(instr1[7:0]), .out(branchAdderResult1));
adder #(8) branchAdder2(.in1(PC+2), .in2(instr2[7:0]), .out(branchAdderResult2));


pipe #(96) IF_ID(.D({PCPlus2,PC,branchAdderResult1,branchAdderResult2, instr1, instr2}), 
		.Q({PCPlus2D,PCD,branchAdderResult1D,branchAdderResult2D, instr1D, instr2D}), 
		.clk(clk), .reset(~rst), .enable(enable)); 




/**************************************************************DECODE STAGE*********************************************/

// registerFile (clk, rst, we1, we2, readRegister1, readRegister2, readRegister3, readRegister4,writeRegister1,writeRegister2,writeData1, writeData2, readData1, readData2, readData3, readData4);
registerFile RegFile (
     .clk(clk), .rst(~rst), .we1(we1), .we2(we2), .readRegister1(readRegister1), .readRegister2(readRegister2), .readRegister3(readRegister3)
	  , .readRegister4(readRegister4),.writeRegister1(writeRegister1), .writeRegister2(writeRegister2), 
	  .writeData1(writeData1), .writeData2(writeData2), .readData1(readData1), .readData2(readData2), .readData3(readData3), .readData4(readData4));



signextender SignExtend1(.in(imm1), .out(extImm1));
signextender SignExtend2(.in(imm2), .out(extImm2));


controlUnit CU (
        .opCode1(opCode1), .funct1(funct1),
        .opCode2(opCode2), .funct2(funct2),
        .Branch1(Branch1), .MemReadEn1(MemReadEn1), .MemWriteEn1(MemWriteEn1), .RegWriteEn1(RegWriteEn1), .ALUSrc1(ALUSrc1), .Jump1(Jump1), .PcSrc1(PcSrc1),
        .Branch2(Branch2), .MemReadEn2(MemReadEn2), .MemWriteEn2(MemWriteEn2), .RegWriteEn2(RegWriteEn2), .ALUSrc2(ALUSrc2), .Jump2(Jump2), .PcSrc2(PcSrc2),
        .MemtoReg1(MemtoReg1), .RegDst1(RegDst1),
        .MemtoReg2(MemtoReg2), .RegDst2(RegDst2),
        .ALUOp1(ALUOp1), .ALUOp2(ALUOp2)
);










































//wire [31:0] instruction, readData1, readData2, extImm, ALUResult, memoryReadData,
// memoryReadDataW, instructionD, readData1E, readData2E, extImmE, instructionE, ALUResultM, readData2M, 
// ALUResultW, ForwardBMuxOutM, FADMuxOut, FBDMuxOut;
//
//wire [15:0] imm;
//
//wire [5:0] opCode, funct;
//
//wire [7:0] PCD,PCE,branchAdderResultD, PCPlus1, branchAdderResult,branchAdderResultE, PCPlus1D, PCPlus1E, PCPlus1M, PCPlus1W, imInput, CorrectedPC, BA_PCP1;
//
//wire [4:0] rs, rt, rd, rsE, rtE, rdE, shamt, writeRegisterM, writeRegisterW, shamtE;
//
//wire [3:0] ALUOp,ALUOpD, ALUOpE, ALUOpNew;
//
//wire [1:0] regDst, memToReg,memToRegD, memToRegE, regDstE,regDstD, memToRegM, memToRegW, ForwardA, ForwardB,memToRegNew, regDstNew, ForwardAD, ForwardBD;
//
//wire pcSrc, jump, branch, memRead, memWrite, ALUSrc, regWrite,pcSrcD, jumpD, regWriteD, memWriteD, memReadD, ALUSrcD, branchD,
// zero, xnorOut,bit26,bit26E,overflow, regWriteE,branchE,predictionE, memWriteE, memReadE, ALUSrcE, regWriteM, memWriteM, memReadM, regWriteW,
// Flush,Stall, Reset,EnablePCIFID,pcSrcNew,jumpNew,regWriteNew,memWriteNew, memReadNew,ALUSrcNew, branchNew, branchTaken, 
// prediction,CPCSignal,predictionD, predictionNew;
// 
//reg [7:0] jumpMuxOut,branchMuxOut,nextPC,CPC;
//reg [31:0] ForwardAMuxOut, ForwardBMuxOut,ALUin2, writeData;
//reg [4:0] writeRegister;
//
//assign opCode = instructionD[31:26];
//assign rd = instructionD[15:11]; 
//assign rs = instructionD[25:21];  
//assign shamt = instructionD[10:6];
//assign rt = instructionD[20:16];  
//assign imm = instructionD[15:0];
//assign funct = instructionD[5:0];
//assign bit26 =instructionD[26];

///* ********************************************** FETCH STAGE ******************************************* */
//
////mux2x1 #(8) jumpMux(.in1(readData1[7:0]), .in2(instructionD[7:0]), .s(jumpD), .out(jumpMuxOut));
////
////mux2x1 #(8) branchMux(.in1(PCPlus1), .in2(branchAdderResult), .s(prediction), .out(branchMuxOut));
////
////mux2x1 #(8) pcMux(.in1(branchMuxOut), .in2(jumpMuxOut), .s(pcSrcD), .out(nextPC));
////
////mux2x1 #(8) cpcMux(.in1(nextPC), .in2(CorrectedPC), .s(CPCSignal), .out(CPC)); 
//
//	always @(*) begin
//		 if (jumpD)
//			  jumpMuxOut = instructionD[7:0];
//			  else 
//			  jumpMuxOut = readData1[7:0];
//	end
//	
//
//	// branchMux logic
//	always @(*) begin
//		 if (prediction)
//			  branchMuxOut = branchAdderResult;
//			  else
//			  branchMuxOut = PCPlus1;
//	end
//
//	// pcMux logic
//	always @(*) begin
//		 if (pcSrcD)
//			  nextPC = jumpMuxOut;
//			else
//			  nextPC = branchMuxOut;
//			  
//	end
//
//	// cpcMux logic
//	always @(*) begin
//
//		 if (CPCSignal)
//			  CPC = CorrectedPC;
//		  else
//				CPC = nextPC;
//	end
//
//programCounter pc(.clk(clk), .rst(rst), .enable(EnablePCIFID), .PCin(CPC), .PCout(PC)); 
//
//adder #(8) pcAdder(.in1(PC), .in2(8'b1), .out(PCPlus1));
//
//adder #(8) branchAdder(.in1(PCPlus1), .in2(instruction[7:0]), .out(branchAdderResult));
//
//instructionMemory IM(.address(CPC), .aclr (~rst), .clock (clk), .addressstall_a(~EnablePCIFID), .q(instruction));
//
//BranchPredictionUnit BPU(.branch_taken(branchTaken), .clk(clk), .reset(rst), .branch(branchE), .pc(PC), .pcE(PCE), .prediction(prediction));
//
//pipe #(57) IF_ID(.D({PCPlus1,PC,branchAdderResult, prediction, instruction}), .Q({PCPlus1D,PCD,branchAdderResultD,predictionNew, instructionD}), .clk(clk), .reset(~Reset), .enable(EnablePCIFID)); 
//
//
//
///* ********************************************** DECODE STAGE ******************************************* */
//
//signextender SignExtend(.in(imm), .out(extImm));
//
//controlUnit CU(.opCode(opCode), .funct(funct), 
//     .RegDst(regDst), .Branch(branch), .MemReadEn(memRead), .MemtoReg(memToReg),
//    .ALUOp(ALUOp), .MemWriteEn(memWrite), .RegWriteEn(regWrite), .ALUSrc(ALUSrc), .Jump(jump), .PcSrc(pcSrc));
//
//registerFile RF(.clk(clk), .rst(rst), .we(regWriteW), 
//   .readRegister1(rs), .readRegister2(rt), .writeRegister(writeRegisterW),
//   .writeData(writeData), .readData1(readData1), .readData2(readData2));
//
//mux2x1 #(16) CUMux(.in1({pcSrc,jump,regWrite, memToReg, memWrite, memRead, ALUOp, regDst, ALUSrc, branch, predictionNew}), .in2(16'b0), .s(Stall),
// .out({pcSrcD, jumpD, regWriteD, memToRegD, memWriteD, memReadD, ALUOpD, regDstD, ALUSrcD, branchD, predictionD}));
//
// 
//pipe #(155) ID_EX(.D({PCD,branchAdderResultD,bit26, branchD, regWriteD, memToRegD, memWriteD, memReadD, ALUOpD, regDstD, ALUSrcD, predictionD, PCPlus1D, readData1, readData2, extImm, rs, rt, rd, shamt}),
//						.Q({PCE,branchAdderResultE,bit26E, branchE, regWriteE, memToRegE, memWriteE, memReadE, ALUOpE, regDstE, ALUSrcE,predictionE, PCPlus1E, readData1E, readData2E, extImmE, rsE, rtE, rdE, shamtE}), .clk(clk), .reset(~(Reset&~pcSrcD)), .enable(enable));
//
///*********************************************** EXECUTE STAGE ********************************************/
//
//HazardDetectionUnit HDU (.Stall(Stall), .Flush(Flush), .CPCSignal(CPCSignal), .takenBranch(branchTaken), 
//.pcSrc(pcSrcD), .writeRegisterE(writeRegister), .rsD(rs), .rtD(rt), .memReadE(memReadE), .branch(branchE), .predictionE(predictionE));
//
//ANDGate holdGate(.in1(~Stall), .in2(enable), .out(EnablePCIFID));
//
//ORGate resetGate(.in1(~rst), .in2(Flush), .out(Reset));
//
////mux3to1 #(32) ForwardAMux(.in1(readData1E), .in2(ALUResultM), .in3(writeData), .s(ForwardA), .out(ForwardAMuxOut));
////
////mux3to1 #(32) ForwardBMux(.in1(readData2E), .in2(ALUResultM), .in3(writeData), .s(ForwardB), .out(ForwardBMuxOut));
////
////mux2x1 #(32) ALUMux(.in1(ForwardBMuxOut), .in2(extImmE), .s(ALUSrcE), .out(ALUin2));
//
//
//	always @(*) begin
//		 case (ForwardA)
//			  2'b00: ForwardAMuxOut = readData1E;
//			  2'b01: ForwardAMuxOut = ALUResultM;
//			  2'b10: ForwardAMuxOut = writeData;
//			  default: ForwardAMuxOut = 32'b0;
//		 endcase
//	end
//
//	// ForwardBMux logic
//	always @(*) begin
//		 case (ForwardB)
//			  2'b00: ForwardBMuxOut = readData2E;
//			  2'b01: ForwardBMuxOut = ALUResultM;
//			  2'b10: ForwardBMuxOut = writeData;
//			  default: ForwardBMuxOut = 32'b0;
//		 endcase
//	end
//
//	// ALUMux logic
//	always @(*) begin
//		 if (ALUSrcE)
//			  ALUin2 = extImmE;
//		 else
//			  ALUin2 = ForwardBMuxOut;
//	end
//
//ALU alu(.operand1(ForwardAMuxOut), .operand2(ALUin2), .shamt(shamtE) ,.opSel(ALUOpE), .result(ALUResult), .overflow(overflow));
//
////mux3to1 #(5) RFMux(.in1(rtE), .in2(rdE), .in3(5'b11111), .s(regDstE), .out(writeRegister));
//	always @(*) begin
//		 case (regDstE)
//			  2'b00: writeRegister = rtE;
//			  2'b01: writeRegister = rdE;
//			  2'b10: writeRegister = 5'b11111;
//			  default: writeRegister = 5'b00000;
//		 endcase
//	end
//
//Comparator #(32) comp (zero, ForwardAMuxOut, ForwardBMuxOut);
//
//XNORGate branchXnor(.out(xnorOut), .in1(bit26E), .in2(~zero));
//
//ANDGate branchAnd(.in1(xnorOut), .in2(branchE), .out(branchTaken));   
// 
//pcCorrection pcCorr (.CorrectedPC(CorrectedPC),.PCE(PCPlus1E), .branchAdderResultE(branchAdderResultE), .PredictionE(predictionE), .branch_taken(branchTaken));     
//
//
//
//ForwardingUnit FU( .rsE(rsE), .rtE(rtE), .writeRegisterM(writeRegisterM), 
//	.writeRegisterW(writeRegisterW), .regWriteM(regWriteM), .regWriteW(regWriteW), .ForwardA(ForwardA), .ForwardB(ForwardB));
//	
//
//pipe #(82) EX_MEM(.D({regWriteE, memToRegE, memWriteE, memReadE, PCPlus1E, ALUResult, ForwardBMuxOut, writeRegister}), 
//.Q({regWriteM, memToRegM, memWriteM, memReadM, PCPlus1M, ALUResultM, ForwardBMuxOutM, writeRegisterM}), .clk(clk), .reset(rst), .enable(enable));
//
//
///* ********************************************** MEMORY STAGE ******************************************* */
//
//dataMemory DM(.address(ALUResultM[7:0]), .clock(~clk), .data(ForwardBMuxOutM), .rden(memReadM), .wren(memWriteM), .q(memoryReadData));
//
//pipe #(80) MEM_WB(.D({regWriteM, memToRegM, PCPlus1M, ALUResultM, memoryReadData, writeRegisterM}), 
//.Q({regWriteW, memToRegW, PCPlus1W, ALUResultW, memoryReadDataW, writeRegisterW}), .clk(clk), .reset(rst), .enable(enable));
//
///* ********************************************** WRITE BACK STAGE ******************************************* */
//
////mux3to1 #(32) WBMux(.in1(ALUResultW), .in2(memoryReadDataW), .in3({{24{1'b0}} ,PCPlus1W}), .s(memToRegW), .out(writeData));
//
//always @(*) begin
//    case (memToRegW)
//        2'b00: writeData = ALUResultW;
//        2'b01: writeData = memoryReadDataW;
//        2'b10: writeData = {{24{1'b0}}, PCPlus1W};
//        default: writeData = 32'b0;
//    endcase
//end

endmodule 