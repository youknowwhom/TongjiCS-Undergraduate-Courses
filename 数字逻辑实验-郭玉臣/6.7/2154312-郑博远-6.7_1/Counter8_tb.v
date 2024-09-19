`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/07 00:34:39
// Design Name: 
// Module Name: Counter8_tb
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


module Counter8_tb();
    reg CLK;
    reg rst_n;
    wire[2:0] oQ;
    wire[6:0] oDisplay;
    
    integer i;
    
    initial
    begin
        rst_n = 0;
        CLK = 0;
        #5;
        rst_n = 1;
        for(i = 0; i <= 18; i = i + 1)
        begin
            CLK = 1;
            #5;
            CLK = 0;
            #5;
        end
       
       rst_n = 0;
        
    end
    
    Counter8 Counter8_inst(CLK, rst_n, oQ, oDisplay);
endmodule
