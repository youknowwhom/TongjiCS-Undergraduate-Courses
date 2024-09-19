`timescale 1ns / 1ns

module board_top(
    input           in_clk,
    input           in_rst,

    input   [15:0]  in_data,
    input           is_init_floors,
    input           is_init_resistance,
    
    output  [7:0]   o_seg,
    output  [7:0]   o_sel,
    
    output          result_is_last_broken
    );

    wire    [31:0]  pc;
    wire    [31:0]  instruction; 

    reg     [15:0]  init_floors;
    reg     [15:0]  init_resistance;

    wire    [31:0]  result_attempt_count;
    wire    [31:0]  result_broken_count;
    wire            new_clk;
    
    clk_divider #(4) clk_divider_uut(
        .in_clk(in_clk),
        .out_clk(new_clk)
    );

    always @(posedge in_clk) 
    begin
        // 初始化楼层数
        if(is_init_floors)
            init_floors     <= in_data;
        // 初始化耐摔值
        else if(is_init_resistance)
            init_resistance <= in_data;
    end

    cpu cpu_uut(
        .in_clk(new_clk),
        .in_rst(in_rst),

        .init_floors({ 16'b0, init_floors }),
        .init_resistance({ 16'b0, init_resistance }),

        .out_pc(pc),
        .out_instruction(instruction),

        .result_attempt_count(result_attempt_count),
        .result_broken_count(result_broken_count),
        .result_is_last_broken(result_is_last_broken)
    );

    seg7x16 seg7(
        .clk(in_clk),
        .reset(in_rst),
        .cs(1'b1),
        .i_data({ result_attempt_count[15:0], result_broken_count[15:0] }),
        .o_seg(o_seg),
        .o_sel(o_sel)
    );

endmodule