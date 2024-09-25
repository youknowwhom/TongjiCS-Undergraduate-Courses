`timescale 1ns / 1ps

module alu (
    input [31:0]    a,    
    input [31:0]    b, 
    input [3:0]     aluc,
    output [31:0]   y,
    output          zero,
    output          carry, 
    output          negative, 
    output          overflow
    );

    wire signed [31:0] signedA, signedB;
    reg [32:0] ans;
    
    assign signedA = a;
    assign signedB = b;

    always@(*) 
    begin
        case(aluc)
            4'b0000: ans = a + b;
            4'b0010: ans = signedA + signedB;
            4'b0001: ans = a - b;
            4'b0011: ans = signedA - signedB;
            4'b0100: ans = a & b;
            4'b0101: ans = a | b;
            4'b0110: ans = a ^ b;
            4'b0111: ans = ~(a | b);
            4'b1000: ans = { b[15:0], 16'b0 };
            4'b1001: ans = { b[15:0], 16'b0 };
            4'b1011: ans = (signedA < signedB);
            4'b1010: ans = (a < b);
            4'b1100:
            begin
                if(a == 0) 
                    { ans[31:0], ans[32] } = { signedB, 1'b0 };
                else
                    { ans[31:0], ans[32] } = signedB >>> (a - 1);
            end
            4'b1110: ans = b << a;
            4'b1111: ans = b << a;
            4'b1101:
            begin
                if(a == 0) 
                    { ans[31:0], ans[32] } = { b, 1'b0 };
                else
                    { ans[31:0], ans[32] } = b >> (a - 1);
            end
        endcase
    end
    
    assign y        = ans[31:0];

    assign zero     = (ans == 32'b0) ? 1'b1 : 1'b0;
    assign carry    = ans[32];
    assign overflow = ans[32] ^ ans[31];
    assign negative = ans[31];
    
endmodule