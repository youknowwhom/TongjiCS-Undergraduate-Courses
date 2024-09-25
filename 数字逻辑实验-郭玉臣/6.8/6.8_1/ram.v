`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/13 10:32:02
// Design Name: 
// Module Name: ram
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


module ram(
    input clk,
    input ena,
    input wena,
    input [4:0] addr,
    input [31:0] data_in,
    output reg [31:0] data_out
);

    reg[31:0] RAM [31:0];

    always @(posedge clk)
    if(ena)
    begin
        if(wena)
            RAM[addr] <= data_in;
        else
            data_out <= RAM[addr];
    end
    else
    begin
        data_out = 32'bz;
    end
    
endmodule
