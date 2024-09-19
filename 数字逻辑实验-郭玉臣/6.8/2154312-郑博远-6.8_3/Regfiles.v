`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/13 23:46:42
// Design Name: 
// Module Name: Regfiles
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


module Regfiles(
    input clk,
    input rst,
    input we,
    
    input [4:0] raddr1,
    input [4:0] raddr2,
    input [4:0] waddr,
    input [31:0] wdata,
    output [31:0] rdata1,
    output [31:0] rdata2
);

    wire [31:0] decoder_out;
    wire [31:0] regfile_out [31:0];
    
    decoder decoder_inst(waddr, we, decoder_out);
    
    genvar i;
    generate
        for(i = 0; i < 32; i = i + 1)
            pcreg pcreg_inst(clk, rst, decoder_out[i], wdata, regfile_out[i]);
    endgenerate
    
    selector32_1 selector32_1_inst(regfile_out[0],regfile_out[1],regfile_out[2],regfile_out[3],
    regfile_out[4],regfile_out[5],regfile_out[6],regfile_out[7],
    regfile_out[8],regfile_out[9],regfile_out[10],regfile_out[11],
    regfile_out[12],regfile_out[13],regfile_out[14],regfile_out[15],
    regfile_out[16],regfile_out[17],regfile_out[18],regfile_out[19],
    regfile_out[20],regfile_out[21],regfile_out[22],regfile_out[23],
    regfile_out[24],regfile_out[25],regfile_out[26],regfile_out[27],
    regfile_out[28],regfile_out[29],regfile_out[30],regfile_out[31], raddr1, rdata1, ~we);
    
    selector32_1 selector32_1_inst2(regfile_out[0],regfile_out[1],regfile_out[2],regfile_out[3],
    regfile_out[4],regfile_out[5],regfile_out[6],regfile_out[7],
    regfile_out[8],regfile_out[9],regfile_out[10],regfile_out[11],
    regfile_out[12],regfile_out[13],regfile_out[14],regfile_out[15],
    regfile_out[16],regfile_out[17],regfile_out[18],regfile_out[19],
    regfile_out[20],regfile_out[21],regfile_out[22],regfile_out[23],
    regfile_out[24],regfile_out[25],regfile_out[26],regfile_out[27],
    regfile_out[28],regfile_out[29],regfile_out[30],regfile_out[31], raddr2, rdata2, ~we);
    
endmodule
