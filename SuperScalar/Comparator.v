module Comparator #(parameter size = 32) (equal, a, b); 
input [size - 1:0]a, b; 
output reg equal; 


always @(a or b) begin
	if (a==b)
		equal = 1;

	else
		equal = 0;

	end
	
endmodule 