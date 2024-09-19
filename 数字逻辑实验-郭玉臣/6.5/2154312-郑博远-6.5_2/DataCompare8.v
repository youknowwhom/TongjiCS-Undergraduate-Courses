`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/17 23:55:13
// Design Name: 
// Module Name: DataCompare8
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


module DataCompare8(
    input[7:0] iData_a,
    input[7:0] iData_b,
    output reg[2:0] oData
    );
    

    always@(*)
    begin
        if(iData_a > iData_b)
            oData = 3'b100;
        else if(iData_a < iData_b)
            oData = 3'b010;
        else
            oData = 3'b001;
    end
   
endmodule
