module registerFile_tb;
    reg clk, rst, we1, we2;
    reg [4:0] readRegister1, readRegister2, readRegister3, readRegister4;
    reg [4:0] writeRegister1, writeRegister2;
    reg [31:0] writeData1, writeData2;
    wire [31:0] readData1, readData2, readData3, readData4;

    // Instantiate the register file module
    registerFile uut (
        .clk(clk), .rst(rst), .we1(we1), .we2(we2),
        .readRegister1(readRegister1), .readRegister2(readRegister2),
        .readRegister3(readRegister3), .readRegister4(readRegister4),
        .writeRegister1(writeRegister1), .writeRegister2(writeRegister2),
        .writeData1(writeData1), .writeData2(writeData2),
        .readData1(readData1), .readData2(readData2),
        .readData3(readData3), .readData4(readData4)
    );

    // Clock generation
    always #5 clk = ~clk;

    initial begin
        // Initialize signals
        clk = 0; rst = 1; we1 = 0; we2 = 0;
        readRegister1 = 0; readRegister2 = 0;
        readRegister3 = 0; readRegister4 = 0;
        writeRegister1 = 0; writeRegister2 = 0;
        writeData1 = 0; writeData2 = 0;

        // Reset the register file
        rst = 0;
        #10 rst = 1;

        // Write data to registers
        #10 we1 = 1; writeRegister1 = 5; writeData1 = 32'hAAAA_AAAA;
        we2 = 1; writeRegister2 = 10; writeData2 = 32'h5555_5555;
        #10 we1 = 0; we2 = 0;

        // Read data from registers
        #10 readRegister1 = 5; readRegister2 = 10;
        readRegister3 = 5; readRegister4 = 10;
		  
        #20 $stop;
    end
endmodule
