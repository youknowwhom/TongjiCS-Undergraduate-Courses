`timescale 1ns / 1ps

module mux2_5(
    input [4:0]         d0,
    input [4:0]         d1,
    input               sel,
    output reg [4:0]    y
    );
	
    always@(*) 
    begin
        case(sel)
            1'b0: y <= d0;
            1'b1: y <= d1;
        endcase
    end
	
endmodule

module mux2_32(
    input [31:0]        d0,
    input [31:0]        d1,
    input               sel,
    output reg [31:0]   y
    );
	
    always@(*) 
    begin
        case(sel)
            1'b0: y <= d0;
            1'b1: y <= d1;
        endcase
    end
	
endmodule

module mux4_32(
    input   [31:0]      d0,
    input   [31:0]      d1,
    input   [31:0]      d2,
    input   [31:0]      d3,
    input   [1:0]       sel,
    output reg [31:0]   y
    );
	
    always@(*) 
    begin
        case(sel)
            2'b00:      y <= d0;
            2'b01:      y <= d1;
            2'b10:      y <= d2;
            2'b11:      y <= d3;
        endcase
   end

endmodule

module mux8_32(
    input   [31:0]      d0,
    input   [31:0]      d1,
    input   [31:0]      d2,
    input   [31:0]      d3,
    input   [31:0]      d4,
    input   [31:0]      d5,
    input   [31:0]      d6,
    input   [31:0]      d7,
    input   [2:0]       sel,
    output reg [31:0]   y
    ); 
	
    always@(*) 
    begin
        case(sel)
            3'b000:     y <= d0;
            3'b001:     y <= d1;
            3'b010:     y <= d2;
            3'b011:     y <= d3;
            3'b100:     y <= d4;
            3'b101:     y <= d5;
            3'b110:     y <= d6;
            3'b111:     y <= d7;
        endcase
    end
	
endmodule
