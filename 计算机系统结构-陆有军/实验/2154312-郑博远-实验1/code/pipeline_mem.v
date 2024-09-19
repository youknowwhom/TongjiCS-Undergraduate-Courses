`timescale 1ns / 1ns

module pipe_mem(
    input           in_clk,

    input           in_dmem_ena,
    input           in_dmem_wena,
    input   [1:0]   in_dmem_type,

    input   [31:0]  in_rs_data,
    input   [31:0]  in_rt_data,
    input   [4:0]   in_rd_waddr,
    input           in_rd_sel,
    input           in_rd_wena,

    input   [31:0]  in_alu_result,

    output  [4:0]   out_rd_waddr,
    output          out_rd_sel,
    output          out_rd_wena,

    output  [31:0]  out_alu_result,
    output  [31:0]  out_dmem_data
    );
    
    wire [31:0] dmem_addr = (in_alu_result - 32'h10010000) / 4;

    assign out_rd_waddr = in_rd_waddr;
    assign out_rd_sel   = in_rd_sel;
    assign out_rd_wena  = in_rd_wena;
    
    assign out_alu_result = in_alu_result;
    
    dmem dmem_uut(
        .clk(in_clk),
        .ena(in_dmem_ena),
        .wena(in_dmem_wena),
        .addr(dmem_addr),
        .dmem_type(in_dmem_type),
        .data_in(in_rt_data),
        .data_out(out_dmem_data)
    );

endmodule