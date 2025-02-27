module mux2x1 #(parameter size = 32) (in1, in2, s, out);

	// inputs	
	input s;
	input [size - 1:0] in1, in2; // fixed mux input and output width
	
	// outputs
	output [size - 1:0] out;

	// Unit logic
	assign out = (~s) ? in1 : in2;
	
endmodule 


module mux3to1 #(parameter size = 32) (in1,in2,in3, s, out); // added 3 to 1 mux

input [1:0] s;
input [size - 1:0] in1, in2, in3;
output reg[size - 1:0] out;


always@(*) begin

	case (s)
	2'b00: out = in1;
	2'b01: out = in2;
	2'b10: out = in3;
	2'b11: out = {size{1'b0}};
	default: out = {size{1'b0}};
	
	endcase
	
end

endmodule

