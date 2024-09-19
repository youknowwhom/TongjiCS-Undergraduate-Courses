`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/09/26 11:12:03
// Design Name: 
// Module Name: de_selector14_tb
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


module de_selector14_tb;
    reg iC;
    reg iS0, iS1;
    wire oZ0, oZ1, oZ2, oZ3;
    initial begin
        iC = 0;
        #10;
        iC = 1;
        #10;
        iC = 0;
        #10;
        iC = 1;
        #10;
        iC = 0;
        #10;
        iC = 1;
        #10;
        iC = 0;
        #10;
        iC = 1;
    end
    
    initial begin
        {iS1, iS0} = 2'b00;
        #20;
        {iS1, iS0} = 2'b01;
        #20;
        {iS1, iS0} = 2'b10;
        #20;
        {iS1, iS0} = 2'b11;
    end
    
    de_selector14 de_selector14_inst(iC, iS1, iS0, oZ0, oZ1, oZ2, oZ3);
endmodule
