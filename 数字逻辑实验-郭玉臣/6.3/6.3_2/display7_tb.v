`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/07 22:08:03
// Design Name: 
// Module Name: display7_tb
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


module display7_tb;
    reg [3:0] iData;
    wire[6:0] oData;
       
    initial
        begin
        for(iData = 0; iData <= 4'b1001; iData = iData + 4'b0001)
            #20;
        end    
    
    display7 display7_inst(iData, oData);
    
endmodule
