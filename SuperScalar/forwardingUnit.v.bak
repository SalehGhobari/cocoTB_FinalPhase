module ForwardingUnit ( rsE, rtE, writeRegisterM, writeRegisterW, regWriteM, regWriteW, ForwardA, ForwardB);

input [4:0] rsE, rtE;       
input [4:0] writeRegisterM, writeRegisterW;
input regWriteM, regWriteW;            
output reg [1:0] ForwardA, ForwardB;


always @(*) begin

	ForwardA[0] = 1'b0;
	ForwardB[0] = 1'b0;
	ForwardA[1] = 1'b0;
	ForwardB[1] = 1'b0;

if (regWriteM && (writeRegisterM == rsE) && (writeRegisterM != 0))
	ForwardA[0] = 1;
	
if (regWriteM && (writeRegisterM == rtE) && (writeRegisterM != 0))
	ForwardB[0] = 1;

if (regWriteW && (writeRegisterW == rsE) && (writeRegisterM != rsE || regWriteM == 0) && (writeRegisterW != 0))
	ForwardA[1] = 1;
	
if (regWriteW && (writeRegisterW == rtE) && (writeRegisterM != rtE || regWriteM == 0) && (writeRegisterW != 0))
	ForwardB[1] = 1;
	
end






endmodule
