`timescale 1ns / 1ps

module pipe_if(
    input   [31:0]  in_pc,
    input   [2:0]   in_pc_sel,
    input   [31:0]  in_pc_eaddr,
    input   [31:0]  in_pc_baddr,
    input   [31:0]  in_pc_raddr,
    input   [31:0]  in_pc_jaddr,
    output  [31:0]  out_npc,
    output  [31:0]  out_pc4,
    output  [31:0]  out_instr 
    );

    assign out_pc4 = in_pc + 32'd4;

	imem imem_inst(in_pc[12:2], out_instr);
    mux8_32 mux_npc(in_pc_jaddr, in_pc_raddr, out_pc4, 32'h00400004, 
                    in_pc_baddr, in_pc_eaddr, 32'bz, 32'bz, in_pc_sel, out_npc);

endmodule

module pipe_if_id(
    input               in_clk,
    input               in_rst,
    input               in_stall,
    input               in_branch,
    input [31:0]        in_pc4,
    input [31:0]        in_instr,
    output reg [31:0]   out_pc4,
    output reg [31:0]   out_instr 
    );

    always @(posedge in_clk or posedge in_rst)
    begin
		if(in_rst) 
        begin
		    out_pc4   <= 32'b0;
		    out_instr <= 32'b0;       
		end 
        else if(in_branch)
        begin
            out_pc4   <= 32'b0;
            out_instr <= 32'b0;
        end 
        else if(~in_stall) 
        begin
		    out_pc4   <= in_pc4;
		    out_instr <= in_instr;
		end
	end
	
endmodule


module pipe_id(
	input           in_clk,
    input           in_rst,
    input [31:0]    in_pc4,
    input [31:0]    in_instr,
    input           in_hi_wena,
    input           in_lo_wena,
    input           in_rd_wena,
    input [4:0]     in_rd_waddr,
    input [31:0]    in_hi_data,
    input [31:0]    in_lo_data,
    input [31:0]    in_rd_data,

    input [5:0]     in_ex_op,
    input [5:0]     in_ex_func,
    input [31:0]    in_ex_pc4,
    input [31:0]    in_ex_alu_data,
    input [31:0]    in_ex_mul_hi,
    input [31:0]    in_ex_mul_lo,
    input [31:0]    in_ex_div_r,
    input [31:0]    in_ex_div_q,
    input [31:0]    in_ex_clz_data,
    input [31:0]    in_ex_hi_data,
    input [31:0]    in_ex_lo_data,
    input [31:0]    in_ex_rs_data,
    input           in_ex_hi_wena,
    input           in_ex_lo_wena,
    input           in_ex_rd_wena,
    input [1:0]     in_ex_hi_sel,
    input [1:0]     in_ex_lo_sel,
    input [2:0]     in_ex_rd_sel,
    input [4:0]     in_ex_rd_waddr,

    input [31:0]    in_mem_pc4,
    input [31:0]    in_mem_alu_data,
    input [31:0]    in_mem_mul_hi,
    input [31:0]    in_mem_mul_lo,
    input [31:0]    in_mem_div_q,
    input [31:0]    in_mem_div_r,
    input [31:0]    in_mem_clz_data,
    input [31:0]    in_mem_lo_data,
    input [31:0]    in_mem_hi_data,
    input [31:0]    in_mem_rs_data,
    input [31:0]    in_mem_dmem_data,
    input           in_mem_hi_wena,
    input           in_mem_lo_wena,
    input           in_mem_rd_wena,
    input [1:0]     in_mem_hi_sel,
    input [1:0]     in_mem_lo_sel,
    input [2:0]     in_mem_rd_sel,
    input [4:0]     in_mem_rd_waddr,


    output          out_stall,
    output          out_branch,
    output [5:0]    out_op,
    output [5:0]    out_func,
    output [2:0]    out_pc_sel,
    output [31:0]   our_pc4,
    output [31:0]   out_immed,
    output [31:0]   out_shamt,
    output [31:0]   out_pc_eaddr,
    output [31:0]   out_pc_baddr,
    output [31:0]   out_pc_jaddr,
    output [31:0]   out_pc_raddr,
    output [31:0]   out_rs_data,
    output [31:0]   out_rt_data,
    output [31:0]   out_hi_data,
    output [31:0]   out_lo_data,
    output [31:0]   out_cp0_data,
    output          out_alu_a_sel,
    output [1:0]    out_alu_b_sel,
    output [3:0]    out_aluc,
    output          out_mul_ena,
    output          out_div_ena,
    output          out_clz_ena,
    output          out_mul_sign,
    output          out_div_sign,
    output          out_hi_wena,
    output          out_lo_wena,
    output          out_rd_wena,
    output          out_cutter_sign,
    output          out_cutter_addr_sel,
    output [2:0]    out_cutter_sel,
    output          out_dmem_ena,
    output          out_dmem_wena,
    output [1:0]    out_dmem_wsel,
    output [1:0]    out_dmem_rsel,
    output [1:0]    out_hi_sel,
    output [1:0]    out_lo_sel,
    output [2:0]    out_rd_sel,
    output [4:0]    out_rd_waddr,
    output [31:0]   out_reg28
    );

    wire [5:0] op   = in_instr[31:26];
    wire [5:0] func = in_instr[5:0];
    wire [4:0] rsc  = in_instr[25:21];
    wire [4:0] rtc  = in_instr[20:16];
    wire rs_rena;
    wire rt_rena;

    wire immed_sign;
    wire mfc0;
    wire mtc0;
    wire eret;
    
    wire [31:0] ex_df_hi_data;
    wire [31:0] ex_df_lo_data;
    wire [31:0] ex_df_rd_data;
    wire [31:0] mem_df_hi_data;
    wire [31:0] mem_df_lo_data;
    wire [31:0] mem_df_rd_data;
    
    wire        ext5_sel;
    wire [4:0]  ext5_data;
    
    wire forward;
    wire is_rs, is_rt;
    wire [31:0] hi_df_data;
    wire [31:0] lo_df_data;
    wire [31:0] rs_df_data;
    wire [31:0] rt_df_data;
    wire [31:0] hi_data;
    wire [31:0] lo_data;
    wire [31:0] rs_data;
    wire [31:0] rt_data;

    wire        cp0_exec;
    wire [4:0]  cp0_addr;
    wire [4:0]  cp0_cause;
    wire [31:0] cp0_status;

    assign out_immed    = { { 16{ immed_sign & in_instr[15] } }, in_instr[15:0] };
    assign out_shamt    = { 27'b0, ext5_data };

    assign out_pc_baddr = in_pc4 + { { { 14{ in_instr[15] } }, in_instr[15:0], 2'b00 } };
    assign out_pc_jaddr = { in_pc4[31:28], in_instr[25:0], 2'b00 };
    assign out_pc_raddr = out_rs_data;

    assign out_rs_data  = (forward && is_rs) ? rs_df_data : rs_data;
    assign out_rt_data  = (forward && is_rt) ? rt_df_data : rt_data;
    assign out_hi_data  = forward ? hi_df_data : hi_data;
    assign out_lo_data  = forward ? lo_df_data : lo_data;

    assign our_pc4      = in_pc4;
    assign out_op       = op;
    assign out_func     = func;

    mux2_5 mux_extend5(in_instr[10:6], out_rs_data[4:0], ext5_sel, ext5_data);

    mux4_32 mux_ex_df_hi(in_ex_div_r, in_ex_mul_hi, in_ex_rs_data, 32'hz, in_ex_hi_sel, ex_df_hi_data);
    mux4_32 mux_ex_df_lo(in_ex_div_q, in_ex_mul_lo, in_ex_rs_data, 32'hz, in_ex_lo_sel, ex_df_lo_data);
    mux8_32 mux_ex_df_rd(in_ex_lo_data, in_ex_pc4, in_ex_clz_data, 32'hz, 32'hz, in_ex_alu_data, in_ex_hi_data, in_ex_mul_lo, in_ex_rd_sel, ex_df_rd_data);

    mux4_32 mux_mem_df_hi(in_mem_div_q, in_mem_mul_hi, in_mem_rs_data, 32'hz, in_mem_hi_sel, mem_df_hi_data);
    mux4_32 mux_mem_df_lo(in_mem_div_r, in_mem_mul_lo, in_mem_rs_data, 32'hz, in_mem_lo_sel, mem_df_lo_data);
    mux8_32 mux_mem_df_rd(in_mem_lo_data, in_mem_pc4, in_mem_clz_data, 32'hz, in_mem_dmem_data, in_mem_alu_data, in_mem_hi_data, in_mem_mul_lo, in_mem_rd_sel, mem_df_rd_data);

    regfile regfile_inst(in_clk, in_rst, in_rd_wena, rsc, rtc, rs_rena, rt_rena, in_rd_waddr, in_rd_data, rs_data, rt_data, out_reg28);
    cp0 cp0_inst(in_clk, in_rst, mfc0, mtc0, in_pc4 - 32'd4, cp0_addr, out_rt_data, cp0_exec, eret, cp0_cause, out_cp0_data, cp0_status, out_pc_eaddr);

    register hi_inst(in_clk, in_rst, in_hi_wena, in_hi_data, hi_data);
    register lo_inst(in_clk, in_rst, in_lo_wena, in_lo_data, lo_data);

    forwarding forwarding_inst(
        .in_clk(in_clk),
        .in_rst(in_rst),
        .in_op(op),
        .in_func(func),
        .in_rs_rena(rs_rena),
        .in_rt_rena(rt_rena),
        .in_rsc(rsc),
        .in_rtc(rtc),
        .in_exe_op(in_ex_op),
        .in_exe_func(in_ex_func),
        .in_exe_hi_data(ex_df_hi_data),
        .in_exe_lo_data(ex_df_lo_data),
        .in_exe_rd_data(ex_df_rd_data),
        .in_exe_hi_wena(in_ex_hi_wena),
        .in_exe_lo_wena(in_ex_lo_wena),
        .in_exe_rd_wena(in_ex_rd_wena),
        .in_exe_rdc(in_ex_rd_waddr),
        .in_mem_hi_data(mem_df_hi_data),
        .in_mem_lo_data(mem_df_lo_data),
        .in_mem_rd_data(mem_df_rd_data),
        .in_mem_hi_wena(in_mem_hi_wena),
        .in_mem_lo_wena(in_mem_lo_wena),
        .in_mem_rd_wena(in_mem_rd_wena),
        .in_mem_rdc(in_mem_rd_waddr),
        .out_stall(out_stall),
        .out_forwarding(forward),
        .out_is_rs(is_rs),
        .out_is_rt(is_rt),
        .out_rs_data(rs_df_data),
        .out_rt_data(rt_df_data),
        .out_hi_data(hi_df_data),
        .out_lo_data(lo_df_data)
        );
	
    compare compare_inst(in_clk, in_rst, out_rs_data, out_rt_data, op, func, cp0_exec, out_branch);

    controller controller_inst(
        .in_branch(out_branch),
        .in_status(cp0_status),
        .in_instr(in_instr),
        .out_pc_sel(out_pc_sel),
        .out_immed_sign(immed_sign),
        .out_ext5_sel(ext5_sel),
        .out_rs_rena(rs_rena),
        .out_rt_rena(rt_rena),
        .out_alu_a_sel(out_alu_a_sel),
        .out_alu_b_sel(out_alu_b_sel),
        .out_aluc(out_aluc),
        .out_mul_ena(out_mul_ena),
        .out_div_ena(out_div_ena),
        .out_clz_ena(out_clz_ena),
        .out_mul_sign(out_mul_sign),
        .out_div_sign(out_div_sign),
        .out_cutter_sign(out_cutter_sign),
        .out_cutter_addr_sel(out_cutter_addr_sel),
        .out_cutter_sel(out_cutter_sel),
        .out_dmem_ena(out_dmem_ena),
        .out_dmem_wena(out_dmem_wena),
        .out_dmem_wsel(out_dmem_wsel),
        .out_dmem_rsel(out_dmem_rsel),
        .out_eret(eret),
        .out_cause(cp0_cause),
        .out_exception(cp0_exec),
        .out_cp0_addr(cp0_addr),
        .out_mfc0(mfc0),
        .out_mtc0(mtc0),
        .out_hi_wena(out_hi_wena),
        .out_lo_wena(out_lo_wena),
        .out_rd_wena(out_rd_wena),
        .out_hi_sel(out_hi_sel),
        .out_lo_sel(out_lo_sel),
        .out_rd_sel(out_rd_sel),
        .out_rdc(out_rd_waddr)
        );

endmodule

module pipe_id_ex(
    input               in_clk,
    input               in_rst,
    input               in_wena,
    input               in_stall,
    input [5:0]         in_op,
    input [5:0]         in_func,
    input [31:0]        in_pc4,
    input [31:0]        in_immed,
    input [31:0]        in_shamt,
    input [31:0]        in_rs_data,
    input [31:0]        in_rt_data,
    input [31:0]        in_hi_data,
    input [31:0]        in_lo_data,
    input [31:0]        in_cp0_data,
    input               in_alu_a_sel,
    input [1:0]         in_alu_b_sel,
    input [3:0]         in_aluc,
    input               in_mul_ena,
    input               in_clz_ena,
    input               in_div_ena,
    input               in_mul_sign,
    input               in_div_sign,
    input               in_cutter_sign,
    input               in_cutter_addr_sel,
    input [2:0]         in_cutter_sel,
    input               in_dmem_ena,
    input               in_dmem_wena,
    input [1:0]         in_dmem_wsel,
    input [1:0]         in_dmem_rsel,
    input               in_hi_wena,
    input               in_lo_wena,
    input               in_rd_wena,
    input [1:0]         in_hi_sel,
    input [1:0]         in_lo_sel,
    input [2:0]         in_rd_sel,
    input [4:0]         in_rd_waddr,

    output reg [5:0]    out_op,
    output reg [5:0]    out_func,
    output reg [31:0]   out_pc4,
    output reg [31:0]   out_immed,
    output reg [31:0]   out_shamt,
    output reg [31:0]   out_rs_data,
    output reg [31:0]   out_rt_data,
    output reg [31:0]   out_hi_data,
    output reg [31:0]   out_lo_data,
    output reg [31:0]   out_cp0_data,
    output reg          out_alu_a_sel,
    output reg [1:0]    out_alu_b_sel,
    output reg [3:0]    out_aluc,
    output reg          out_clz_ena,
    output reg          out_mul_ena,
    output reg          out_div_ena,
    output reg          out_mul_sign,
    output reg          out_div_sign,
    output reg          out_cutter_sign,
    output reg          out_cutter_addr_sel,
    output reg [2:0]    out_cutter_sel,
    output reg          out_dmem_ena,
    output reg          out_dmem_wena,
    output reg [1:0]    out_dmem_wsel,
    output reg [1:0]    out_dmem_rsel,
    output reg          out_rd_wena,
    output reg          out_hi_wena,
    output reg          out_lo_wena,
    output reg [1:0]    out_hi_sel,
    output reg [1:0]    out_lo_sel,
    output reg [2:0]    out_rd_sel,
    output reg [4:0]    out_rd_waddr
    );

    always @(posedge in_clk or posedge in_rst) 
    begin
        if(in_rst || in_stall) 
        begin
            out_cutter_sign     <= 1'b0;
            out_cutter_addr_sel <= 1'b0;
            out_cutter_sel      <= 3'b0;
            out_dmem_ena        <= 1'b0;
            out_dmem_wena       <= 1'b0;
            out_dmem_wsel       <= 2'b0;
            out_dmem_rsel       <= 2'b0;
            out_op              <= 6'b0;
            out_func            <= 6'b0;
            out_immed           <= 32'b0;
            out_shamt           <= 32'b0;
            out_pc4             <= 32'b0;
            out_rs_data         <= 32'b0;
            out_rt_data         <= 32'b0;
            out_hi_data         <= 32'b0;
            out_lo_data         <= 32'b0;
            out_cp0_data        <= 32'b0;
            out_alu_a_sel       <= 1'b0;
            out_alu_b_sel       <= 1'b0;
            out_aluc            <= 4'b0;
            out_mul_ena         <= 1'b0;
            out_div_ena         <= 1'b0;
            out_clz_ena         <= 1'b0;
            out_mul_sign        <= 1'b0;
            out_div_sign        <= 1'b0;
            out_hi_wena         <= 1'b0;
            out_lo_wena         <= 1'b0;
            out_rd_wena         <= 1'b0;
            out_hi_sel          <= 2'b0;
            out_lo_sel          <= 2'b0;
            out_rd_sel          <= 3'b0;
            out_rd_waddr        <= 5'b0;
        end
        else if(in_wena) 
        begin
            out_op              <= in_op;
            out_func            <= in_func;
            out_immed           <= in_immed;
            out_shamt           <= in_shamt;
            out_pc4             <= in_pc4;
            out_dmem_ena        <= in_dmem_ena;
            out_dmem_wena       <= in_dmem_wena;
            out_dmem_wsel       <= in_dmem_wsel;
            out_dmem_rsel       <= in_dmem_rsel;
            out_alu_a_sel       <= in_alu_a_sel;
            out_alu_b_sel       <= in_alu_b_sel;
            out_aluc            <= in_aluc;
            out_rs_data         <= in_rs_data;
            out_rt_data         <= in_rt_data;
            out_hi_data         <= in_hi_data;
            out_lo_data         <= in_lo_data;
            out_cp0_data        <= in_cp0_data;
            out_cutter_sign     <= in_cutter_sign;
            out_cutter_addr_sel <= in_cutter_addr_sel;
            out_cutter_sel      <= in_cutter_sel;
            out_mul_ena         <= in_mul_ena;
            out_div_ena         <= in_div_ena;
            out_clz_ena         <= in_clz_ena;
            out_mul_sign        <= in_mul_sign;
            out_div_sign        <= in_div_sign;
            out_hi_wena         <= in_hi_wena;
            out_lo_wena         <= in_lo_wena;
            out_rd_wena         <= in_rd_wena;
            out_hi_sel          <= in_hi_sel;
            out_lo_sel          <= in_lo_sel;
            out_rd_sel          <= in_rd_sel;
            out_rd_waddr        <= in_rd_waddr;
        end
    end 
endmodule

module pipe_ex(
    input           in_rst,
    input [31:0]    in_pc4,
    input [31:0]    in_immed,
    input [31:0]    in_shamt,
    input [31:0]    in_rs_data,
    input [31:0]    in_rt_data,
    input [31:0]    in_hi_data,
    input [31:0]    in_lo_data,
    input [31:0]    in_cp0_data,
    input           in_alu_a_sel,
    input [1:0]     in_alu_b_sel,
    input [3:0]     in_aluc,
    input           in_mul_ena,
    input           in_div_ena,
    input           in_clz_ena,
    input           in_mul_sign,
    input           in_div_sign,
    input           in_cutter_sign,
    input           in_cutter_addr_sel,
    input [2:0]     in_cutter_sel,
    input           in_dmem_ena,
    input           in_dmem_wena,
    input [1:0]     in_dmem_wsel,
    input [1:0]     in_dmem_rsel,
    input           in_rd_wena,
    input           in_hi_wena,
    input           in_lo_wena,
    input [1:0]     in_hi_sel,
    input [1:0]     in_lo_sel,
    input [2:0]     in_rd_sel,
    input [4:0]     in_rd_waddr,
    output [31:0]   out_pc4,
    output [31:0]   out_mul_hi,
    output [31:0]   out_mul_lo,
    output [31:0]   out_div_r,
    output [31:0]   out_div_q,
    output [31:0]   out_rs_data,
    output [31:0]   out_rt_data,
    output [31:0]   out_hi_data,
    output [31:0]   out_lo_data,
    output [31:0]   out_cp0_data,
    output [31:0]   out_clz_data,
    output [31:0]   out_alu_data,
    output          out_cutter_sign,
    output          out_cutter_addr_sel,
    output [2:0]    out_cutter_sel,
    output          out_dmem_ena,
    output          out_dmem_wena,
    output [1:0]    out_dmem_wsel,
    output [1:0]    out_dmem_rsel,
    output          out_hi_wena,
    output          out_lo_wena,
    output          out_rd_wena,
    output [1:0]    out_hi_sel,
    output [1:0]    out_lo_sel,
    output [2:0]    out_rd_sel,
    output [4:0]    out_rd_waddr
);

    wire [31:0] alu_a;
    wire [31:0] alu_b;
    wire zero, carry, negative, overdlow;

    assign out_pc4              = in_pc4;
    assign out_cutter_sign      = in_cutter_sign;
    assign out_cutter_addr_sel  = in_cutter_addr_sel;
    assign out_cutter_sel       = in_cutter_sel;
    assign out_dmem_ena         = in_dmem_ena;
    assign out_dmem_wena        = in_dmem_wena;
    assign out_dmem_rsel        = in_dmem_rsel;
    assign out_dmem_wsel        = in_dmem_wsel;
    assign out_rs_data          = in_rs_data;
    assign out_rt_data          = in_rt_data;
    assign out_hi_data          = in_hi_data;
    assign out_lo_data          = in_lo_data;
    assign out_cp0_data         = in_cp0_data;
    assign out_rd_wena          = in_rd_wena;
    assign out_hi_wena          = in_hi_wena;
    assign out_lo_wena          = in_lo_wena;
    assign out_hi_sel           = in_hi_sel;
    assign out_lo_sel           = in_lo_sel;
    assign out_rd_sel           = in_rd_sel;
    assign out_rd_waddr         = in_rd_waddr;

    mux2_32 mux_alu_a(in_shamt, in_rs_data, in_alu_a_sel, alu_a);
    mux4_32 mux_alu_b(in_rt_data, in_immed, 32'bz, 32'bz, in_alu_b_sel, alu_b);
    alu alu_inst(alu_a, alu_b, in_aluc, out_alu_data, zero, carry, negative, overdlow);

    mult mult_inst(in_rst, in_mul_ena, in_mul_sign, in_rs_data, in_rt_data, out_mul_hi, out_mul_lo);
    div div_inst(in_rst, in_div_ena, in_div_sign, in_rs_data, in_rt_data, out_div_q, out_div_r);

    clz_counter clz_counter_inst(in_rs_data, in_clz_ena, out_clz_data);

endmodule


module pipe_ex_mem(
    input               in_clk,
    input               in_rst,
    input               in_wena,
    input [31:0]        in_pc4,
    input [31:0]        in_rs_data,
    input [31:0]        in_rt_data,
    input [31:0]        in_hi_data,
    input [31:0]        in_lo_data,
    input [31:0]        in_cp0_data,
    input [31:0]        in_alu_data,
    input [31:0]        in_mul_hi,
    input [31:0]        in_mul_lo,
    input [31:0]        in_div_r,
    input [31:0]        in_div_q,
    input [31:0]        in_clz_data,
    input               in_cutter_sign,
    input [2:0]         in_cutter_sel,
    input               in_cutter_addr_sel,
    input               in_dmem_ena,
    input               in_dmem_wena,
    input [1:0]         in_dmem_wsel,
    input [1:0]         in_dmem_rsel,
    input               in_hi_wena,
    input               in_lo_wena,
    input               in_rd_wena,
    input [1:0]         in_hi_sel,
    input [1:0]         in_lo_sel,
    input [2:0]         in_rd_sel,
    input [4:0]         in_rd_waddr,

    output reg [31:0]   out_pc4,
    output reg [31:0]   out_rs_data,
    output reg [31:0]   out_rt_data,
    output reg [31:0]   out_hi_data,
    output reg [31:0]   out_lo_data,
    output reg [31:0]   out_cp0_data,
    output reg [31:0]   out_alu_data,
    output reg [31:0]   out_mul_hi,
    output reg [31:0]   out_mul_lo,
    output reg [31:0]   out_div_r,
    output reg [31:0]   out_div_q,
    output reg [31:0]   out_clz_data,
    output reg          out_cutter_sign,
    output reg          out_cutter_addr_sel,
    output reg [2:0]    out_cutter_sel,
    output reg          out_dmem_ena,
    output reg          out_dmem_wena,
    output reg [1:0]    out_dmem_wsel,
    output reg [1:0]    out_dmem_rsel,
    output reg          out_rd_wena,
    output reg          out_hi_wena,
    output reg          out_lo_wena,
    output reg [1:0]    out_hi_sel,
    output reg [1:0]    out_lo_sel,
    output reg [2:0]    out_rd_sel,
    output reg [4:0]    out_rd_waddr
);

always @(posedge in_clk or posedge in_rst) 
begin
    if(in_rst) 
    begin
        out_pc4             <= 32'b0;
        out_rs_data         <= 32'b0;
        out_rt_data         <= 32'b0;
        out_alu_data        <= 32'b0;
        out_mul_hi          <= 32'b0;
        out_mul_lo          <= 32'b0;
        out_div_r           <= 32'b0;
        out_div_q           <= 32'b0;
        out_clz_data        <= 32'b0;
        out_hi_data         <= 32'b0;
        out_lo_data         <= 32'b0;
        out_cp0_data        <= 32'b0;
        out_rd_waddr        <= 5'b0;
        out_cutter_sign     <= 1'b0;
        out_cutter_addr_sel <= 1'b0;
        out_cutter_sel      <= 3'b0;
        out_dmem_ena        <= 1'b0;
        out_dmem_wena       <= 1'b0;
        out_dmem_wsel       <= 1'b0;
        out_dmem_rsel       <= 1'b0;
        out_hi_wena         <= 1'b0;
        out_lo_wena         <= 1'b0;
        out_rd_wena         <= 1'b0;
        out_hi_sel          <= 2'b0;
        out_lo_sel          <= 2'b0;
        out_rd_sel          <= 3'b0;
    end 
    else if(in_wena) 
    begin
        out_mul_hi          <= in_mul_hi;
        out_mul_lo          <= in_mul_lo;
        out_div_r           <= in_div_r;
        out_div_q           <= in_div_q;
        out_clz_data        <= in_clz_data;
        out_alu_data        <= in_alu_data;
        out_pc4             <= in_pc4;
        out_rs_data         <= in_rs_data;
        out_rt_data         <= in_rt_data;
        out_hi_data         <= in_hi_data;
        out_lo_data         <= in_lo_data;
        out_cp0_data        <= in_cp0_data;
        out_cutter_sign     <= in_cutter_sign;
        out_cutter_addr_sel <= in_cutter_addr_sel;
        out_cutter_sel      <= in_cutter_sel;
        out_dmem_ena        <= in_dmem_ena;
        out_dmem_wena       <= in_dmem_wena;
        out_dmem_wsel       <= in_dmem_wsel;
        out_dmem_rsel       <= in_dmem_rsel;
        out_hi_wena         <= in_hi_wena;
        out_lo_wena         <= in_lo_wena;
        out_rd_wena         <= in_rd_wena;
        out_hi_sel          <= in_hi_sel;
        out_lo_sel          <= in_lo_sel;
        out_rd_sel          <= in_rd_sel;
        out_rd_waddr        <= in_rd_waddr;
    end
end

endmodule

module pipe_mem(
    input           in_clk,
    input [31:0]    in_pc4,
    input [31:0]    in_rs_data,
    input [31:0]    in_rt_data,
    input [31:0]    in_hi_data,
    input [31:0]    in_lo_data,
    input [31:0]    in_cp0_data,
    input [31:0]    in_alu_data,
    input [31:0]    in_mul_hi,
    input [31:0]    in_mul_lo,
    input [31:0]    in_div_r,
    input [31:0]    in_div_q,
    input [31:0]    in_clz_data,
    input           in_cutter_sign,
    input           in_cutter_addr_sel,
    input [2:0]     in_cutter_sel,
    input [1:0]     in_dmem_wsel,
    input [1:0]     in_dmem_rsel,
    input           in_dmem_ena,
    input           in_dmem_wena,
    input           in_hi_wena,
    input           in_lo_wena,
    input           in_rd_wena,
    input [1:0]     in_hi_sel,
    input [1:0]     in_lo_sel,
    input [2:0]     in_rd_sel,
    input [4:0]     in_rd_waddr,

    output [31:0]   our_pc4,
    output [31:0]   out_rs_data,
    output [31:0]   out_hi_data,
    output [31:0]   out_lo_data,
    output [31:0]   out_cp0_data,
    output [31:0]   out_alu_data,
    output [31:0]   out_mul_hi,
    output [31:0]   out_mul_lo,
    output [31:0]   out_div_r,
    output [31:0]   out_div_q,
    output [31:0]   out_clz_data,
    output [31:0]   out_dmem_data,
    output          out_hi_wena,
    output          out_lo_wena,
    output          out_rd_wena,
    output [1:0]    out_hi_sel,
    output [1:0]    out_lo_sel,
    output [2:0]    out_rd_sel,
    output [4:0]    out_rd_waddr
    );

    wire [31:0] in_cutter;
	wire [31:0] dmem_data_temp;

    assign our_pc4      = in_pc4;
	assign out_mul_hi   = in_mul_hi;
    assign out_mul_lo   = in_mul_lo;
    assign out_div_q    = in_div_q;
    assign out_div_r    = in_div_r;
    assign out_clz_data = in_clz_data;
    assign out_alu_data = in_alu_data;
    assign out_rs_data  = in_rs_data;
    assign out_hi_data  = in_hi_data;
    assign out_lo_data  = in_lo_data;
    assign out_cp0_data = in_cp0_data;
    assign out_hi_wena  = in_hi_wena;
    assign out_lo_wena  = in_lo_wena;
    assign out_rd_wena  = in_rd_wena;
    assign out_hi_sel   = in_hi_sel;
    assign out_lo_sel   = in_lo_sel;
    assign out_rd_sel   = in_rd_sel;
    assign out_rd_waddr = in_rd_waddr;

    mux2_32 mux_cutter(in_rt_data, dmem_data_temp, in_cutter_addr_sel, in_cutter);
    cutter cutter_inst(in_cutter, in_cutter_sel, in_cutter_sign, out_dmem_data);

    dmem dmem_inst(in_clk, in_dmem_ena, in_dmem_wena, in_dmem_wsel, in_dmem_rsel, 
                    out_dmem_data, in_alu_data, dmem_data_temp);

endmodule

module pipe_mem_wb(
    input               in_clk,
    input               in_rst,
    input               in_wena,
    input [31:0]        in_pc4,
    input [31:0]        in_rs_data,
    input [31:0]        in_hi_data,
    input [31:0]        in_lo_data,
    input [31:0]        in_cp0_data,
    input [31:0]        in_alu_data,
    input [31:0]        in_mul_hi,
    input [31:0]        in_mul_lo,
    input [31:0]        in_div_r,
    input [31:0]        in_div_q,
    input [31:0]        in_clz_data,
    input [31:0]        in_dmem_data,
    input               in_hi_wena,
    input               in_lo_wena,
    input               in_rd_wena,
    input [1:0]         in_hi_sel,
    input [1:0]         in_lo_sel,
    input [2:0]         in_rd_sel,
    input [4:0]         in_rd_waddr,

    output reg [31:0]   out_pc4,
    output reg [31:0]   out_rs_data,
    output reg [31:0]   out_hi_data,
    output reg [31:0]   out_lo_data,
    output reg [31:0]   out_cp0_data,
    output reg [31:0]   out_alu_data,
    output reg [31:0]   out_mul_hi,
    output reg [31:0]   out_mul_lo,
    output reg [31:0]   out_div_r,
    output reg [31:0]   out_div_q,
    output reg [31:0]   out_clz_data,
    output reg [31:0]   out_dmem_data,
    output reg          out_hi_wena,
    output reg          out_lo_wena,
    output reg          out_rd_wena,
    output reg [1:0]    out_hi_sel,
    output reg [1:0]    out_lo_sel,
    output reg [2:0]    out_rd_sel,
    output reg [4:0]    out_rd_waddr
    );

    always @(posedge in_clk or posedge in_rst) 
    begin
        if(in_rst)
        begin
            out_pc4         <= 32'b0;
            out_rs_data     <= 32'b0;
            out_hi_data     <= 32'b0;
            out_lo_data     <= 32'b0;
            out_cp0_data    <= 32'b0;
            out_alu_data    <= 32'b0;
            out_mul_hi      <= 32'b0;
            out_mul_lo      <= 32'b0;
            out_div_r       <= 32'b0;
            out_div_q       <= 32'b0;
            out_clz_data    <= 32'b0;
            out_dmem_data   <= 32'b0;
            out_rd_wena     <= 1'b0;
            out_hi_wena     <= 1'b0;
            out_lo_wena     <= 1'b0;
            out_hi_sel      <= 2'b0;
            out_lo_sel      <= 2'b0;
            out_rd_sel      <= 3'b0;
            out_rd_waddr    <= 5'b0;
        end
        else if(in_wena)
        begin
            out_pc4         <= in_pc4;		    
            out_rs_data     <= in_rs_data;
            out_hi_data     <= in_hi_data;
            out_lo_data     <= in_lo_data;
            out_cp0_data    <= in_cp0_data;
            out_alu_data    <= in_alu_data;
            out_mul_hi      <= in_mul_hi;			
            out_mul_lo      <= in_mul_lo;
            out_div_r       <= in_div_r;			
            out_div_q       <= in_div_q;
            out_clz_data    <= in_clz_data;
            out_dmem_data   <= in_dmem_data;
            out_rd_wena     <= in_rd_wena;
            out_hi_wena     <= in_hi_wena;
            out_lo_wena     <= in_lo_wena;
            out_hi_sel      <= in_hi_sel;
            out_lo_sel      <= in_lo_sel;
            out_rd_sel      <= in_rd_sel;
            out_rd_waddr    <= in_rd_waddr;
        end
    end 

endmodule

module pipe_wb(
    input [31:0]    in_pc4,
    input [31:0]    in_rs_data,
    input [31:0]    in_hi_data,
    input [31:0]    in_lo_data,
    input [31:0]    in_cp0_data,
    input [31:0]    in_alu_data,
    input [31:0]    in_mul_hi,
    input [31:0]    in_mul_lo,
    input [31:0]    in_div_r,
    input [31:0]    in_div_q,
    input [31:0]    in_clz_data,
    input [31:0]    in_dmem_data,
    input           in_hi_wena,
    input           in_lo_wena,
    input           in_rd_wena,
    input [1:0]     in_hi_sel,
    input [1:0]     in_lo_sel,
    input [2:0]     in_rd_sel,
    input [4:0]     in_rd_waddr,

    output          out_hi_wena,
    output          out_lo_wena,
    output          out_rd_wena,
    output [4:0]    out_rd_waddr,
    output [31:0]   out_hi_data,
    output [31:0]   out_lo_data,
    output [31:0]   out_rd_data
    );
	
    assign out_hi_wena   = in_hi_wena;
    assign out_lo_wena   = in_lo_wena;
	assign out_rd_wena   = in_rd_wena;
	assign out_rd_waddr  = in_rd_waddr;

    mux4_32 mux_hi(in_div_r, in_mul_hi, in_rs_data, 32'hz, in_hi_sel, out_hi_data);
    mux4_32 mux_lo(in_div_q, in_mul_lo, in_rs_data, 32'hz, in_lo_sel, out_lo_data);

    mux8_32 mux_rd(in_lo_data, in_pc4, in_clz_data, in_cp0_data, 
                    in_dmem_data, in_alu_data, in_hi_data, in_mul_lo, 
                    in_rd_sel, out_rd_data);

endmodule
