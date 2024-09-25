`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/17 22:51:00
// Design Name: 
// Module Name: FA
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
