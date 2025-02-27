module HazardDetectionUnit (Stall, Flush, CPCSignal, takenBranch, pcSrc, writeRegisterE, rsD, rtD, memReadE, branch, predictionE);
 input takenBranch, pcSrc, memReadE, branch,predictionE;
 input [4:0] writeRegisterE, rsD, rtD;
 output reg Stall, Flush,CPCSignal;
	
	
	always @(*) begin
	
		Flush =(takenBranch ^ predictionE) & branch|pcSrc ;
		
	end
	
	always @(*) begin
		Stall = 0;
		if (memReadE && (writeRegisterE == rsD || writeRegisterE == rtD) && (writeRegisterE != 5'b0)) begin
			Stall = 1;
		end
	end
	
	always @(*) begin 
		CPCSignal = (takenBranch ^ predictionE) & branch;
		
	end

endmodule 