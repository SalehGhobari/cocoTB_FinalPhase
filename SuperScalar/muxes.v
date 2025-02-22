module mux2x1 #(parameter size = 32) (in1, in2, s, out);

	// inputs	
	input s;
	input [size - 1:0] in1, in2; // fixed mux input and output width
	
	// outputs
	output [size - 1:0] out;

	// Unit logic
	assign out = (~s) ? in1 : in2;
	
endmodule 

module mux2x1En #(parameter size = 32) (in1, in2, s, en, out);

	// inputs	
	input s, en;
	input [size - 1:0] in1, in2; // fixed mux input and output width
	
	// outputs
	output reg[size - 1:0] out;
	
	always @(*) begin
    if (en) begin
        
        out = s ? in2 : in1;
    end
    
	end

	
endmodule 


module mux3to1 #(parameter size = 32) (in1, in2, in3, s, out); // added 3 to 1 mux

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

module mux5to1 #(parameter size = 32) (in1, in2, in3, in4, in5, s, out); // added 3 to 1 mux

input [2:0] s;
input [size - 1:0] in1, in2, in3, in4, in5;
output reg[size - 1:0] out;


always@(*) begin

	case (s)
	3'b000: out = in1;
	3'b001: out = in2;
	3'b010: out = in3;
	3'b011: out = in4;
	3'b100: out = in5;
	3'b101: out = {size{1'b0}};
	3'b110: out = {size{1'b0}};
	3'b111: out = {size{1'b0}};
	default: out = {size{1'b0}};
	
	endcase
	
end

endmodule


