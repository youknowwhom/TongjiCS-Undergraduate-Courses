`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/15 23:35:09
// Design Name: 
// Module Name: barrelshifter32
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


module barrelshifter32(
    input signed [31 : 0] a,
    input [4 : 0] b,
    input [1 : 0] aluc,
    output reg[31 : 0] c
    );
    
    always@(*)
    begin
        case(aluc)
            2'b00 : c = a >>> b;
            2'b10 : c = a >> b;
            2'b01 : c = a <<< b;
            2'b11 : c = a << b;
        endcase
    end
    
endmodule
