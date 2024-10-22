`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/21 20:01:14
// Design Name: 
// Module Name: alu_tb
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


module alu_tb;
    reg [31:0] a;
    reg [31:0] b;
    reg [3:0] aluc;
    wire [31:0] r;
    wire zero, carry, negative, overflow;
    
    initial
    begin
    //unsigned plus
        aluc = 4'b0000;
            // carry
        a = 32'b00011100_00000000_00001110_00000010;
        b = 32'b11111111_11111111_11111111_11111111;
            // negative
        #5;
        a = 32'b00011100_00000000_00001110_00000010;
        b = 32'b10000000_00111000_00001000_00000010;
        #5;
            // carry
        a = 32'b11111111_11000000_00001110_01100000;
        b = 32'b11111111_00111001_00001000_00011110;
        #5;

    //signed plus
        aluc = 4'b0010;
            // no overflow
        a = 32'b00011100_00000000_00001110_00000010;
        b = 32'b11111111_11111111_11111111_11111111;
            // negative
        #5;
        a = 32'b00011100_00000000_00001110_00000010;
        b = 32'b10000000_00111000_00001000_00000010;
        #5;
            // no overflow
        a = 32'b11111111_11000000_00001110_01100000;
        b = 32'b11111111_00111001_00001000_00011110;
        #5;
            // overflow
        a = 32'b01111111_11000000_00001110_01100000;
        b = 32'b01111111_00111001_00001000_00011110;
        #5;
            // no overflow
        a = 32'b10110011_11000000_00001110_01100000;
        b = 32'b10001001_00111001_00001000_00011110;
        #5;
        
    //unsigned minus
        aluc = 4'b0001;
            // carry
        a = 32'b00011100_00000000_00001110_00000010;
        b = 32'b11111111_11111111_11111111_11111111;
            // zero
        #5;
        a = 32'b10000000_00111000_00001000_00000010;
        b = 32'b10000000_00111000_00001000_00000010;
        #5;
            // no carry
        a = 32'b11111111_11000000_00001110_01100000;
        b = 32'b11111111_00111001_00001000_00011110;
        #5;
        
    //signed minus
        aluc = 4'b0011;
            // no overflow
        a = 32'b00011100_00000000_00001110_00000010;
        b = 32'b11111111_11111111_11111111_11111111;
            // zero
        #5;
        a = 32'b10000000_00111000_00001000_00000010;
        b = 32'b10000000_00111000_00001000_00000010;
        #5;
            // no overflow
        a = 32'b11111111_11000000_00001110_01100000;
        b = 32'b11111111_00111001_00001000_00011110;
        #5;
            // overflow
        a = 32'b01111111_11000000_00001110_01100000;
        b = 32'b11111111_00111001_00001000_00011110;
        #5;
        
        
    //AND
        aluc = 4'b0100;
            // zero
        a = 32'b00011100_00000000_00001110_00000010;
        b = 32'b11100011_11111111_11110001_11111101;
        #5;
        
    //OR
        aluc = 4'b0101;
        #5;
        
    //XOR
        aluc = 4'b0110;
        #5;
        
    //NOR
        aluc = 4'b0111;
        #5;
        
    //LUI
        aluc = 4'b1001;
        #5;

    //signed compare
        aluc = 4'b1011;
        //no negative
        a = 32'b00011100_00000000_00001110_00000010;
        b = 32'b11111111_11111111_11111111_11111111;
        //negative
        #5;
        a = 32'b00000000_00111000_00001000_00000010;
        b = 32'b00100000_00111000_00001000_00000010;    
        #5;
        
    //unsigned compare
        aluc = 4'b1010;
        //carry
        a = 32'b00011100_00000000_00001110_00000010;
        b = 32'b11111111_11111111_11111111_11111111;
        //no carry
        #5;
        a = 32'b11110000_00111000_00001000_00000010;
        b = 32'b11100000_00111000_00001000_00000010;    
        //zero
        #5;
        a = 32'b11110000_00111000_00001000_00000010;
        b = 32'b11110000_00111000_00001000_00000010;         

    // >>>
        aluc = 4'b1100;
        //carry
        a = 32'b00000000_00000000_00000000_00001000;
        b = 32'b11110000_00000000_00000000_10000000;
        #5;
        
    // >>
        aluc = 4'b1101;
        //no carry
        a = 32'b00000000_00000000_00000000_00001000;
        b = 32'b11110000_00000000_10000000_00000000;
        #5;
        
    // << / <<<
        aluc = 4'b1111;
        //no carry
        a = 32'b00000000_00000000_00000000_00001000;
        b = 32'b11111111_00001111_00000000_00000000;
        #5;

    end
    
    alu alu_inst(a, b, aluc, r, zero, carry, negative, overflow);    

endmodule
