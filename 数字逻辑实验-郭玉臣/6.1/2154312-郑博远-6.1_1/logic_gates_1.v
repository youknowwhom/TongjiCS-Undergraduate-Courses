`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/09/19 19:48:43
// Design Name: 
// Module Name: logic_gates_1
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

module logic_gates_1(iA,iB,oAnd,oOr,oNot); 
    input iA, iB; 
    output oAnd,oOr,oNot; 
    and and_inst(oAnd, iA,iB); 
    or or_inst(oOr, iA,iB); 
    not not_inst(oNot, iA); 
endmodule
