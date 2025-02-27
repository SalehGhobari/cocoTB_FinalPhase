module BranchPredictionUnit (
    clk, reset, branch1, branch2, branch_taken1, branch_taken2,
    pc1, pc2, pcM1, pcM2, targetM1, targetM2, prediction1, prediction2, 
    nextPC, instMemPred, predictedTarget1, instMemTarget
);
    // Inputs
    input clk, reset;
    input branch1, branch2;            // Branch signals for the two instructions
    input branch_taken1, branch_taken2; // Whether the branches were taken or not
    input wire [7:0] pc1, pc2;            // Program counters for the two instructions
    input wire [7:0] pcM1, pcM2;          // Program counters for the two instructions in Memory stage
    input wire [7:0] nextPC;
    input wire [7:0] targetM1, targetM2;   // Actual branch targets from Memory stage

    // Outputs
    output reg prediction1, prediction2, instMemPred;          // Predictions for the three branches
    output reg [7:0] predictedTarget1;      // Predicted target addresses
    output reg [7:0] instMemTarget;         // Predicted target for instruction memory

    // Branch History Table (BHT)
    //attribute ramstyle of BHT is "M9K"
    (* ramstyle = "M9K" *) reg [1:0] BHT [0:255]; // 256-entry BHT, 2-bit saturating counters

    // Branch Target Buffer (BTB)
    //attribute ramstyle of BTB is "M9K"
    (* ramstyle = "M9K" *) reg [8:0] BTB [0:255];  // 256-entry BTB storing target addresses and valid bit
    // BTB[addr][8] is valid bit, BTB[addr][7:0] is target

    // Extract values for cleaner code
    wire [1:0] bht_pc1 = BHT[pc1];
    wire [1:0] bht_pc2 = BHT[pc2];
    wire [1:0] bht_nextPC = BHT[nextPC];
    
    wire [8:0] btb_pc1 = BTB[pc1];
    wire [8:0] btb_nextPC = BTB[nextPC];
    
    // Simplified prediction logic - MSB of counter determines prediction
	 always @(*) begin 
	  prediction1 = bht_pc1[1];
     prediction2 = bht_pc2[1];
     instMemPred = bht_nextPC[1];
	  
	  predictedTarget1 = btb_pc1[8] ? btb_pc1[7:0] : (pc1 + 8'd1);
     instMemTarget = btb_nextPC[8] ? btb_nextPC[7:0] : (nextPC + 8'd1);
	 end
  
    
    // Function to update counter based on outcome
    function [1:0] update_counter;
        input [1:0] counter;
        input taken;
        begin
            case ({counter, taken})
                {2'b00, 1'b0}: update_counter = 2'b00; // Strongly not taken -> stay
                {2'b00, 1'b1}: update_counter = 2'b01; // Strongly not taken -> weakly not taken
                {2'b01, 1'b0}: update_counter = 2'b00; // Weakly not taken -> strongly not taken
                {2'b01, 1'b1}: update_counter = 2'b10; // Weakly not taken -> weakly taken
                {2'b10, 1'b0}: update_counter = 2'b01; // Weakly taken -> weakly not taken
                {2'b10, 1'b1}: update_counter = 2'b11; // Weakly taken -> strongly taken
                {2'b11, 1'b0}: update_counter = 2'b10; // Strongly taken -> weakly taken
                {2'b11, 1'b1}: update_counter = 2'b11; // Strongly taken -> stay
                default:       update_counter = 2'b01; // Default (should never happen)
            endcase
        end
    endfunction

    // Update logic for the BHT and BTB - use single procedural block
    // and reduce redundant logic
    
    always @(posedge clk or negedge reset) begin : block
	 integer i;
        if (~reset) begin
			
            // Initialize only what's necessary in reset
            for (i = 0; i < 256; i = i + 1) begin
                BHT[i] <= 2'b01;      // Initialize to Weakly Not Taken
                BTB[i] <= 9'b0;       // Initialize BTB (valid=0, target=0)
            end
        end else begin
            // Update for branch1
            if (branch1) begin
                BHT[pcM1] <= update_counter(BHT[pcM1], branch_taken1);
                
                if (branch_taken1) begin
                    BTB[pcM1] <= {1'b1, targetM1}; // Valid bit + target
                end
            end

            // Update for branch2
            if (branch2) begin
                BHT[pcM2] <= update_counter(BHT[pcM2], branch_taken2);
                
                if (branch_taken2) begin
                    BTB[pcM2] <= {1'b1, targetM2}; // Valid bit + target
                end
            end
        end
    end
endmodule 