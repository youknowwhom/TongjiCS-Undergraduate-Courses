`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/07 09:05:32
// Design Name: 
// Module Name: Divider_tb
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


module Divider_tb();
    reg I_CLK;
    reg rst;
    wire O_CLK;
    integer i;
    
    initial
    begin
        rst = 1;
        #5;
        I_CLK = 1;
        #5;
        rst = 0;
        I_CLK = 0;
        
        for(i = 0; i <= 35; i = i + 1)
        begin
            I_CLK = 1;
            #5;
            I_CLK = 0;
            #5;
        end
        
        rst  = 1;
        #5;
        I_CLK = 1;
        #5;
        rst = 0;
        I_CLK = 0;
        
        for(i = 0; i <= 35; i = i + 1)
        begin
            I_CLK = 1;
            #5;
            I_CLK = 0;
            #5;
        end        
    end
    
    Divider Divider_inst(I_CLK, rst, O_CLK);

endmodule
