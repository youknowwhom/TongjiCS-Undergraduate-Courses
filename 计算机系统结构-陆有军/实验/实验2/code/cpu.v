`timescale 1ns / 1ps

module cpu(
    input           clk,
    input           rst,
    input           ena,
    output [31:0]   pc,
    output [31:0]   instr,
    output [31:0]   reg28
);

    // 各寄存器使能信号
    wire pc_ena;
    wire id_ex_reg_wena;
    wire ex_mem_reg_wena;
    wire mem_wb_reg_wena;

    // 暂停和分支信号
    wire stall;
    wire branch;

    // IF段
    wire [31:0] if_out_npc; 
    wire [31:0] if_out_pc4;


    // ID段
    wire [31:0] id_in_pc4;
    wire [31:0] id_in_instr;

    wire [2:0]  id_out_pc_sel;
    wire [5:0]  id_out_op;
    wire [5:0]  id_out_func;
    wire [31:0] id_out_immed;
    wire [31:0] id_out_shamt;
    wire [31:0] id_out_pc4;
    wire [31:0] id_out_eaddr;
    wire [31:0] id_out_baddr;
    wire [31:0] id_out_jaddr;
    wire [31:0] id_out_raddr;
    wire [31:0] id_out_rs_data;  
    wire [31:0] id_out_rt_data;
    wire [31:0] id_out_hi_data;
    wire [31:0] id_out_lo_data;
    wire [31:0] id_out_cp0_data;
    wire        id_out_alu_a_sel;
    wire [1:0]  id_out_alu_b_sel;
    wire [3:0]  id_out_aluc;
    wire        id_out_mul_ena;
    wire        id_out_div_ena;
    wire        id_out_clz_ena;
    wire        id_out_mul_sign;
    wire        id_out_div_sign;
    wire        id_out_cutter_sign;
    wire        id_out_cutter_addr_sel;
    wire [2:0]  id_out_cutter_sel;
    wire        id_out_dmem_ena;
    wire        id_out_dmem_wena;
    wire [1:0]  id_out_dmem_wsel;
    wire [1:0]  id_out_dmem_rsel;
    wire        id_out_hi_wena;
    wire        id_out_lo_wena;
    wire        id_out_rd_wena;
    wire [1:0]  id_out_hi_sel;
    wire [1:0]  id_out_lo_sel;
    wire [2:0]  id_out_rd_sel;
    wire [4:0]  id_out_rd_waddr;


    // EX模块
    wire [5:0]  ex_in_op;
    wire [5:0]  ex_in_func;
    wire [31:0] ex_in_pc4;
    wire [31:0] ex_in_immed;
    wire [31:0] ex_in_shamt;
    wire [31:0] ex_in_rs_data;
    wire [31:0] ex_in_rt_data;
    wire [31:0] ex_in_hi_data;
    wire [31:0] ex_in_lo_data;
    wire [31:0] ex_in_cp0_data;
    wire        ex_in_alu_a_sel;
    wire [1:0]  ex_in_alu_b_sel;
    wire [3:0]  ex_in_aluc;
    wire        ex_in_mul_ena;
    wire        ex_in_div_ena;
    wire        ex_in_clz_ena;
    wire        ex_in_mul_sign;
    wire        ex_in_div_sign;
    wire        ex_in_cutter_sign;
    wire        ex_in_cutter_addr_sel;
    wire [2:0]  ex_in_cutter_sel;
    wire        ex_in_dmem_ena;
    wire        ex_in_dmem_wena;
    wire [1:0]  ex_in_dmem_wsel;
    wire [1:0]  ex_in_dmem_rsel;
    wire        ex_in_hi_wena;
    wire        ex_in_lo_wena;
    wire        ex_in_rd_wena;
    wire [1:0]  ex_in_hi_sel;
    wire [1:0]  ex_in_lo_sel;
    wire [2:0]  ex_in_rd_sel;
    wire [4:0]  ex_in_rd_waddr;

    wire [31:0] ex_out_pc4;
    wire [31:0] ex_out_rs_data;
    wire [31:0] ex_out_rt_data;
    wire [31:0] ex_out_hi_data;
    wire [31:0] ex_out_lo_data;
    wire [31:0] ex_out_cp0_data;
    wire [31:0] ex_out_alu_data;
    wire [31:0] ex_out_mul_hi;
    wire [31:0] ex_out_mul_lo;
    wire [31:0] ex_out_div_r;
    wire [31:0] ex_out_div_q;
    wire [31:0] ex_out_clz_data;
    wire        ex_out_cutter_sign;
    wire        ex_out_cutter_addr_sel;
    wire [2:0]  ex_out_cutter_sel;
    wire        ex_out_dmem_ena;
    wire        ex_out_dmem_wena;
    wire [1:0]  ex_out_dmem_wsel;
    wire [1:0]  ex_out_dmem_rsel;
    wire        ex_out_hi_wena;
    wire        ex_out_lo_wena;
    wire        ex_out_rd_wena;
    wire [1:0]  ex_out_hi_sel;
    wire [1:0]  ex_out_lo_sel;
    wire [2:0]  ex_out_rd_sel;
    wire [4:0]  ex_out_rd_waddr;


    // MEM模块
    wire [31:0] mem_in_pc4;
    wire [31:0] mem_in_rs_data;
    wire [31:0] mem_in_rt_data;
    wire [31:0] mem_in_hi_data;
    wire [31:0] mem_in_lo_data;
    wire [31:0] mem_in_cp0_data;
    wire [31:0] mem_in_alu_data;
    wire [31:0] mem_in_mul_hi;
    wire [31:0] mem_in_mul_lo;  
    wire [31:0] mem_in_div_r;
    wire [31:0] mem_in_div_q;
    wire [31:0] mem_in_clz_data;
    wire        mem_in_cutter_sign;
    wire        mem_in_cutter_addr_sel;
    wire [2:0]  mem_in_cutter_sel;
    wire        mem_in_dmem_ena;
    wire        mem_in_dmem_wena;
    wire [1:0]  mem_in_dmem_wsel;
    wire [1:0]  mem_in_dmem_rsel;
    wire        mem_in_hi_wena;
    wire        mem_in_lo_wena;
    wire        mem_in_rd_wena;
    wire [1:0]  mem_in_hi_sel;
    wire [1:0]  mem_in_lo_sel;
    wire [2:0]  mem_in_rd_sel;
    wire [4:0]  mem_in_rd_waddr;

    wire [31:0] mem_out_pc4;
    wire [31:0] mem_out_rs_data;
    wire [31:0] mem_out_hi_data;
    wire [31:0] mem_out_lo_data;
    wire [31:0] mem_out_cp0_data;
    wire [31:0] mem_out_alu_data;
    wire [31:0] mem_out_mul_hi;
    wire [31:0] mem_out_mul_lo;
    wire [31:0] mem_out_div_r;
    wire [31:0] mem_out_div_q;
    wire [31:0] mem_out_clz_data;
    wire [31:0] mem_out_dmem_data;
    wire        mem_out_hi_wena;
    wire        mem_out_lo_wena;
    wire        mem_out_rd_wena;       
    wire [1:0]  mem_out_hi_sel;
    wire [1:0]  mem_out_lo_sel;
    wire [2:0]  mem_out_rd_sel;
    wire [4:0]  mem_out_rd_waddr;


    // WB模块
    wire [31:0] wb_in_pc4;
    wire [31:0] wb_in_rs_data;
    wire [31:0] wb_in_hi_data;
    wire [31:0] wb_in_lo_data;
    wire [31:0] wb_in_cp0_data;
    wire [31:0] wb_in_alu_data;
    wire [31:0] wb_in_mul_hi;
    wire [31:0] wb_in_mul_lo;
    wire [31:0] wb_in_div_r;
    wire [31:0] wb_in_div_q;
    wire [31:0] wb_in_clz_data;
    wire [31:0] wb_in_dmem_data;
    wire        wb_in_hi_wena;
    wire        wb_in_lo_wena;
    wire        wb_in_rd_wena;
    wire [1:0]  wb_in_hi_sel;
    wire [1:0]  wb_in_lo_sel;
    wire [2:0]  wb_in_rd_sel;
    wire [4:0]  wb_in_rd_waddr;

    wire        wb_out_hi_wena;
    wire        wb_out_lo_wena;
    wire        wb_out_rd_wena;
    wire [31:0] wb_out_hi_data;
    wire [31:0] wb_out_lo_data;
    wire [31:0] wb_out_rd_data;
    wire [4:0]  wb_out_rd_waddr;


    assign pc_ena           = ena;
    assign id_ex_reg_wena   = ena;
    assign ex_mem_reg_wena  = ena;
    assign mem_wb_reg_wena  = ena;
	
	pc pc_inst(
	    .in_clk(clk),
        .in_rst(rst),
        .in_ena(pc_ena),
        .in_stall(stall),
        .in_pc(if_out_npc),
        .out_pc(pc)
    );

    pipe_if pipe_if_inst(
        .in_pc(pc),
        .in_pc_sel(id_out_pc_sel),
        .in_pc_eaddr(id_out_eaddr),
        .in_pc_baddr(id_out_baddr),
        .in_pc_raddr(id_out_raddr),
        .in_pc_jaddr(id_out_jaddr),
        .out_npc(if_out_npc),
        .out_pc4(if_out_pc4),
        .out_instr(instr)
    );

    pipe_if_id pipe_if_id_inst(
        .in_clk(clk),
        .in_rst(rst),
        .in_stall(stall),
        .in_branch(branch),
        .in_pc4(if_out_pc4),
        .in_instr(instr),
        .out_pc4(id_in_pc4),
        .out_instr(id_in_instr)
    );

    pipe_id pipe_id_inst(
        .in_clk(clk),
        .in_rst(rst),
        .in_pc4(id_in_pc4),
        .in_instr(id_in_instr),
        .in_hi_wena(wb_out_hi_wena),
        .in_lo_wena(wb_out_lo_wena),
        .in_rd_wena(wb_out_rd_wena),
        .in_rd_waddr(wb_out_rd_waddr),
        .in_hi_data(wb_out_hi_data),
        .in_lo_data(wb_out_lo_data),
        .in_rd_data(wb_out_rd_data),
        .in_ex_op(ex_in_op),
        .in_ex_func(ex_in_func),
        .in_ex_pc4(ex_out_pc4),
        .in_ex_alu_data(ex_out_alu_data),
        .in_ex_mul_hi(ex_out_mul_hi),
        .in_ex_mul_lo(ex_out_mul_lo),
        .in_ex_div_r(ex_out_div_r),
        .in_ex_div_q(ex_out_div_q),
        .in_ex_clz_data(ex_out_clz_data),
        .in_ex_hi_data(ex_out_hi_data),
        .in_ex_lo_data(ex_out_lo_data),
        .in_ex_rs_data(ex_out_rs_data),
        .in_ex_hi_wena(ex_out_hi_wena),
        .in_ex_lo_wena(ex_out_lo_wena),
        .in_ex_rd_wena(ex_out_rd_wena),
        .in_ex_hi_sel(ex_out_hi_sel),
        .in_ex_lo_sel(ex_out_lo_sel),
        .in_ex_rd_sel(ex_out_rd_sel),
        .in_ex_rd_waddr(ex_out_rd_waddr),
        .in_mem_pc4(mem_out_pc4),
        .in_mem_alu_data(mem_out_alu_data),
        .in_mem_mul_hi(mem_out_mul_hi),
        .in_mem_mul_lo(mem_out_mul_lo),
        .in_mem_div_q(mem_out_div_r),
        .in_mem_div_r(mem_out_div_q),
        .in_mem_clz_data(mem_out_clz_data),
        .in_mem_lo_data(mem_out_lo_data),
        .in_mem_hi_data(mem_out_hi_data),
        .in_mem_rs_data(mem_out_rs_data),
        .in_mem_dmem_data(mem_out_dmem_data),
        .in_mem_hi_wena(mem_out_hi_wena),
        .in_mem_lo_wena(mem_out_lo_wena),
        .in_mem_rd_wena(mem_out_rd_wena),
        .in_mem_hi_sel(mem_out_hi_sel),
        .in_mem_lo_sel(mem_out_lo_sel),
        .in_mem_rd_sel(mem_out_rd_sel),
        .in_mem_rd_waddr(mem_out_rd_waddr),
        .out_stall(stall),
        .out_branch(branch),
        .out_op(id_out_op),
        .out_func(id_out_func),
        .out_pc_sel(id_out_pc_sel),
        .our_pc4(id_out_pc4),
        .out_immed(id_out_immed),
        .out_shamt(id_out_shamt),
        .out_pc_eaddr(id_out_eaddr),
        .out_pc_baddr(id_out_baddr),
        .out_pc_jaddr(id_out_jaddr),
        .out_pc_raddr(id_out_raddr),
        .out_rs_data(id_out_rs_data),
        .out_rt_data(id_out_rt_data),
        .out_hi_data(id_out_hi_data),
        .out_lo_data(id_out_lo_data),
        .out_cp0_data(id_out_cp0_data),
        .out_alu_a_sel(id_out_alu_a_sel),
        .out_alu_b_sel(id_out_alu_b_sel),
        .out_aluc(id_out_aluc),
        .out_mul_ena(id_out_mul_ena),
        .out_div_ena(id_out_div_ena),
        .out_clz_ena(id_out_clz_ena),
        .out_mul_sign(id_out_mul_sign),
        .out_div_sign(id_out_div_sign),
        .out_hi_wena(id_out_hi_wena),
        .out_lo_wena(id_out_lo_wena),
        .out_rd_wena(id_out_rd_wena),
        .out_cutter_sign(id_out_cutter_sign),
        .out_cutter_addr_sel(id_out_cutter_addr_sel),
        .out_cutter_sel(id_out_cutter_sel),
        .out_dmem_ena(id_out_dmem_ena),
        .out_dmem_wena(id_out_dmem_wena),
        .out_dmem_wsel(id_out_dmem_wsel),
        .out_dmem_rsel(id_out_dmem_rsel),
        .out_hi_sel(id_out_hi_sel),
        .out_lo_sel(id_out_lo_sel),
        .out_rd_sel(id_out_rd_sel),
        .out_rd_waddr(id_out_rd_waddr),
        .out_reg28(reg28)
    );

    pipe_id_ex pipe_id_ex_inst(
        .in_clk(clk),
        .in_rst(rst),
        .in_wena(id_ex_reg_wena),
        .in_stall(stall),
        .in_op(id_out_op),
        .in_func(id_out_func),
        .in_pc4(id_out_pc4),
        .in_immed(id_out_immed),
        .in_shamt(id_out_shamt),
        .in_rs_data(id_out_rs_data),
        .in_rt_data(id_out_rt_data),
        .in_hi_data(id_out_hi_data),
        .in_lo_data(id_out_lo_data),
        .in_cp0_data(id_out_cp0_data),
        .in_alu_a_sel(id_out_alu_a_sel),
        .in_alu_b_sel(id_out_alu_b_sel),
        .in_aluc(id_out_aluc),
        .in_mul_ena(id_out_mul_ena),
        .in_clz_ena(id_out_clz_ena),
        .in_div_ena(id_out_div_ena),
        .in_mul_sign(id_out_mul_sign),
        .in_div_sign(id_out_div_sign),
        .in_cutter_sign(id_out_cutter_sign),
        .in_cutter_addr_sel(id_out_cutter_addr_sel),
        .in_cutter_sel(id_out_cutter_sel),
        .in_dmem_ena(id_out_dmem_ena),
        .in_dmem_wena(id_out_dmem_wena),
        .in_dmem_wsel(id_out_dmem_wsel),
        .in_dmem_rsel(id_out_dmem_rsel),
        .in_hi_wena(id_out_hi_wena),
        .in_lo_wena(id_out_lo_wena),
        .in_rd_wena(id_out_rd_wena),
        .in_hi_sel(id_out_hi_sel),
        .in_lo_sel(id_out_lo_sel),
        .in_rd_sel(id_out_rd_sel),
        .in_rd_waddr(id_out_rd_waddr),
        .out_op(ex_in_op),
        .out_func(ex_in_func),
        .out_pc4(ex_in_pc4),
        .out_immed(ex_in_immed),
        .out_shamt(ex_in_shamt),
        .out_rs_data(ex_in_rs_data),
        .out_rt_data(ex_in_rt_data),
        .out_hi_data(ex_in_hi_data),
        .out_lo_data(ex_in_lo_data),
        .out_cp0_data(ex_in_cp0_data),
        .out_alu_a_sel(ex_in_alu_a_sel),
        .out_alu_b_sel(ex_in_alu_b_sel),
        .out_aluc(ex_in_aluc),
        .out_clz_ena(ex_in_clz_ena),
        .out_mul_ena(ex_in_mul_ena),
        .out_div_ena(ex_in_div_ena),
        .out_mul_sign(ex_in_mul_sign),
        .out_div_sign(ex_in_div_sign),
        .out_cutter_sign(ex_in_cutter_sign),
        .out_cutter_addr_sel(ex_in_cutter_addr_sel),
        .out_cutter_sel(ex_in_cutter_sel),
        .out_dmem_ena(ex_in_dmem_ena),
        .out_dmem_wena(ex_in_dmem_wena),
        .out_dmem_wsel(ex_in_dmem_wsel),
        .out_dmem_rsel(ex_in_dmem_rsel),
        .out_rd_wena(ex_in_rd_wena),
        .out_hi_wena(ex_in_hi_wena),
        .out_lo_wena(ex_in_lo_wena),
        .out_hi_sel(ex_in_hi_sel),
        .out_lo_sel(ex_in_lo_sel),
        .out_rd_sel(ex_in_rd_sel),
        .out_rd_waddr(ex_in_rd_waddr)
    );

    pipe_ex pipe_ex_inst(
        .in_rst(rst),
        .in_pc4(ex_in_pc4),
        .in_immed(ex_in_immed),
        .in_shamt(ex_in_shamt),
        .in_rs_data(ex_in_rs_data),
        .in_rt_data(ex_in_rt_data),
        .in_hi_data(ex_in_hi_data),
        .in_lo_data(ex_in_lo_data),
        .in_cp0_data(ex_in_cp0_data),
        .in_alu_a_sel(ex_in_alu_a_sel),
        .in_alu_b_sel(ex_in_alu_b_sel),
        .in_aluc(ex_in_aluc),
        .in_mul_ena(ex_in_mul_ena),
        .in_div_ena(ex_in_div_ena),
        .in_clz_ena(ex_in_clz_ena),
        .in_mul_sign(ex_in_mul_sign),
        .in_div_sign(ex_in_div_sign),
        .in_cutter_sign(ex_in_cutter_sign),
        .in_cutter_addr_sel(ex_in_cutter_addr_sel),
        .in_cutter_sel(ex_in_cutter_sel),
        .in_dmem_ena(ex_in_dmem_ena),
        .in_dmem_wena(ex_in_dmem_wena),
        .in_dmem_wsel(ex_in_dmem_wsel),
        .in_dmem_rsel(ex_in_dmem_rsel),
        .in_rd_wena(ex_in_rd_wena),
        .in_hi_wena(ex_in_hi_wena),
        .in_lo_wena(ex_in_lo_wena),
        .in_hi_sel(ex_in_hi_sel),
        .in_lo_sel(ex_in_lo_sel),
        .in_rd_sel(ex_in_rd_sel),
        .in_rd_waddr(ex_in_rd_waddr),
        .out_pc4(ex_out_pc4),
        .out_mul_hi(ex_out_mul_hi),
        .out_mul_lo(ex_out_mul_lo),
        .out_div_r(ex_out_div_r),
        .out_div_q(ex_out_div_q),
        .out_rs_data(ex_out_rs_data),
        .out_rt_data(ex_out_rt_data),
        .out_hi_data(ex_out_hi_data),
        .out_lo_data(ex_out_lo_data),
        .out_cp0_data(ex_out_cp0_data),
        .out_clz_data(ex_out_clz_data),
        .out_alu_data(ex_out_alu_data),
        .out_cutter_sign(ex_out_cutter_sign),
        .out_cutter_addr_sel(ex_out_cutter_addr_sel),
        .out_cutter_sel(ex_out_cutter_sel),
        .out_dmem_ena(ex_out_dmem_ena),
        .out_dmem_wena(ex_out_dmem_wena),
        .out_dmem_wsel(ex_out_dmem_wsel),
        .out_dmem_rsel(ex_out_dmem_rsel),
        .out_hi_wena(ex_out_hi_wena),
        .out_lo_wena(ex_out_lo_wena),
        .out_rd_wena(ex_out_rd_wena),
        .out_hi_sel(ex_out_hi_sel),
        .out_lo_sel(ex_out_lo_sel),
        .out_rd_sel(ex_out_rd_sel),
        .out_rd_waddr(ex_out_rd_waddr)
    );


    pipe_ex_mem pipe_ex_mem_inst(
        .in_clk(clk),
        .in_rst(rst),
        .in_wena(ex_mem_reg_wena),
        .in_pc4(ex_out_pc4),
        .in_rs_data(ex_out_rs_data),
        .in_rt_data(ex_out_rt_data),
        .in_hi_data(ex_out_hi_data),
        .in_lo_data(ex_out_lo_data),
        .in_cp0_data(ex_out_cp0_data),
        .in_alu_data(ex_out_alu_data),
        .in_mul_hi(ex_out_mul_hi),
        .in_mul_lo(ex_out_mul_lo),
        .in_div_r(ex_out_div_r),
        .in_div_q(ex_out_div_q),
        .in_clz_data(ex_out_clz_data),
        .in_cutter_sign(ex_out_cutter_sign),
        .in_cutter_sel(ex_out_cutter_sel),
        .in_cutter_addr_sel(ex_out_cutter_addr_sel),
        .in_dmem_ena(ex_out_dmem_ena),
        .in_dmem_wena(ex_out_dmem_wena),
        .in_dmem_wsel(ex_out_dmem_wsel),
        .in_dmem_rsel(ex_out_dmem_rsel),
        .in_hi_wena(ex_out_hi_wena),
        .in_lo_wena(ex_out_lo_wena),
        .in_rd_wena(ex_out_rd_wena),
        .in_hi_sel(ex_out_hi_sel),
        .in_lo_sel(ex_out_lo_sel),
        .in_rd_sel(ex_out_rd_sel),
        .in_rd_waddr(ex_out_rd_waddr),
        .out_pc4(mem_in_pc4),
        .out_rs_data(mem_in_rs_data),
        .out_rt_data(mem_in_rt_data),
        .out_hi_data(mem_in_hi_data),
        .out_lo_data(mem_in_lo_data),
        .out_cp0_data(mem_in_cp0_data),
        .out_alu_data(mem_in_alu_data),
        .out_mul_hi(mem_in_mul_hi),
        .out_mul_lo(mem_in_mul_lo),
        .out_div_r(mem_in_div_r),
        .out_div_q(mem_in_div_q),
        .out_clz_data(mem_in_clz_data),
        .out_cutter_sign(mem_in_cutter_sign),
        .out_cutter_addr_sel(mem_in_cutter_addr_sel),
        .out_cutter_sel(mem_in_cutter_sel),
        .out_dmem_ena(mem_in_dmem_ena),
        .out_dmem_wena(mem_in_dmem_wena),
        .out_dmem_wsel(mem_in_dmem_wsel),
        .out_dmem_rsel(mem_in_dmem_rsel),
        .out_rd_wena(mem_in_rd_wena),
        .out_hi_wena(mem_in_hi_wena),
        .out_lo_wena(mem_in_lo_wena),
        .out_hi_sel(mem_in_hi_sel),
        .out_lo_sel(mem_in_lo_sel),
        .out_rd_sel(mem_in_rd_sel),
        .out_rd_waddr(mem_in_rd_waddr)
    );

    pipe_mem pipe_mem_inst(
        .in_clk(clk),
        .in_pc4(mem_in_pc4),
        .in_rs_data(mem_in_rs_data),
        .in_rt_data(mem_in_rt_data),
        .in_hi_data(mem_in_hi_data),
        .in_lo_data(mem_in_lo_data),
        .in_cp0_data(mem_in_cp0_data),
        .in_alu_data(mem_in_alu_data),
        .in_mul_hi(mem_in_mul_hi),
        .in_mul_lo(mem_in_mul_lo),
        .in_div_r(mem_in_div_r),
        .in_div_q(mem_in_div_q),
        .in_clz_data(mem_in_clz_data),
        .in_cutter_sign(mem_in_cutter_sign),
        .in_cutter_addr_sel(mem_in_cutter_addr_sel),
        .in_cutter_sel(mem_in_cutter_sel),
        .in_dmem_wsel(mem_in_dmem_wsel),
        .in_dmem_rsel(mem_in_dmem_rsel),
        .in_dmem_ena(mem_in_dmem_ena),
        .in_dmem_wena(mem_in_dmem_wena),
        .in_hi_wena(mem_in_hi_wena),
        .in_lo_wena(mem_in_lo_wena),
        .in_rd_wena(mem_in_rd_wena),
        .in_hi_sel(mem_in_hi_sel),
        .in_lo_sel(mem_in_lo_sel),
        .in_rd_sel(mem_in_rd_sel),
        .in_rd_waddr(mem_in_rd_waddr),
        .our_pc4(mem_out_pc4),
        .out_rs_data(mem_out_rs_data),
        .out_hi_data(mem_out_hi_data),
        .out_lo_data(mem_out_lo_data),
        .out_cp0_data(mem_out_cp0_data),
        .out_alu_data(mem_out_alu_data),
        .out_mul_hi(mem_out_mul_hi),
        .out_mul_lo(mem_out_mul_lo),
        .out_div_r(mem_out_div_r),
        .out_div_q(mem_out_div_q),
        .out_clz_data(mem_out_clz_data),
        .out_dmem_data(mem_out_dmem_data),
        .out_hi_wena(mem_out_hi_wena),
        .out_lo_wena(mem_out_lo_wena),
        .out_rd_wena(mem_out_rd_wena),
        .out_hi_sel(mem_out_hi_sel),
        .out_lo_sel(mem_out_lo_sel),
        .out_rd_sel(mem_out_rd_sel),
        .out_rd_waddr(mem_out_rd_waddr)
    );

    pipe_mem_wb pipe_mem_wb_inst(
        .in_clk(clk),
        .in_rst(rst),
        .in_wena(mem_wb_reg_wena),
        .in_pc4(mem_out_pc4),
        .in_rs_data(mem_out_rs_data),
        .in_hi_data(mem_out_hi_data),
        .in_lo_data(mem_out_lo_data),
        .in_cp0_data(mem_out_cp0_data),
        .in_alu_data(mem_out_alu_data),
        .in_mul_hi(mem_out_mul_hi),
        .in_mul_lo(mem_out_mul_lo),
        .in_div_r(mem_out_div_r),
        .in_div_q(mem_out_div_q),
        .in_clz_data(mem_out_clz_data),
        .in_dmem_data(mem_out_dmem_data),
        .in_hi_wena(mem_out_hi_wena),
        .in_lo_wena(mem_out_lo_wena),
        .in_rd_wena(mem_out_rd_wena),
        .in_hi_sel(mem_out_hi_sel),
        .in_lo_sel(mem_out_lo_sel),
        .in_rd_sel(mem_out_rd_sel),
        .in_rd_waddr(mem_out_rd_waddr),
        .out_pc4(wb_in_pc4),
        .out_rs_data(wb_in_rs_data),
        .out_hi_data(wb_in_hi_data),
        .out_lo_data(wb_in_lo_data),
        .out_cp0_data(wb_in_cp0_data),
        .out_alu_data(wb_in_alu_data),
        .out_mul_hi(wb_in_mul_hi),
        .out_mul_lo(wb_in_mul_lo),
        .out_div_r(wb_in_div_r),
        .out_div_q(wb_in_div_q),
        .out_clz_data(wb_in_clz_data),
        .out_dmem_data(wb_in_dmem_data),
        .out_hi_wena(wb_in_hi_wena),
        .out_lo_wena(wb_in_lo_wena),
        .out_rd_wena(wb_in_rd_wena),
        .out_hi_sel(wb_in_hi_sel),
        .out_lo_sel(wb_in_lo_sel),
        .out_rd_sel(wb_in_rd_sel),
        .out_rd_waddr(wb_in_rd_waddr)
    );

    pipe_wb pipe_wb_inst(
        .in_pc4(wb_in_pc4),
        .in_rs_data(wb_in_rs_data),
        .in_hi_data(wb_in_hi_data),
        .in_lo_data(wb_in_lo_data),
        .in_cp0_data(wb_in_cp0_data),
        .in_alu_data(wb_in_alu_data),
        .in_mul_hi(wb_in_mul_hi),
        .in_mul_lo(wb_in_mul_lo),
        .in_div_r(wb_in_div_q),
        .in_div_q(wb_in_div_q),
        .in_clz_data(wb_in_clz_data),
        .in_dmem_data(wb_in_dmem_data),
        .in_hi_wena(wb_in_hi_wena),
        .in_lo_wena(wb_in_lo_wena),
        .in_rd_wena(wb_in_rd_wena),
        .in_hi_sel(wb_in_hi_sel),
        .in_lo_sel(wb_in_lo_sel),
        .in_rd_sel(wb_in_rd_sel),
        .in_rd_waddr(wb_in_rd_waddr),
        .out_hi_wena(wb_out_hi_wena),
        .out_lo_wena(wb_out_lo_wena),
        .out_rd_wena(wb_out_rd_wena),
        .out_rd_waddr(wb_out_rd_waddr),
        .out_hi_data(wb_out_hi_data),
        .out_lo_data(wb_out_lo_data),
        .out_rd_data(wb_out_rd_data)
    );

endmodule