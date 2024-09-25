`timescale 1ns / 1ns

module pipe_ex_mem(
    input               in_clk,
    input               in_rst,

    input               in_dmem_ena,
    input               in_dmem_wena,
    input   [1:0]       in_dmem_type,

    input   [31:0]      in_rs_data,
    input   [31:0]      in_rt_data,
    input   [4:0]       in_rd_waddr,
    input               in_rd_sel,
    input               in_rd_wena,

    input   [31:0]      in_alu_result,

    output reg          out_dmem_ena,
    output reg          out_dmem_wena,
    output reg [1:0]    out_dmem_type,

    output reg [31:0]   out_rs_data,
    output reg [31:0]   out_rt_data,
    output reg [4:0]    out_rd_waddr,
    output reg          out_rd_sel, 
    output reg          out_rd_wena,

    output reg [31:0]   out_alu_result
    );

    always@ (posedge in_clk or posedge in_rst) 
    begin
        if(in_rst) 
        begin
            out_dmem_ena    <= 1'b0;
            out_dmem_wena   <= 1'b0;
            out_dmem_type   <= 2'b0;

            out_rs_data     <= 32'b0;
            out_rt_data     <= 32'b0;
            out_rd_waddr    <= 5'b0;
            out_rd_sel      <= 1'b0;
            out_rd_wena     <= 1'b0;

            out_alu_result  <= 32'b0;
        end
        else 
        begin
            out_dmem_ena    <= in_dmem_ena;
            out_dmem_wena   <= in_dmem_wena;
            out_dmem_type   <= in_dmem_type;

            out_rs_data     <= in_rs_data;
            out_rt_data     <= in_rt_data;
            out_rd_waddr    <= in_rd_waddr;
            out_rd_sel      <= in_rd_sel;
            out_rd_wena     <= in_rd_wena;

            out_alu_result  <= in_alu_result;
        end
    end 

endmodule