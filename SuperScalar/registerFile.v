module registerFile (
     clk, rst, we1, we2, readRegister1, readRegister2, readRegister3, readRegister4,writeRegister1,
	  writeRegister2,writeData1, writeData2, readData1, readData2, readData3, readData4);

	 input clk, rst, we1, we2;
    input [4:0] readRegister1, readRegister2, readRegister3, readRegister4;
    input [4:0] writeRegister1, writeRegister2;
    input [31:0] writeData1, writeData2;
    output reg [31:0] readData1, readData2, readData3, readData4;

    // Register file (32 registers)
    reg [31:0] registers [0:31];

    // Read from the register file
    always @(*) begin
        readData1 = registers[readRegister1];
        readData2 = registers[readRegister2];
        readData3 = registers[readRegister3];
        readData4 = registers[readRegister4];
    end

    // Write to the register file
    always @(negedge clk or negedge rst) begin : block
        integer i;
        if (~rst) begin
            for (i = 0; i < 32; i = i + 1) registers[i] = 0;
        end else begin
            if (we1 && writeRegister1 != 0 && writeRegister2 != writeRegister1) registers[writeRegister1] <= writeData1;
            if (we2 && writeRegister2 != 0 ) 
                registers[writeRegister2] <= writeData2;
        end
    end

endmodule
