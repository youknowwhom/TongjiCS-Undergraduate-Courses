`timescale 1ns / 1ns

module stall(
    input           in_clk,
    input           in_rst,

    input   [4:0]   in_rs_addr,
    input   [4:0]   in_rt_addr,
    input           in_rs_rena,
    input           in_rt_rena,

    input           in_ex_wena,
    input           in_mem_wena,
    input   [4:0]   in_ex_waddr,
	input   [4:0]   in_mem_waddr,

    output  reg     out_stall
    );

    reg stall_ltime;

    always @ (negedge in_clk or posedge in_rst) 
    begin
        if(in_rst) 
        begin
            out_stall   <= 1'b1;
            stall_ltime <= 1'b0;
        end
        else if (stall_ltime == 0) 
        begin
            // 流水线stall时间到
            if(out_stall) 
            begin
                out_stall <= 1'b0;
            end
            // 正常运行 检测冲突
            else
            begin
                // ex阶段与id阶段读写冲突，stall 2个周期
                if(in_ex_wena && ((in_rs_rena && (in_ex_waddr == in_rs_addr)) || (in_rt_rena && (in_ex_waddr == in_rt_addr)))) 
                begin
                    stall_ltime <= 1'b1;
                    out_stall   <= 1'b1;
                end
                // ex阶段与mem阶段读写冲突，stall 1个周期
                else if(in_mem_wena && ((in_rs_rena && (in_mem_waddr == in_rs_addr)) || (in_rt_rena && (in_mem_waddr == in_rt_addr)))) 
                begin
                    stall_ltime <= 1'b0;
                    out_stall   <= 1'b1;
                end
            end
        end
        else 
        begin
            stall_ltime = stall_ltime - 1;
        end
	end
endmodule