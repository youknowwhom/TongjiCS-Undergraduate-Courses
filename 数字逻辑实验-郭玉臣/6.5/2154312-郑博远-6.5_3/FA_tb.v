`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/17 23:01:24
// Design Name: 
// Module Name: FA_tb
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


module FA_tb;
    wire iA, iB, iC;
    wire oS, oC;
    reg [3 : 0] ABC;
    assign {iA, iB, iC} = ABC[2 : 0];
    
    initial
    begin
    for(ABC = 0; ABC <= 3'b111; ABC = ABC + 1)
        #5;
    end
    
    FA FA_inst(iA, iB, iC, oS, oC);
    
endmodule
