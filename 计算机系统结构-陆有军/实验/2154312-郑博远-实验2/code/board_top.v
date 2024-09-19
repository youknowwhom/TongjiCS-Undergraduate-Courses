
`timescale 1ns / 1ps

module board_top(
    input           clk,
    input           rst,
    input           ena,
    input  [1:0]    switch,
    output [7:0]    o_seg,
    output [7:0]    o_sel
    );

    wire [31:0] display_data;
    wire [31:0] pc, instr;
    wire [31:0] reg28;

    wire        clk_cpu;
    reg [20:0]  clk_div;

    always@(posedge clk)
        clk_div = clk_div + 1;
    
    // assign clk_cpu = clk_div[19];       // 下板时用于分频
    assign clk_cpu = clk;               // 仿真时直接使用

    mux4_32 mux_display(reg28, pc, instr, 32'b0, switch, display_data);

    seg7x16 seg7x16_inst(clk, rst, 1'b1, display_data, o_seg, o_sel);

    cpu cpu_inst(clk_cpu, rst, ena, pc, instr, reg28);

endmodule
