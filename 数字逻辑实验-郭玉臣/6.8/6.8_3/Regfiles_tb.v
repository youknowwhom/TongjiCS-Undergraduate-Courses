`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/14 19:13:09
// Design Name: 
// Module Name: Regfiles_tb
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


module Regfiles_tb;
    reg clk;
    reg rst;
    reg we;
    reg [4:0] raddr1;
    reg [4:0] raddr2;
    reg [4:0] waddr;
    reg [31:0] wdata;
    wire [31:0] rdata1;
    wire [31:0] rdata2;
    
    initial
    begin
        rst = 0;
        clk = 0;
        forever
        begin
            clk = #5 ~clk;
        end
    end
    
    initial
    begin
        we = 1;
        wdata = 32'b0;
        for(waddr = 0; waddr < 31; waddr = waddr + 1)
        begin
            wdata = wdata + 1;
            #10;
        end
        we = 0;
        for(raddr1 = 0; raddr1 < 31; raddr1 = raddr1 + 1)
        begin
            raddr2 = 30 - raddr1;
            #10;
        end        
    end
    
    Regfiles Regfiles_inst(clk, rst, we, raddr1, raddr2, waddr, wdata, rdata1, rdata2);
    
endmodule
