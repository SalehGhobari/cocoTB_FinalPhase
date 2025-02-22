module pcCorrection (CorrectedPC,PCE, branchAdderResultE, PredictionE, branch_taken);

input PredictionE, branch_taken;
input [7:0] PCE, branchAdderResultE;
output reg [7:0]CorrectedPC;
always@(*) begin
CorrectedPC <= PCE;
		if (branch_taken & !PredictionE) begin
				CorrectedPC <= branchAdderResultE;
			end
	end
			
endmodule 