module controlUnit(opCode, funct,
				   RegDst, Branch, MemReadEn, MemtoReg,
				   ALUOp, MemWriteEn, RegWriteEn, ALUSrc, Jump, PcSrc);
				   
		
	// inputs 
	input wire [5:0] opCode, funct;
	// outputs (signals)
	output reg Branch, MemReadEn, MemWriteEn, RegWriteEn, ALUSrc, Jump, PcSrc;
	output reg [1:0] MemtoReg,RegDst;
	output reg [3:0] ALUOp;
	
	// parameters (opCodes/functs)
	parameter _RType = 6'h0, _addi = 6'h8, _lw = 6'h23, _sw = 6'h2b, _beq = 6'h4, _bne = 6'h5, _jal=6'h03, _ori=6'h0d, _xori=6'h16;
	parameter _add_ = 6'h20, _sub_ = 6'h22, _and_ = 6'h24, _or_ = 6'h25, _slt_ = 6'h2a, _sgt_ = 6'h14, _sll_ = 6'h00,
	_srl_ = 6'h02, _nor_ = 6'h27, _xor_ = 6'h15, _jr_ = 6'h08, _andi = 6'hc, _slti = 6'ha, _j = 6'h2;
	
	
	// unit logic - generate signals
	always @(*) begin
	
		RegDst = 2'b0; Branch = 1'b0; MemReadEn = 1'b0; MemtoReg = 2'b0;
		MemWriteEn = 1'b0; RegWriteEn = 1'b0; ALUSrc = 1'b0; Jump=1'b0; PcSrc=1'b0;
		ALUOp = 4'b0;
		case(opCode)
				
			_RType : begin
				
				RegDst = 2'b01;
				Branch = 1'b0;
				MemReadEn = 1'b0;
				MemtoReg = 2'b0;
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b1;
				ALUSrc = 1'b0;
				Jump = 1'b0;
				PcSrc = 1'b0;
					
				case (funct) 
					
					_add_ : begin
						ALUOp = 4'b0000;
					end
						
					_sub_ : begin
						ALUOp = 4'b0001;
					end
						
					_and_ : begin
						ALUOp = 4'b0010;
					end
						
					_or_ : begin
						ALUOp = 4'b0011; 
					end
						
					_slt_ : begin
						ALUOp = 4'b0100;
					end
					
					_sgt_ : begin
						ALUOp = 4'b0101;
					end
					
					_nor_ : begin
						ALUOp = 4'b0110;
					end
					
					_xor_ : begin
						ALUOp = 4'b0111;
					end
					
					_sll_ : begin
						ALUOp = 4'b1000;
					end
					
					_srl_ : begin
						ALUOp = 4'b1001;
					end
					
								
					_jr_ : begin
						Branch = 1'b0;
						MemReadEn = 1'b0;
						MemWriteEn = 1'b0;
						RegWriteEn = 1'b0;
						Jump = 1'b0;
						PcSrc = 1'b1;
					end
					
					default: ;
				
				endcase
				
			end
				
			_addi : begin
				RegDst = 2'b0;
				Branch = 1'b0;
				MemReadEn = 1'b0;
				MemtoReg = 2'b0;
				ALUOp = 4'b0000;
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b1;
				ALUSrc = 1'b1;
				Jump = 1'b0;
				PcSrc = 1'b0;				
			end
				
			_lw : begin
				RegDst = 2'b0;
				Branch = 1'b0;
				MemReadEn = 1'b1;
				MemtoReg = 2'b01;
				ALUOp = 4'b0000;
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b1;		
				ALUSrc = 1'b1;
				Jump = 1'b0;
				PcSrc = 1'b0;		
			end
				
			_sw : begin
				Branch = 1'b0;
				MemReadEn = 1'b0;
				ALUOp = 4'b0000;
				MemWriteEn = 1'b1;
				RegWriteEn = 1'b0;
				ALUSrc = 1'b1;	
				Jump = 1'b0;
				PcSrc = 1'b0;			
			end
				
			_beq : begin
				Branch = 1'b1;
				MemReadEn = 1'b0;
				ALUOp = 4'b0001;
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b0;
				ALUSrc = 1'b0;
				Jump = 1'b0;
				PcSrc = 1'b0;				
			end
			
			_bne : begin
				Branch = 1'b1;
				MemReadEn = 1'b0;
				ALUOp = 4'b0001;
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b0;
				ALUSrc = 1'b0;
				Jump = 1'b0;
				PcSrc = 1'b0;
			end

			
			_jal : begin
				Branch = 1'b0; 
				MemReadEn = 1'b0;
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b1;
				ALUSrc = 1'b0;
				Jump = 1'b1;
				PcSrc = 1'b1;
				RegDst = 2'b10;
				MemtoReg =  2'b10;
				
			end
			
			_ori : begin
				RegDst = 2'b0;
				Branch = 1'b0;
				MemReadEn = 1'b0;
				MemtoReg = 2'b0;
				ALUOp = 4'b0011;
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b1;
				ALUSrc = 1'b1;
				Jump = 1'b0;
				PcSrc = 1'b0;				
			end
			
			_xori : begin
				RegDst = 2'b0;
				Branch = 1'b0;
				MemReadEn = 1'b0;
				MemtoReg = 2'b0;
				ALUOp = 4'b0111;
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b1;
				ALUSrc = 1'b1;
				Jump = 1'b0;
				PcSrc = 1'b0;				
			end
			
			_andi : begin
				RegDst = 2'b0;
				Branch = 1'b0;
				MemReadEn = 1'b0;
				MemtoReg = 2'b0;
				ALUOp = 4'b0010;
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b1;
				ALUSrc = 1'b1;
				Jump = 1'b0;
				PcSrc = 1'b0;				
			end
			
			_slti : begin
				RegDst = 2'b0;
				Branch = 1'b0;
				MemReadEn = 1'b0;
				MemtoReg = 2'b0;
				ALUOp = 4'b0100; 
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b1;
				ALUSrc = 1'b1;
				Jump = 1'b0;
				PcSrc = 1'b0;				
			end
			
			_j : begin
				Branch = 1'b0;    
				MemReadEn = 1'b0;
				MemWriteEn = 1'b0;
				RegWriteEn = 1'b0;
				ALUSrc = 1'b0;
				Jump = 1'b1;
				PcSrc = 1'b1;
				RegDst = 2'b10;
				MemtoReg =  2'b10;
				
			end
			
			
			default: ;
				
		endcase
	end
	
	
endmodule
