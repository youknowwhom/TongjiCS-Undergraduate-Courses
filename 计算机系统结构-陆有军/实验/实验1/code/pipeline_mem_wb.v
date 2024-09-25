`timescale 1ns / 1ns

module pipe_mem_wb(
    input               in_clk,
    input               in_rst,

    input       [4:0]   in_rd_waddr,
    input               in_rd_sel,
    input               in_rd_wena,

    input       [31:0]  in_alu_result,
    input       [31:0]  in_dmem_data,

    output reg  [4:0]   out_rd_waddr,
    output reg          out_rd_wena,
    output reg          out_rd_sel,

    output reg  [31:0]  out_alu_result,
    output reg  [31:0]  out_dmem_data
    );

    always @(posedge in_clk or posedge in_rst) 
    begin
        if(in_rst == 1'b1) 
        begin
            out_rd_waddr    <= 5'b0;
            out_rd_sel      <= 1'b0;
            out_rd_wena     <= 1'b0;

            out_alu_result  <= 32'b0;
            out_dmem_data   <= 32'b0;
        end
        else 
        begin
            out_rd_waddr    <= in_rd_waddr;
            out_rd_sel      <= in_rd_sel;
            out_rd_wena     <= in_rd_wena;

            out_alu_result  <= in_alu_result;
            out_dmem_data   <= in_dmem_data;
        end
    end 
endmodule