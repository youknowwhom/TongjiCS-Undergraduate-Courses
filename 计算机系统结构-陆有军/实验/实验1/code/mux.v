`timescale 1ns / 1ns

module mux4_5(
    input [4:0] d0,
    input [4:0] d1,
    input [4:0] d2,
    input [4:0] d3,
    input [1:0]  s,
    output reg [4:0] y
    );

    always@(*)
    begin
        case(s)
            2'b00:  y <= d0;
            2'b01:  y <= d1;   
            2'b10:  y <= d2;
            2'b11:  y <= d3;
        endcase
    end

endmodule

module mux4_32(
    input [31:0] d0,
    input [31:0] d1,
    input [31:0] d2,
    input [31:0] d3,
    input [1:0]  s,
    output reg [31:0] y
    );

    always@(*)
    begin
        case(s)
            2'b00:  y <= d0;
            2'b01:  y <= d1;   
            2'b10:  y <= d2;
            2'b11:  y <= d3;
        endcase
    end

endmodule