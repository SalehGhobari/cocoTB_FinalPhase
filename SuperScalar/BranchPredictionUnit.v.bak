module BranchPredictionUnit (
    clk, reset, branch1, branch2, branch_taken1, branch_taken2,
    pc1, pc2, pcM1, pcM2, targetM1, targetM2, prediction1, prediction2, 
    nextPC, instMemPred, predictedTarget1, predictedTarget2, instMemTarget
);
    // Inputs
    input clk, reset;
    input branch1, branch2;            // Branch signals for the two instructions
    input branch_taken1, branch_taken2; // Whether the branches were taken or not
    input [10:0] pc1, pc2;            // Program counters for the two instructions
    input [10:0] pcM1, pcM2;          // Program counters for the two instructions in Memory stage
    input [10:0] nextPC;
    input [10:0] targetM1, targetM2;   // Actual branch targets from Memory stage

    // Outputs
    output reg prediction1, prediction2, instMemPred;           // Predictions for the two branches
    output reg [10:0] predictedTarget1, predictedTarget2;      // Predicted target addresses
    output reg [10:0] instMemTarget;         // Predicted target for instruction memory

    // Branch History Table (BHT)
    reg [1:0] BHT [0:63]; // 32-entry BHT, 2-bit saturating counters

    // Branch Target Buffer (BTB)
    reg [10:0] BTB_target [0:63];  // 32-entry BTB storing target addresses
    reg BTB_valid [0:63];          // Valid bits for BTB entries

    // Indexes for accessing the BHT and BTB
    wire [5:0] index1 = pc1[5:0];
    wire [5:0] index2 = pc2[5:0];
    wire [5:0] indexM1 = pcM1[5:0];
    wire [5:0] indexM2 = pcM2[5:0];
    wire [5:0] predIndex = nextPC[5:0];

    // Prediction logic for the first branch
    always @(*) begin
        case (BHT[index1])
            2'b11: prediction1 = 1'b1; // Strongly Taken
            2'b10: prediction1 = 1'b1; // Weakly Taken
            2'b01: prediction1 = 1'b0; // Weakly Not Taken
            2'b00: prediction1 = 1'b0; // Strongly Not Taken
            default: prediction1 = 1'b0;
        endcase
        
        // BTB target prediction for first branch
        predictedTarget1 = BTB_valid[index1] ? BTB_target[index1] : pc1 + 11'd1;
    end

    // Prediction logic for the second branch
    always @(*) begin
        case (BHT[index2])
            2'b11: prediction2 = 1'b1;
            2'b10: prediction2 = 1'b1;
            2'b01: prediction2 = 1'b0;
            2'b00: prediction2 = 1'b0;
            default: prediction2 = 1'b0;
        endcase
        
        // BTB target prediction for second branch
        predictedTarget2 = BTB_valid[index2] ? BTB_target[index2] : pc2 + 11'd1;
    end

    // Prediction logic for instruction memory
    always @(*) begin
        case (BHT[predIndex])
            2'b11: instMemPred = 1'b1;
            2'b10: instMemPred = 1'b1;
            2'b01: instMemPred = 1'b0;
            2'b00: instMemPred = 1'b0;
            default: instMemPred = 1'b0;
        endcase
        
        // BTB target prediction for instruction memory
        instMemTarget = BTB_valid[predIndex] ? BTB_target[predIndex] : nextPC + 11'd1;
    end

    // Update logic for the BHT and BTB
    always @(posedge clk or negedge reset) begin : bLoCk
        integer i;
        if (~reset) begin
            // Initialize BHT to Weakly Not Taken (2'b01)
            for (i = 0; i < 64; i = i + 1) begin
                BHT[i] <= 2'b01;
                BTB_valid[i] <= 1'b0;  // Initialize BTB valid bits to invalid
                BTB_target[i] <= 11'd0; // Initialize BTB targets to 0
            end
        end else begin
            // Update BHT and BTB for the first branch
            if (branch1) begin
                // Update BHT
                case (BHT[indexM1])
                    2'b11: BHT[indexM1] <= branch_taken1 ? 2'b11 : 2'b10;
                    2'b10: BHT[indexM1] <= branch_taken1 ? 2'b11 : 2'b01;
                    2'b01: BHT[indexM1] <= branch_taken1 ? 2'b10 : 2'b00;
                    2'b00: BHT[indexM1] <= branch_taken1 ? 2'b01 : 2'b00;
                endcase
                
                // Update BTB
                if (branch_taken1) begin
                    BTB_target[indexM1] <= targetM1;
                    BTB_valid[indexM1] <= 1'b1;
                end
            end

            // Update BHT and BTB for the second branch
            if (branch2) begin
                // Update BHT
                case (BHT[indexM2])
                    2'b11: BHT[indexM2] <= branch_taken2 ? 2'b11 : 2'b10;
                    2'b10: BHT[indexM2] <= branch_taken2 ? 2'b11 : 2'b01;
                    2'b01: BHT[indexM2] <= branch_taken2 ? 2'b10 : 2'b00;
                    2'b00: BHT[indexM2] <= branch_taken2 ? 2'b01 : 2'b00;
                endcase
                
                // Update BTB
                if (branch_taken2) begin
                    BTB_target[indexM2] <= targetM2;
                    BTB_valid[indexM2] <= 1'b1;
                end
            end
        end
    end
endmodule