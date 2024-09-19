`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/16 18:59:11
// Design Name: 
// Module Name: DataCompare4_tb
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


module DataCompare4_tb();
    reg [3:0] iData_a;
    reg [3:0] iData_b;
    reg [2:0] iData;
    wire [2:0] oData;
    
    initial
    begin
        iData_a = 4'b1111;
        iData_b = 4'b0000;
        iData = 3'b000;
        #5;
        iData_a = 4'b0000;
        iData_b = 4'b1111;
        #5;
        iData_a = 4'b1100;
        iData_b = 4'b1100;
        iData = 3'b100;
        #5;
        iData = 3'b010;
        #5;
        iData = 3'b001;
        #5;
    end
    
    DataCompare4 DataCompare4_inst(iData_a, iData_b, iData, oData);
    
endmodule
