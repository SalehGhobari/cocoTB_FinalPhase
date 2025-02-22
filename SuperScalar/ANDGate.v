module ANDGate(in1, in2, out);

	input in1, in2;
	output out;
	assign out = in1 & in2;
	
endmodule

module AND3Gate(in1, in2, in3, out);

	input in1, in2, in3;
	output out;
	assign out = in1 & in2 & in3;
	
endmodule 