module pcCorrection (
    PredictionM1, PredictionM2, branch_taken1, branch_taken2, 
    PCPlus1M, PCPlus2M, branchAdderResultM1, branchAdderResultM2, 
    CorrectedPC1, CorrectedPC2
);

    // Inputs
    input PredictionM1, PredictionM2; // Predictions for the two branches
    input branch_taken1, branch_taken2; // Whether the branches were taken or not
    input [8:0] PCPlus1M, PCPlus2M; // Program counters for the two instructions in Execute stage
    input [8:0] branchAdderResultM1, branchAdderResultM2; // Branch target addresses for the two instructions

    // Outputs
    output reg [8:0] CorrectedPC1, CorrectedPC2; // Corrected PCs for the two branches

    // Correction logic for the first branch
    always @(*) begin
        CorrectedPC1 = PCPlus1M; // Default to the current PC
        if (branch_taken1 & !PredictionM1) begin
            CorrectedPC1 = branchAdderResultM1; // Correct PC if branch was mispredicted
        end
    end

    // Correction logic for the second branch
    always @(*) begin
        CorrectedPC2 = PCPlus2M; // Default to the current PC
        if (branch_taken2 & !PredictionM2) begin
            CorrectedPC2 = branchAdderResultM2; // Correct PC if branch was mispredicted
        end
    end

endmodule 