`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/28 19:13:43
// Design Name: 
// Module Name: JK_FF
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


module JK_FF(
    input CLK,
    input J,
    input K,
    input RST_n,
    output reg Q1,
    output reg Q2
);

    always@ (posedge CLK or negedge RST_n)
    begin
        if(!RST_n)
        begin
            Q1 <= 0;
            Q2 <= 1;
        end
        else
        begin
            case({J, K})
            2'b00: 
            begin
                Q1 <= Q1; 
                Q2 <= Q2;
            end
            2'b01:
            begin
                Q1 <= 0;
                Q2 <= 1;
            end
            2'b10:
            begin
                Q1 <= 1;
                Q2 <= 0;
            end
            2'b11:
            begin
                Q1 <= !Q1;
                Q2 <= !Q2;
            end
            endcase 
        end       
    end
    
endmodule
