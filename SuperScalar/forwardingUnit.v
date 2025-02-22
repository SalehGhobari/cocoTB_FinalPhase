module ForwardingUnit (rsE1, rtE1, rsE2, rtE2, rsM2, rtM2, writeRegisterM1, writeRegisterM2, writeRegisterW1, writeRegisterW2, regWriteM1, regWriteM2, regWriteW1, regWriteW2, 
ForwardA1, ForwardB1, ForwardBranchA, ForwardBranchB, ForwardA2, ForwardB2, branch2M);

    input [4:0] rsE1, rtE1;
    input [4:0] rsE2, rtE2, rsM2, rtM2;
    input [4:0] writeRegisterM1;
    input [4:0] writeRegisterM2;
    input [4:0] writeRegisterW1;
    input [4:0] writeRegisterW2;
    input regWriteM1, regWriteM2, branch2M;
    input regWriteW1, regWriteW2;

    output reg [2:0] ForwardA1, ForwardB1;
    output reg [2:0] ForwardA2, ForwardB2;
	 output reg ForwardBranchA, ForwardBranchB;

always @(*) begin
        ForwardA1 = 3'b000;
        ForwardB1 = 3'b000;
        ForwardA2 = 3'b000;
        ForwardB2 = 3'b000;
		  ForwardBranchA = 1'b0;
		  ForwardBranchB = 1'b0;
		  

        if (regWriteM1 && (writeRegisterM1 == rsE1) && (writeRegisterM1 != 0))
            ForwardA1 = 3'b001;
        else if (regWriteM2 && (writeRegisterM2 == rsE1) && (writeRegisterM2 != 0) && (writeRegisterM1 != rsE1))
            ForwardA1 = 3'b010;
        else if (regWriteW1 && (writeRegisterW1 == rsE1) && (writeRegisterW1 != 0) &&
                ((writeRegisterM1 != rsE1 || !regWriteM1) && (writeRegisterM2 != rsE1 || !regWriteM2)))
            ForwardA1 = 3'b011;
        else if (regWriteW2 && (writeRegisterW2 == rsE1) && (writeRegisterW2 != 0) &&
                ((writeRegisterM1 != rsE1 || !regWriteM1) && (writeRegisterM2 != rsE1 || !regWriteM2)) && (writeRegisterW1 != rsE1))
            ForwardA1 = 3'b100;

        if (regWriteM1 && (writeRegisterM1 == rtE1) && (writeRegisterM1 != 0))
            ForwardB1 = 3'b001;
        else if (regWriteM2 && (writeRegisterM2 == rtE1) && (writeRegisterM2 != 0) && (writeRegisterM1 != rtE1))
            ForwardB1 = 3'b010;
        else if (regWriteW1 && (writeRegisterW1 == rtE1) && (writeRegisterW1 != 0) &&
                ((writeRegisterM1 != rtE1 || !regWriteM1) && (writeRegisterM2 != rtE1 || !regWriteM2)))
            ForwardB1 = 3'b011;
        else if (regWriteW2 && (writeRegisterW2 == rtE1) && (writeRegisterW2 != 0) &&
                ((writeRegisterM1 != rtE1 || !regWriteM1) && (writeRegisterM2 != rtE1 || !regWriteM2)) && (writeRegisterW1 != rtE1))
            ForwardB1 = 3'b100;

        if (regWriteM1 && (writeRegisterM1 == rsE2) && (writeRegisterM1 != 0))
            ForwardA2 = 3'b001;
        else if (regWriteM2 && (writeRegisterM2 == rsE2) && (writeRegisterM2 != 0) && (writeRegisterM1 != rsE2))
            ForwardA2 = 3'b010;
        else if (regWriteW1 && (writeRegisterW1 == rsE2) && (writeRegisterW1 != 0) &&
                ((writeRegisterM1 != rsE2 || !regWriteM1) && (writeRegisterM2 != rsE2 || !regWriteM2)))
            ForwardA2 = 3'b011;
        else if (regWriteW2 && (writeRegisterW2 == rsE2) && (writeRegisterW2 != 0) &&
                ((writeRegisterM1 != rsE2 || !regWriteM1) && (writeRegisterM2 != rsE2 || !regWriteM2)) && (writeRegisterW1 != rsE2))
            ForwardA2 = 3'b100;

        if (regWriteM1 && (writeRegisterM1 == rtE2) && (writeRegisterM1 != 0))
            ForwardB2 = 3'b001;
        else if (regWriteM2 && (writeRegisterM2 == rtE2) && (writeRegisterM2 != 0) && (writeRegisterM1 != rtE2))
            ForwardB2 = 3'b010;
        else if (regWriteW1 && (writeRegisterW1 == rtE2) && (writeRegisterW1 != 0) &&
                ((writeRegisterM1 != rtE2 || !regWriteM1) && (writeRegisterM2 != rtE2 || !regWriteM2)))
            ForwardB2 = 3'b011;
        else if (regWriteW2 && (writeRegisterW2 == rtE2) && (writeRegisterW2 != 0) &&
                ((writeRegisterM1 != rtE2 || !regWriteM1) && (writeRegisterM2 != rtE2 || !regWriteM2)) && (writeRegisterW1 != rtE2))
            ForwardB2 = 3'b100;
				
			if(regWriteM1 & branch2M &&((writeRegisterM1 == rsM2))) begin
				ForwardBranchA = 1'b1;
			end
			if(regWriteM1 & branch2M &&((writeRegisterM1 == rtM2))) begin
				ForwardBranchB = 1'b1;
			end
end
endmodule 