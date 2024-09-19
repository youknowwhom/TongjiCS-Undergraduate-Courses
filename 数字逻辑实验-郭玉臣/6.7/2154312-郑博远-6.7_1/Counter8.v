`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/07 00:24:17
// Design Name: 
// Module Name: Counter8
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


module Counter8(
    input CLK,
    input rst_n,
    output [2:0] oQ,
    output [6:0] oDisplay
    );
    
    wire Q0, Q1, Q2, Q0n, Q1n, Q2n, Q0ANDQ1;
    
    assign oQ  = {Q2, Q1, Q0};
    JK_FF jk1(CLK, 1, 1, rst_n, Q0, Q0n);
    JK_FF jk2(CLK, Q0, Q0, rst_n, Q1, Q1n);
    and q0andq1(Q0ANDQ1, Q0, Q1);
    JK_FF jk3(CLK, Q0ANDQ1, Q0ANDQ1, rst_n, Q2, Q2n);
    
    display7 display7_inst({0, oQ}, oDisplay);
    
endmodule
