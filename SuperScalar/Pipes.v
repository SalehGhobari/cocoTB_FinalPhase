module pipe #(parameter size = 96)(Q, D, clk, reset, enable, flush);
input [size - 1:0] D;
input clk, reset, enable, flush;
output reg [size - 1:0] Q;



always @(posedge clk, negedge reset) begin


if (~reset)
	Q <= {size{1'b0}};
	
else if(flush&clk) 
	Q <= {size{1'b0}};

else if (~enable)
	Q <= Q;

else
	Q <= D;

end 

endmodule 