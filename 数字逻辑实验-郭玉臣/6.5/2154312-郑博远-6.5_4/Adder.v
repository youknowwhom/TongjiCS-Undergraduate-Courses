`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/24 19:16:53
// Design Name: 
// Module Name: Adder
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
module FA(
    input iA,
    input iB,
    input iC,
    output oS,
    output oC
    );
    
    wire AandB, AxorB, Cand;
    
    xor (AxorB, iA, iB);
    and (Cand, iC, AxorB);
    and (AandB, iA, iB);
    
    or(oC, AandB, Cand);
    xor(oS, iC, AxorB);
    
endmodule



module Adder(
    input[7:0] iData_a,
    input[7:0] iData_b,
    input iC,
    output[7:0] oData,
    output oData_C
    );
    
    wire [6:0]carrybit;
    FA FA0(iData_a[0], iData_b[0], iC, oData[0], carrybit[0]);
    FA FA1(iData_a[1], iData_b[1], carrybit[0], oData[1], carrybit[1]);
    FA FA2(iData_a[2], iData_b[2], carrybit[1], oData[2], carrybit[2]);
    FA FA3(iData_a[3], iData_b[3], carrybit[2], oData[3], carrybit[3]);
    FA FA4(iData_a[4], iData_b[4], carrybit[3], oData[4], carrybit[4]);
    FA FA5(iData_a[5], iData_b[5], carrybit[4], oData[5], carrybit[5]);
    FA FA6(iData_a[6], iData_b[6], carrybit[5], oData[6], carrybit[6]);
    FA FA7(iData_a[7], iData_b[7], carrybit[6], oData[7], oData_C);
    
endmodule
