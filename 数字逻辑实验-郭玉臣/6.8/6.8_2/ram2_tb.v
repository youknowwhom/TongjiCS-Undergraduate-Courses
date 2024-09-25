`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/13 10:44:01
// Design Name: 
// Module Name: ram_tb
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


module ram2_tb();
    reg clk, ena, wena;
    reg [4:0] addr;
    wire [31:0] data;
    reg [31:0] data_in;
    reg wr;
    
    initial
    begin
        clk = 0;
        forever
        begin
            clk = #5 ~clk;
        end
    end
    
    assign data = wr ? data_in : 'bz;
    
    initial
    begin    
        ena = 1;
        wena = 1;
        wr = 1;
        data_in = 127;

        
        for(addr = 0; addr < 31; addr = addr + 1)
        begin
            data_in = data_in + 1;
            #10;
        end
        
        wena = 0;
        wr = 0;
        for(addr = 0; addr < 31; addr = addr + 1)
        begin
            #10;
        end
        
        ena = 0;
    end
    
   ram2 ram2_inst(clk, ena, wena, addr, data);
    
endmodule
