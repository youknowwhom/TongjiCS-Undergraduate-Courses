`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/08 00:12:24
// Design Name: 
// Module Name: encoder83_Pri_tb
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


module encoder83_Pri_tb;
    reg [8:0] iData;
    reg iEI;
    wire [2:0] oData;
    wire oEO;
    
    initial
    begin
        iEI = 0;
        for(iData = 8'b01111111; iData <= 8'b11111111; iData = iData + 8'b00000001)
            #5;
    end
    
    encoder83_Pri encoder83_Pri_inst(iData[7:0], iEI, oData, oEO);
    
endmodule
