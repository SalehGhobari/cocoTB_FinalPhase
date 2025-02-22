module ALU (operand1, operand2, shamt, opSel, result);
	
	parameter data_width = 32;
	parameter sel_width = 4;
	
	// Inputs
	// ......
	
	input [data_width - 1 : 0] operand1, operand2;
	input [sel_width - 1 :0] opSel;
	input [4:0] shamt;
	// Outputs
	// .......
	
	output reg [data_width - 1 : 0] result;
	// Operation Parameters
	// ....................
	parameter   _ADD  = 'b0000, _SUB  = 'b0001, _AND = 'b0010,
				_OR   = 'b0011, _SLT  = 'b0100, _SGT = 'b0101, _NOR = 'b0110, _XOR = 'b0111,
				_SLL = 'b1000, _SRL = 'b1001;	
	
	// Perform Operation
	// .................
	
	
	
	always @ (*) begin
	
			result = 32'b0;
		case(opSel)
			
			_ADD: begin
				result = operand1 + operand2;
			end
			
			_SUB: begin
				result = operand1 - operand2;
			end
			
			_AND: begin
				result = operand1 & operand2;
			end
			_OR : begin
				result = operand1 | operand2;
			end
			_NOR: begin
				result = ~(operand1 | operand2);
			end
			_XOR: begin
				result = operand1 ^ operand2;
			end
			_SLT: begin
				result = ($signed(operand1) < $signed(operand2)) ? 1 : 0;
			end
			_SGT: begin 
				result = ($signed(operand1) > $signed(operand2)) ? 1 : 0;
			end
			_SLL: begin
				result = operand2 << shamt;
			end
			_SRL: begin
				result = operand2 >> shamt;
			end
			default:;

		endcase
	
	end
	

endmodule 
