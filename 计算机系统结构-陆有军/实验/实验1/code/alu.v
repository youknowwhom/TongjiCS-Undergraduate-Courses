`timescale 1ns / 1ns

module alu(
    input   [31:0]  a,
    input   [31:0]  b,
    output  [31:0]  y,
    input   [3:0]   aluc,
    output          zero,
    output          carry,
    output          negative,
    output          overflow
    );
    
    wire signed [31:0] signedA, signedB;
    reg [32:0] ans;
    
    assign signedA = a;
    assign signedB = b;
    
    parameter ADD   =   4'b0000;
    parameter ADDU  =   4'b0001;
    parameter SUB   =   4'b0010;
    parameter SUBU  =   4'b0011;
    parameter AND   =   4'b0100;
    parameter OR    =   4'b0101;
    parameter XOR   =   4'b0110;
    parameter NOR   =   4'b0111;
    parameter SLT   =   4'b1000;
    parameter SLTU  =   4'b1001;
    parameter SLL   =   4'b1010;
    parameter SRL   =   4'b1011;
    parameter SRA   =   4'b1100;
    parameter LUI   =   4'b1101;
    
    always@ (*)
    begin
        case(aluc)
            ADD:
            begin
                ans = signedA + signedB;
            end
            ADDU:
            begin
                ans = a + b;
            end
            SUB:
            begin
                ans = signedA - signedB;
            end
            SUBU: 
            begin
                ans = a - b;
            end
            AND:
            begin
                ans = a & b;
            end
            OR:
            begin
                ans = a | b;
            end
            XOR:
            begin
                ans = a ^ b;
            end
            NOR:
            begin
                ans = ~(a | b);
            end
            SLT: 
            begin
                ans = (signedA < signedB);
            end
            SLTU:
            begin
                ans = (a < b);
            end
            SLL:
            begin
                ans = (b << a);
            end
            SRL:
            begin
                if(a == 0) 
                    { ans[31:0], ans[32] } = { b, 1'b0 };
                else
                    { ans[31:0], ans[32] } = b >> (a - 1);
            end
            SRA:
            begin
                if(a == 0) 
                    { ans[31:0], ans[32] } = { signedB, 1'b0 };
                else
                    { ans[31:0], ans[32] } = signedB >>> (a - 1);
            end
            LUI:
            begin
                ans = { b[15:0], 16'b0 };
            end
        endcase
    end
    
    assign y        = ans[31:0];
    assign zero     = (ans == 32'b0) ? 1'b1 : 1'b0;
    assign carry    = ans[32];
    assign overflow = ans[32] ^ ans[31];
    assign negative = ans[31];
    
endmodule