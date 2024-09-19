`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/28 19:19:39
// Design Name: 
// Module Name: JK_FF_tb
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


module JK_FF_tb();
    reg CLK;
    reg J;
    reg K;
    reg RST_n;
    wire Q1;
    wire Q2;
    
    initial
    begin
        J = 0;
        K = 1;
        RST_n = 1;
        CLK = 1;
        #5;
        CLK = 0;
        #5;
        J = 1;
        K = 0;
        #5;
        CLK = 1;
        #5;
        CLK = 0;
        #5;
        J = 0;
        K = 0;
        #5;
        CLK = 1;
        #5;
        CLK = 0;
        #5;
        RST_n = 0;
        #5;
        J = 1;
        K = 1;
        #5;
        CLK = 1;
        RST_n = 1;
    
    end
    
    JK_FF JK_FF_inst(CLK, J, K, RST_n, Q1, Q2);
    
endmodule
