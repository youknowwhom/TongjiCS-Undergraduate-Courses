`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/28 22:49:00
// Design Name: 
// Module Name: pcreg_tb
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


module pcreg_tb();
    reg clk;
    reg rst;
    reg ena;
    reg [31:0] data_in;
    wire [31:0] data_out;
    
    initial
    begin
        data_in = 32'b11111111_00000000_11110000_00001111;
        rst = 0;
        ena = 1;
        clk = 1;
        #5;
        clk = 0;
        #5;
        data_in = 32'b11111111_11111111_11111111_11111111;
        #5;
        clk = 1;
        #5;
        clk = 0;
        #5;
        rst = 1;
        #5;
        rst = 0;
        ena = 0;
        #5;
        data_in = 32'b11111111_00000000_11110000_00001111;
        #5;
        clk = 1;
        #5;
        clk = 0;
        ena = 1;
        #5;
        clk = 1; 
    end
    
    pcreg pcreg_inst(clk, rst, ena, data_in, data_out);
    
endmodule
