`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/28 17:19:32
// Design Name: 
// Module Name: Synchronous_D_FF_tb
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


module Synchronous_D_FF_tb();
    reg CLK;
    reg D;
    reg RST_n;
    wire Q1;
    wire Q2;
    
    initial
    begin
        RST_n = 1;
        D = 0;
        #5;
        CLK = 1;
        #5;
        CLK = 0;
        #5;
        D = 1;
        #5;
        CLK = 1;
        #5;
        CLK = 0;
        #5;
        RST_n = 0;
        #5;
        CLK = 1;
        #5;
        RST_n = 1;
        CLK = 0;
        #5;
        CLK = 1;
    end    
    
    Synchronous_D_FF Synchronous_D_FF_inst(CLK, D, RST_n, Q1, Q2);
    
endmodule
