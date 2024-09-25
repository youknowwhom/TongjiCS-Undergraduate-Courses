`timescale 1ns / 1ns

module pipe_id(
    input           in_clk,
    input           in_rst,

    input   [31:0]  in_npc,
    input   [31:0]  in_instruction,
 
	input   [4:0]   in_ex_waddr,
	input   [4:0]   in_mem_waddr,
    input           in_ex_wena,
    input           in_mem_wena,

    input   [4:0]   in_wb_reg_addr,
    input           in_wb_reg_ena,
    input   [31:0]  in_wb_reg_data,

    input   [31:0]  init_floors,
    input   [31:0]  init_resistance,

    output  [31:0]      out_rs_data,
    output  [31:0]      out_rt_data,
    output  [4:0]       out_rd_waddr,
    output              out_rd_sel,
    output              out_rd_wena,
    output  [31:0]      out_immed,
    output  [31:0]      out_shamt,

    output              out_dmem_ena,
    output              out_dmem_wena,
    output  [1:0]       out_dmem_type,

    output  [31:0]      out_pc_baddr,
    output  [31:0]      out_pc_jaddr,
    output  [1:0]       out_pc_sel,

    output              out_alu_a_sel,
    output              out_alu_b_sel,
    output [3:0]        out_alu_sel,

    output              out_stall,
    output              out_branch,

    output  [31:0]      result_attempt_count,
    output  [31:0]      result_broken_count,
    output              result_is_last_broken
    );

    // 解析指令的各个部分
    wire [5:0] inst_op   = in_instruction[31:26];
    wire [5:0] inst_func = in_instruction[ 5: 0];
    wire [4:0] rs_addr   = in_instruction[25:21];
    wire [4:0] rt_addr   = in_instruction[20:16];
    wire [4:0] rd_addr   = in_instruction[15:11];

    wire rs_rena, rt_rena;
    wire ext_signed;

    assign out_immed = { { 16{ ext_signed & in_instruction[15] } }, in_instruction[15:0] };
    assign out_shamt = { 27'b0, in_instruction[10:6] };

    assign out_pc_baddr = in_npc + { { 14{ in_instruction[15] }}, in_instruction[15:0], 2'b0 };
    assign out_pc_jaddr = { in_npc[31:28], in_instruction[25:0], 2'b0 };
    assign out_npc = in_npc;

    assign out_branch = (((inst_op == 6'b000100) && (out_rs_data == out_rt_data)) || ((inst_op == 6'b000101) && (out_rs_data != out_rt_data)) || (inst_op == 6'b000010));

    // 寄存器堆
    regfile regfile_uut(
        .in_clk(in_clk),
        .in_rst(in_rst),

        .in_rs_rena(rs_rena),
        .in_rt_rena(rt_rena),
        .in_rd_wena(in_wb_reg_ena),
        .in_rs_addr(rs_addr),
        .in_rt_addr(rt_addr),
        .in_rd_addr(in_wb_reg_addr),
        .in_rd_data(in_wb_reg_data),

        .init_floors(init_floors),
        .init_resistance(init_resistance),

        .out_rs_data(out_rs_data),
        .out_rt_data(out_rt_data),

        .result_attempt_count(result_attempt_count),
        .result_broken_count(result_broken_count),
        .result_is_last_broken(result_is_last_broken)
    );

    // 控制器 解析指令，发出控制信号
    controller controller_uut( 
        .in_branch(out_branch),
        .in_instruction(in_instruction),

        .out_rs_rena(rs_rena),
        .out_rt_rena(rt_rena),
        .out_rd_wena(out_rd_wena),
        .out_rd_sel(out_rd_sel),
        .out_rd_addr(out_rd_waddr),

        .out_dmem_ena(out_dmem_ena),
        .out_dmem_wena(out_dmem_wena),
        .out_dmem_type(out_dmem_type),

        .out_ext_signed(ext_signed),
        .out_alu_a_sel(out_alu_a_sel),
        .out_alu_b_sel(out_alu_b_sel),
        .out_alu_sel(out_alu_sel),
        .out_pc_sel(out_pc_sel)
    );

    // 判断数据冲突，若有则发stall信号
    stall stall_uut(
        .in_clk(in_clk),
        .in_rst(in_rst),
        .in_rs_addr(rs_addr),
        .in_rt_addr(rt_addr),
        .in_rs_rena(rs_rena),
        .in_rt_rena(rt_rena),
        .in_ex_waddr(in_ex_waddr),
        .in_mem_waddr(in_mem_waddr),
        .in_ex_wena(in_ex_wena),
        .in_mem_wena(in_mem_wena),
        .out_stall(out_stall)
    );

endmodule