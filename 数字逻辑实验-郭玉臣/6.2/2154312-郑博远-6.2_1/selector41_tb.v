`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/09/26 01:06:25
// Design Name: 
// Module Name: selector41_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module selector41_tb;
     reg [3:0] iC0, iC1, iC2, iC3;
     reg iS0, iS1;
     wire [3:0] oZ;
     initial begin
        iC0 = 4'b0001;
        iC1 = 4'b0010;
        iC2 = 4'b0100;
        iC3 = 4'b1000;
     end
     
     initial begin
        {iS1, iS0} = 2'b00;
        #10;
        {iS1, iS0} = 2'b01;
        #10;
        {iS1, iS0} = 2'b10;
        #10;
        {iS1, iS0} = 2'b11;
     end
     selector41 selector41_inst(iC0, iC1, iC2, iC3, iS1, iS0, oZ);
endmodule
