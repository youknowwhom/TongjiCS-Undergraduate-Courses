`timescale 1ns / 1ns

module pipe_ex(
    input           in_rst,

    input           in_dmem_ena,
    input           in_dmem_wena,
    input   [1:0]   in_dmem_type,

    input   [31:0]  in_rs_data,
    input   [31:0]  in_rt_data,
    input   [4:0]   in_rd_waddr,
    input           in_rd_sel,
    input           in_rd_wena,

    input   [31:0]  in_immed,
    input   [31:0]  in_shamt,

    input           in_alu_a_sel,
    input           in_alu_b_sel,
    input   [3:0]   in_alu_sel,

    output          out_dmem_ena,
    output          out_dmem_wena,
    output  [1:0]   out_dmem_type,

    output  [31:0]  out_rs_data,
    output  [31:0]  out_rt_data,
    output  [4:0]   out_rd_waddr,
    output          out_rd_sel,
    output          out_rd_wena,

    output  [31:0]  out_alu_result
    );
    
    wire [31:0] a;
    wire [31:0] b;
    wire zero, carry, negative, overflow;

    assign out_dmem_ena     = in_dmem_ena;
    assign out_dmem_wena    = in_dmem_wena;
    assign out_dmem_type    = in_dmem_type;

    assign out_rs_data      = in_rs_data;
    assign out_rt_data      = in_rt_data;
    assign out_rd_waddr     = in_rd_waddr;
    assign out_rd_sel       = in_rd_sel;
    assign out_rd_wena      = in_rd_wena;

    assign a = in_alu_a_sel ? in_shamt : in_rs_data;
    assign b = in_alu_b_sel ? in_immed : in_rt_data;

    alu alu_uut(
        .a(a), 
        .b(b), 
        .y(out_alu_result),
        .aluc(in_alu_sel), 
        .zero(zero),
        .carry(carry),
        .negative(negative),
        .overflow(overflow)
    );

endmodule
