`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/07 15:36:20
// Design Name: 
// Module Name: display7
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


module display7(
    input [3:0] iData,
    output reg [6:0] oData
);

    always @(*)
    begin
        case(iData)
            4'b0000 : oData = 7'b1000000;
            4'b0001 : oData = 7'b1111001;
            4'b0010 : oData = 7'b0100100;
            4'b0011 : oData = 7'b0110000;
            4'b0100 : oData = 7'b0011001;
            4'b0101 : oData = 7'b0010010;
            4'b0110 : oData = 7'b0000010;
            4'b0111 : oData = 7'b1111000;
            4'b1000 : oData = 7'b0000000;
            4'b1001 : oData = 7'b0010000;
        endcase
    end
    
endmodule
