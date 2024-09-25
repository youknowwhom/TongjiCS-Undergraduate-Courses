`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/07 09:00:25
// Design Name: 
// Module Name: Divider
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


module Divider(
    input I_CLK,
    input rst,
    output reg O_CLK
    );
    
    integer cnt;
    parameter N = 20;
    
    always@ (posedge I_CLK)
    begin
        if(rst)
        begin
            cnt <= 0;
            O_CLK <= 0;
        end
        else if(cnt == N/2 - 1)
        begin
            cnt <= 0;
            O_CLK <= ~O_CLK;
        end
        else
            cnt <= cnt + 1;
    end
    
endmodule
