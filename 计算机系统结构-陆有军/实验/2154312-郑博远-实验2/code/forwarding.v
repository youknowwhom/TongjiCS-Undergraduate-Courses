`include "mips_def.vh"
`timescale 1ns / 1ps

module forwarding(
    input               in_clk,
    input               in_rst,
    input [5:0]         in_op,
    input [5:0]         in_func,
    input               in_rs_rena,
    input               in_rt_rena,
    input [4:0]         in_rsc,
    input [4:0]         in_rtc,

    input [5:0]         in_exe_op,
    input [5:0]         in_exe_func,
    input [31:0]        in_exe_hi_data,
    input [31:0]        in_exe_lo_data,
    input [31:0]        in_exe_rd_data,
    input               in_exe_hi_wena,
    input               in_exe_lo_wena,
    input               in_exe_rd_wena,
    input [4:0]         in_exe_rdc,

    input [31:0]        in_mem_hi_data,
    input [31:0]        in_mem_lo_data,
    input [31:0]        in_mem_rd_data,
    input               in_mem_hi_wena,
    input               in_mem_lo_wena,
    input               in_mem_rd_wena,
    input [4:0]         in_mem_rdc,

    output reg          out_stall,
    output reg          out_forwarding,
    output reg          out_is_rs,
    output reg          out_is_rt,
    output reg [31:0]   out_rs_data,
    output reg [31:0]   out_rt_data,
    output reg [31:0]   out_hi_data,
    output reg [31:0]   out_lo_data
    );


    always@(negedge in_clk or posedge in_rst) 
    begin
        if(in_rst) 
        begin
            out_stall       <= 1'b0;
            out_rs_data     <= 32'b0;
            out_rt_data     <= 32'b0;
            out_hi_data     <= 32'b0;
            out_lo_data     <= 32'b0;
            out_forwarding  <= 1'b0;
            out_is_rs       <= 1'b0;
            out_is_rt       <= 1'b0;
        end 
        else if(out_stall) 
        begin
            out_stall <= 1'b0;
            if(out_is_rs) 
                out_rs_data <= in_mem_rd_data;
            else if(out_is_rt)
                out_rt_data <= in_mem_rd_data;
        end 
        else if(~out_stall) 
        begin
            out_forwarding = 0;
            out_is_rs = 0;
            out_is_rt = 0;
            if(in_op == `OP_MFHI && in_func == `FUNC_MFHI) 
            begin
                if(in_exe_hi_wena) 
                begin
                    out_hi_data     <= in_exe_hi_data;
                    out_forwarding  <= 1'b1;
                end 
                else if(in_mem_hi_wena) 
                begin
                    out_hi_data     <= in_mem_hi_data;
                    out_forwarding  <= 1'b1;
                end
            end 
            else if(in_op == `OP_MFLO && in_func == `FUNC_MFLO) 
            begin
                if(in_exe_lo_wena) 
                begin
                    out_lo_data     <= in_exe_lo_data;
                    out_forwarding  <= 1'b1;
                end 
                else if(in_mem_lo_wena) 
                begin
                    out_lo_data     <= in_mem_lo_data;
                    out_forwarding  <= 1'b1;
                end
            end 
            else 
            begin
                // 先分析rs的冲突
                if(in_exe_rd_wena && in_rs_rena && in_exe_rdc == in_rsc) 
                begin
                    if(in_exe_op == `OP_LW || in_exe_op == `OP_LH || in_exe_op == `OP_LHU || in_exe_op == `OP_LB || in_exe_op == `OP_LBU) 
                    begin
                        out_is_rs       <= 1'b1;
                        out_stall       <= 1'b1;
                        out_forwarding  <= 1'b1;
                    end
                    else 
                    begin
                        out_is_rs       <= 1'b1;
                        out_rs_data     <= in_exe_rd_data;
                        out_forwarding  <= 1'b1;
                    end
                end
                else if(in_mem_rd_wena && in_rs_rena && in_mem_rdc == in_rsc) 
                begin
                    out_is_rs       <= 1'b1;
                    out_rs_data     <= in_mem_rd_data;
                    out_forwarding  <= 1'b1;
                end
                // 分析rt的分析，与上面相似
                if(in_exe_rd_wena && in_rt_rena && in_exe_rdc == in_rtc) 
                begin
                    if(in_exe_op == `OP_LW || in_exe_op == `OP_LH || in_exe_op == `OP_LHU || in_exe_op == `OP_LB || in_exe_op == `OP_LBU) 
                    begin
                        out_is_rt       <= 1'b1;
                        out_stall       <= 1'b1;
                        out_forwarding  <= 1'b1;
                    end 
                    else 
                    begin
                        out_is_rt       <= 1'b1;
                        out_rt_data     <= in_exe_rd_data;
                        out_forwarding  <= 1'b1;
                    end
                end 
                else if(in_mem_rd_wena && in_rt_rena && in_mem_rdc == in_rtc) 
                begin
                    out_is_rt       <= 1'b1;
                    out_rt_data     <= in_mem_rd_data;
                    out_forwarding  <= 1'b1;
                end
            end
        end
	end      

endmodule