`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/07 22:46:48
// Design Name: 
// Module Name: encoder83_tb
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


module encoder83_tb;
    reg [8:0] iData;
    wire [2:0] oData;
    
    initial
    begin
        for(iData = 8'b00000001; iData <= 8'b10000000; iData = iData << 1)
        begin
            #20;
        end
    end
    
    encoder83 encoder83_inst(iData[7 : 0], oData);
    
endmodule
