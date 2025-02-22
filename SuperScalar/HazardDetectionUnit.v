module HazardDetectionUnit (
    takenBranch1, takenBranch2, pcSrc1, pcSrc2, memReadE1, memReadE2, 
    branch1, branch2, predictionE1, predictionE2, writeRegisterE1, writeRegisterE2, 
    rsD1, rtD1, rsD2, rtD2, Stall11, Stall21, Stall12, Stall22, FlushIFID1, FlushEX, FlushMEM2, CPCSignal1, CPCSignal2
);

    // Inputs
    input takenBranch1, takenBranch2; // Branch outcomes for the two instructions
    input pcSrc1, pcSrc2;             // PC source signals for the two instructions
    input memReadE1, memReadE2;       // Memory read signals for the two instructions in Execute stage
    input branch1, branch2;           // Branch signals for the two instructions
    input predictionE1, predictionE2; // Predictions for the two branches
    input [4:0] writeRegisterE1, writeRegisterE2; // Destination registers for the two instructions in Execute stage
    input [4:0] rsD1, rtD1, rsD2, rtD2; // Source registers for the two instructions in Decode stage

    // Outputs
    output reg Stall11, Stall21, Stall12, Stall22;        // Stall signals for the two instructions
    output reg FlushIFID1,FlushEX, FlushMEM2;        // Flush signals for the two instructions
    output reg CPCSignal1, CPCSignal2; // Correct PC signals for the two branches

    // Flush logic for the two instructions
    always @(*) begin
       FlushIFID1 = pcSrc1 | pcSrc2 | (branch1&(predictionE1^takenBranch1)) | (branch2&(predictionE2^takenBranch2));
		 FlushEX = (branch1&(predictionE1^takenBranch1)) | (branch2&(predictionE2^takenBranch2));
		 FlushMEM2 = (branch1&(predictionE1^takenBranch1)) ;
    end

    // Stall logic for the two instructions
    always @(*) begin
        Stall11 = 0;
        Stall21 = 0;
		Stall12 = 0;
        Stall22 = 0;

        // Stall logic for the first instruction
        if (memReadE1 && ((writeRegisterE1 == rsD1 || writeRegisterE1 == rtD1) && (writeRegisterE1 != 5'b0))) begin
            Stall11 = 1;
        end
		  if(memReadE2 && ((writeRegisterE2 == rsD1 || writeRegisterE2 == rtD1) && (writeRegisterE2 != 5'b0)) & !memReadE1) begin 
				Stall21 = 1;
		  end

        // Stall logic for the second instruction
		  if(memReadE1 && ((writeRegisterE1 == rsD2 || writeRegisterE1 == rtD2) && (writeRegisterE1 != 5'b0))) begin
				Stall12 = 1;
		  end
        if (memReadE2 && ((writeRegisterE2 == rsD2 || writeRegisterE2 == rtD2) && (writeRegisterE2 != 5'b0))& !memReadE1) begin
            Stall22 = 1;
        end
		 
    end

    // Correct PC signal logic for the two branches
	 initial begin 
	 	  CPCSignal1=0;
		  CPCSignal2=0;
	 end
    always @(*) begin

        CPCSignal1 = (takenBranch1 ^ predictionE1) & branch1;
        CPCSignal2 = (takenBranch2 ^ predictionE2) & branch2;
    end

endmodule 