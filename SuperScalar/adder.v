// parameterized adder module

module adder #(parameter size = 11) (in1, in2, out);
	// size parameter
	// inputs
	input wire [size-1:0] in1, in2;
	// outputs
	output wire [size-1:0] out;
	
	// summation
	assign out = in1 + $signed(in2);

endmodule
