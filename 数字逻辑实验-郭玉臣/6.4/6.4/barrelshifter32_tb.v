`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/15 23:47:36
// Design Name: 
// Module Name: barrelshifter32_tb
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


module barrelshifter32_tb();
    reg [31 : 0] a;
    reg [5 : 0] b;
    reg [2 : 0] aluc;
    wire [31 : 0] c;
    
    initial
    begin
        a = 32'b1111_0000_1100_0011_1001_0110_0001_1110;
        for(b = 0; b <= 4'b11111; b = b + 4'b00001)
            for(aluc = 0; aluc <= 2'b11; aluc = aluc + 2'b01)
            begin
                #5;
            end
    end
    
    barrelshifter32 barrelshifter_inst(a, b, aluc, c);
    
endmodule
