`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/28 22:41:21
// Design Name: 
// Module Name: pcreg
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


module pcreg(
    input clk,
    input rst,
    input ena,
    
    input[31:0] data_in,
    output reg[31:0] data_out
    );
    
    always@ (posedge clk or posedge rst)
    begin
        if(rst)
            data_out <= 0;
        else if(ena)
            data_out <= data_in; 
    end
    
endmodule
