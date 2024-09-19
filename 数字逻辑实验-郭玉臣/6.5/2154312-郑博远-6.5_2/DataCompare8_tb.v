`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/24 19:09:59
// Design Name: 
// Module Name: DataCompare8_tb
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


module DataCompare8_tb();
    reg[7:0] iData_a;
    reg[7:0] iData_b;
    wire [2:0] oData;
    
    initial
    begin
        iData_a = 8'b11110000;
        iData_b = 8'b00001111;
        #20;
        iData_a = 8'b01010101;
        iData_b = 8'b10101010;
        #20;
        iData_a = 8'b11001100;
        iData_b = 8'b11001100;
        #20;
    end
    
    DataCompare8 DataCompare8_inst(iData_a, iData_b, oData);
    
endmodule
