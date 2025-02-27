module ORGate(in1, in2, out);

	input in1, in2;
	output out;
	assign out = in1 | in2;
	
endmodule

module ORGate4(in1, in2, in3, in4, out);

	input in1, in2, in3, in4;
	output out;
	assign out = in1 | in2 | in3 |in4;
	
endmodule

module ORGate5(in1, in2, in3, in4, in5, out);

	input in1, in2, in3, in4, in5;
	output out;
	assign out = in1 | in2 | in3 | in4 | in5;
	
endmodule
