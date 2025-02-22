// sign Extender
// input is 16 bit, output is 32 bit

module signextender(in1, out); // changed module name to match file name

	//inputs
	input [15:0] in1;
	
	//outputs
	output [31:0] out;
	
	// Unit logic
	assign out = {{16{in1[15]}}, in1};
	
endmodule






