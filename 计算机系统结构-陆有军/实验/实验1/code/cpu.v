`timescale 1ns / 1ns

module cpu(
    input           in_clk,
    input           in_rst,
    
    input   [31:0]  init_floors,
    input   [31:0]  init_resistance,

    output  [31:0]  out_pc,
    output  [31:0]  out_instruction,

    output  [31:0]  result_attempt_count,
    output  [31:0]  result_broken_count,
    output          result_is_last_broken
    );


    /* IF¶Î */
    wire [31:0] if_out_pc;
    wire [31:0] if_out_npc;
    wire [31:0] if_out_instruction;

    /* ID¶Î */
    wire [31:0] id_in_npc;
    wire [31:0] id_in_instruction;
	wire [4:0]  id_in_ex_waddr;
	wire [4:0]  id_in_mem_waddr;
    wire        id_in_wena;
    wire        id_in_ex_wena;
    wire        id_in_mem_wena;

    wire        id_out_dmem_ena;
    wire        id_out_dmem_wena;
    wire [1:0]  id_out_dmem_type;
    wire [31:0] id_out_rs_data;
    wire [31:0] id_out_rt_data;
    wire [4:0]  id_out_rd_waddr;
    wire        id_out_rd_sel;
    wire        id_out_rd_wena;
    wire [31:0] id_out_immed;
    wire [31:0] id_out_shamt;
    wire [1:0]  id_out_pc_sel;
    wire [31:0] id_out_pc_baddr;
    wire [31:0] id_out_pc_jaddr;
    wire        id_out_alu_a_sel;
    wire        id_out_alu_b_sel;
    wire [3:0]  id_out_alu_sel;
    wire        id_out_stall;
    wire        id_out_branch;

    /* EX¶Î */
    wire        ex_in_dmem_ena;
    wire        ex_in_dmem_wena;
    wire [1:0]  ex_in_dmem_type;
    wire [31:0] ex_in_rs_data;
    wire [31:0] ex_in_rt_data;
    wire [4:0]  ex_in_rd_waddr;
    wire        ex_in_rd_wena;
    wire        ex_in_rd_sel;
    wire [31:0] ex_in_immed;
    wire [31:0] ex_in_shamt;
    wire        ex_in_alu_a_sel;
    wire        ex_in_alu_b_sel;
    wire [3:0]  ex_in_alu_sel;
    wire        ex_in_stall;

    wire        ex_out_dmem_ena;
    wire        ex_out_dmem_wena;
    wire [1:0]  ex_out_dmem_type;
    wire [31:0] ex_out_rs_data;
    wire [31:0] ex_out_rt_data;
    wire [4:0]  ex_out_rd_waddr;
    wire        ex_out_rd_sel;
    wire        ex_out_rd_wena;
    wire [31:0] ex_out_alu_result;

    /* MEM¶Î */
    wire        mem_in_dmem_ena;
    wire        mem_in_dmem_wena;
    wire [1:0]  mem_in_dmem_type;
    wire [31:0] mem_in_rs_data;
    wire [31:0] mem_in_rt_data;
    wire [4:0]  mem_in_rd_waddr;
    wire        mem_in_rd_sel;
    wire        mem_in_rd_wena;
    wire [31:0] mem_in_alu_result;

    wire [4:0]  mem_out_rd_waddr;
    wire        mem_out_rd_sel;
    wire        mem_out_rd_wena;
    wire [31:0] mem_out_alu_result;
    wire [31:0] mem_out_dmem_data;

    /* WB¶Î */
    wire [4:0]  wb_in_rd_waddr;
    wire        wb_in_rd_sel;
    wire        wb_in_rd_wena;
    wire [31:0] wb_in_alu_result;
    wire [31:0] wb_in_dmem_data;

    wire [4:0]  wb_out_rd_waddr;
    wire        wb_out_rd_wena;
    wire [31:0] wb_out_rd_data;

    assign out_pc           = if_out_pc;
    assign out_instruction  = if_out_instruction;

    pipe_if pipe_if_uut(
        .in_clk(in_clk),
        .in_rst(in_rst),
        .in_stall(id_out_stall),

        .in_pc_baddr(id_out_pc_baddr),
        .in_pc_jaddr(id_out_pc_jaddr),
        .in_pc_sel(id_out_pc_sel),

        .out_pc(if_out_pc),
        .out_npc(if_out_npc),
        .out_instruction(if_out_instruction)
    );

    pipe_if_id pipe_if_id_uut(
        .in_clk(in_clk),
        .in_rst(in_rst),

        .in_npc(if_out_npc),
        .in_instruction(if_out_instruction),

        .in_stall(id_out_stall),
        .in_branch(id_out_branch),

        .out_npc(id_in_npc),
        .out_instruction(id_in_instruction)
    );

    pipe_id pipe_id_uut(
        .in_clk(in_clk),
        .in_rst(in_rst),

        .in_npc(id_in_npc),
        .in_instruction(id_in_instruction),

        .in_ex_waddr(ex_out_rd_waddr),
	    .in_mem_waddr(mem_out_rd_waddr),
        .in_ex_wena(ex_out_rd_wena),
        .in_mem_wena(mem_out_rd_wena),

        .in_wb_reg_addr(wb_out_rd_waddr),
        .in_wb_reg_data(wb_out_rd_data),
        .in_wb_reg_ena(wb_out_rd_wena),

        .init_floors(init_floors),
        .init_resistance(init_resistance),

        .out_rs_data(id_out_rs_data),
        .out_rt_data(id_out_rt_data),
        .out_rd_waddr(id_out_rd_waddr),
        .out_rd_wena(id_out_rd_wena),
        .out_rd_sel(id_out_rd_sel),
        .out_immed(id_out_immed),
        .out_shamt(id_out_shamt),

        .out_dmem_ena(id_out_dmem_ena),
        .out_dmem_wena(id_out_dmem_wena),
        .out_dmem_type(id_out_dmem_type),

        .out_alu_a_sel(id_out_alu_a_sel),
        .out_alu_b_sel(id_out_alu_b_sel),
        .out_alu_sel(id_out_alu_sel),

        .out_pc_sel(id_out_pc_sel),
        .out_pc_baddr(id_out_pc_baddr),
        .out_pc_jaddr(id_out_pc_jaddr),

        .out_stall(id_out_stall),
        .out_branch(id_out_branch),

        .result_attempt_count(result_attempt_count),
        .result_broken_count(result_broken_count),
        .result_is_last_broken(result_is_last_broken)
    );

    pipe_id_ex pipe_id_ex_uut(
        .in_clk(in_clk),
        .in_rst(in_rst),

        .in_dmem_ena(id_out_dmem_ena),
        .in_dmem_wena(id_out_dmem_wena),
        .in_dmem_type(id_out_dmem_type),

        .in_rs_data(id_out_rs_data),
        .in_rt_data(id_out_rt_data),

        .in_rd_waddr(id_out_rd_waddr),
        .in_rd_sel(id_out_rd_sel),
        .in_rd_wena(id_out_rd_wena),

        .in_alu_a_sel(id_out_alu_a_sel),
        .in_alu_b_sel(id_out_alu_b_sel),
        .in_alu_sel(id_out_alu_sel),

        .in_immed(id_out_immed),
        .in_shamt(id_out_shamt),

        .in_stall(id_out_stall),

        .out_dmem_ena(ex_in_dmem_ena),
        .out_dmem_wena(ex_in_dmem_wena),
        .out_dmem_type(ex_in_dmem_type),

        .out_rs_data(ex_in_rs_data),
        .out_rt_data(ex_in_rt_data),
        .out_rd_waddr(ex_in_rd_waddr),
        .out_rd_sel(ex_in_rd_sel),
        .out_rd_wena(ex_in_rd_wena),

        .out_alu_a_sel(ex_in_alu_a_sel),
        .out_alu_b_sel(ex_in_alu_b_sel),
        .out_alu_sel(ex_in_alu_sel),

        .out_immed(ex_in_immed),
        .out_shamt(ex_in_shamt)
    );

    pipe_ex pipe_ex_uut(
        .in_rst(in_rst),

        .in_dmem_ena(ex_in_dmem_ena),
        .in_dmem_wena(ex_in_dmem_wena),
        .in_dmem_type(ex_in_dmem_type),

        .in_rs_data(ex_in_rs_data),
        .in_rt_data(ex_in_rt_data),
        .in_rd_waddr(ex_in_rd_waddr),
        .in_rd_sel(ex_in_rd_sel),
        .in_rd_wena(ex_in_rd_wena),

        .in_immed(ex_in_immed),
        .in_shamt(ex_in_shamt),

        .in_alu_a_sel(ex_in_alu_a_sel),
        .in_alu_b_sel(ex_in_alu_b_sel),
        .in_alu_sel(ex_in_alu_sel),
        
        .out_dmem_ena(ex_out_dmem_ena),
        .out_dmem_wena(ex_out_dmem_wena),
        .out_dmem_type(ex_out_dmem_type),

        .out_rs_data(ex_out_rs_data),
        .out_rt_data(ex_out_rt_data),
        .out_rd_waddr(ex_out_rd_waddr),
        .out_rd_sel(ex_out_rd_sel),
        .out_rd_wena(ex_out_rd_wena),

        .out_alu_result(ex_out_alu_result)
    );

    pipe_ex_mem pipe_ex_mem_uut(
        .in_clk(in_clk),
        .in_rst(in_rst),

        .in_dmem_ena(ex_out_dmem_ena),
        .in_dmem_wena(ex_out_dmem_wena),
        .in_dmem_type(ex_out_dmem_type),

        .in_rs_data(ex_out_rs_data),
        .in_rt_data(ex_out_rt_data),
        .in_rd_waddr(ex_out_rd_waddr),
        .in_rd_sel(ex_out_rd_sel),
        .in_rd_wena(ex_out_rd_wena),
        
        .in_alu_result(ex_out_alu_result),

        .out_dmem_ena(mem_in_dmem_ena),
        .out_dmem_wena(mem_in_dmem_wena),
        .out_dmem_type(mem_in_dmem_type),

        .out_rs_data(mem_in_rs_data),
        .out_rt_data(mem_in_rt_data),
        .out_rd_waddr(mem_in_rd_waddr),
        .out_rd_sel(mem_in_rd_sel),
        .out_rd_wena(mem_in_rd_wena),

        .out_alu_result(mem_in_alu_result)
    );

    pipe_mem pipe_mem_uut(
        .in_clk(in_clk),

        .in_dmem_ena(mem_in_dmem_ena),
        .in_dmem_wena(mem_in_dmem_wena),
        .in_dmem_type(mem_in_dmem_type),

        .in_rs_data(mem_in_rs_data),
        .in_rt_data(mem_in_rt_data),
        .in_rd_waddr(mem_in_rd_waddr),
        .in_rd_sel(mem_in_rd_sel),
        .in_rd_wena(mem_in_rd_wena),

        .in_alu_result(mem_in_alu_result),

        .out_rd_waddr(mem_out_rd_waddr),
        .out_rd_wena(mem_out_rd_wena),
        .out_rd_sel(mem_out_rd_sel),

        .out_alu_result(mem_out_alu_result),

        .out_dmem_data(mem_out_dmem_data)
    );

    pipe_mem_wb pipe_mem_wb_uut(
        .in_clk(in_clk),
        .in_rst(in_rst),

        .in_rd_waddr(mem_out_rd_waddr),
        .in_rd_sel(mem_out_rd_sel),
        .in_rd_wena(mem_out_rd_wena),

        .in_alu_result(mem_out_alu_result),
        .in_dmem_data(mem_out_dmem_data),

        .out_rd_waddr(wb_in_rd_waddr),
        .out_rd_sel(wb_in_rd_sel),
        .out_rd_wena(wb_in_rd_wena),

        .out_alu_result(wb_in_alu_result),
        .out_dmem_data(wb_in_dmem_data)
    );

    pipe_wb pipe_wb_uut(
        .in_rd_waddr(wb_in_rd_waddr),
        .in_rd_sel(wb_in_rd_sel),
        .in_rd_wena(wb_in_rd_wena),

        .in_alu_result(wb_in_alu_result),
        .in_dmem_data(wb_in_dmem_data),

        .out_rd_waddr(wb_out_rd_waddr),
        .out_rd_wdata(wb_out_rd_data),
        .out_rd_wena(wb_out_rd_wena)
    );

endmodule