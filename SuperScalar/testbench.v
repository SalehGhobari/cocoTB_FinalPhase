`timescale 1ns/1ps
module testbench;

	reg clk, rst, enable;
	
	wire [8:0] PC;
	
	initial begin
		clk = 0;
		rst = 0;
		enable = 1;
		#4 rst = 1;
		#30000 $stop;
	end
	
	always #5 clk = ~clk;
	
	processor uut(clk, rst, PC, enable);
	
	
endmodule
