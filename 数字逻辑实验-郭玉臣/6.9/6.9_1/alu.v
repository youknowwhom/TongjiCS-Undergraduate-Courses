`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/21 16:31:11
// Design Name: 
// Module Name: alu
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


module alu(
    input [31:0] a,
    input [31:0] b,
    input [3:0] aluc,
    output reg [31:0] r,
    output reg zero,
    output reg carry,
    output reg negative,
    output reg overflow
    );
    
    reg [32:0] ae;
    reg [32:0] be;
    reg [32:0] ce;
    
    reg signed [31:0] sa;
    reg signed [31:0] sb;
    
    always@ (*)
    begin
    ae = {1'b0, a};
    be = {1'b0, b};
        casex(aluc)
            4'b0000:    //unsigned plus
            begin
                r <= a + b;
                zero = (r == 0) ? 1 : 0; 
                ce = ae + be;
                carry <=  ce[32];
                negative <= r[31];
            end
            4'b0010:    //signed plus
            begin
                r <= a + b;
                zero = (r == 0) ? 1 : 0;
                negative <= r[31];
                if( a[31]== 1 && b[31]==1 && r[31] == 0)
                    overflow <= 1'b1;
                else if ( a[31]== 0 && b[31]==0 && r[31] == 1)
                    overflow <= 1'b1;
                else
                    overflow <= 1'b0;
            end
            4'b0001:    //unsigned minus
            begin       
                r <= a - b;
                zero = (r == 0) ? 1 : 0;
                ce = ae - be;
                carry <= ce[32];
                negative <= r[31];
            end
            4'b0011:    //signed minus
            begin
                r <= a - b;
                zero = (r == 0) ? 1 : 0;
                ce = ae - be;
                negative <= r[31];
                if( a[31]== 0 && b[31] == 1 && r[31] == 1)
                  overflow <= 1'b1;
                else if ( a == 1 && b == 0 && r[31] == 0)
                  overflow <= 1'b1;
                else
                  overflow <= 1'b0;
            end
            4'b0100:    // AND
            begin
                r = a & b;
                zero = (r == 0) ? 1 : 0;
                negative <= r[31];
            end
            4'b0101:    // OR
            begin
                r = a | b;
                zero = (r == 0) ? 1 : 0;
                negative <= r[31];
            end
            4'b0110:    // XOR
            begin
                r = a ^ b;
                zero = (r == 0) ? 1 : 0;
                negative <= r[31];
            end
            4'b0111:    // NOR
            begin
                r = ~(a | b);
                zero = (r == 0) ? 1 : 0;
                negative <= r[31];
            end
            4'b100x:    // immediate number -> high position
            begin
                r = {b[15:0], 16'b0};
                zero = (r == 0) ? 1 : 0;
                negative <= r[31];
            end
            4'b1011:    // signed compare
            begin
                zero = (a - b == 0) ? 1 : 0;
                sa = a;
                sb = b;
                negative = (sa < sb) ? 1 : 0;
            end
            4'b1010:    // unsigned compare
            begin
                zero = (a - b == 0) ? 1 : 0;
                carry = (a < b) ? 1 : 0;                
            end
            4'b1100:    // >>>
            begin
                sb = b;
                r = sb >>> a;
                zero = (r == 0) ? 1 : 0;
                carry <= b[a - 1];
                negative <= r[31];
            end
            4'b111x:    // << / <<<
            begin
                r = b << a;
                zero = (r == 0) ? 1 : 0;
                carry <= b[32 - a];
                negative <= r[31];
            end
            4'b1101:    // >>
            begin
                r = b >> a;
                zero = (r == 0) ? 1 : 0;
                carry <= b[a - 1];
                negative <= r[31];
            end
        endcase
    end
    
endmodule
