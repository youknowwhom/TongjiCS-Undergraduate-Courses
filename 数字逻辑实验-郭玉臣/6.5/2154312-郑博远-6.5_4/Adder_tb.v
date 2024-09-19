`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/24 19:24:03
// Design Name: 
// Module Name: Adder_tb
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


module Adder_tb();
    reg[8:0] iData_a;
    reg[8:0] iData_b;
    reg[1:0] iC;
    wire[7:0] oData;
    wire oData_C;
    
    initial
    begin
    for(iData_a = 8'b0000_1100; iData_a <= 8'b1111_1111; iData_a = iData_a + 2'b010)
        for(iData_b = 8'b1111_0000; iData_b <= 8'b1111_1111; iData_b = iData_b + 2'b010)
            for(iC = 0; iC <= 1'b1; iC = iC + 1)
                #5;
    end
    
    Adder Adder_inst(iData_a[7:0], iData_b[7:0], iC[0], oData, oData_C);
endmodule
