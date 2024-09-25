`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/09/19 20:43:09
// Design Name: 
// Module Name: logic_gates_2
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


module logic_gates_2(iA,iB,oAnd,oOr,oNot); 
    input iA, iB; 
    output oAnd,oOr,oNot; 
    assign oAnd = iA & iB; 
    assign oOr = iA | iB; 
    assign oNot = ~iA; 
endmodule