`timescale 1ns / 1ns

module pipe_if(
    input           in_clk,
    input           in_rst,
    input           in_stall,
    input   [31:0]  in_pc_jaddr,
    input   [31:0]  in_pc_baddr,
    input   [1:0]   in_pc_sel,
    output  [31:0]  out_pc,
    output  [31:0]  out_npc,
    output  [31:0]  out_instruction
    );

    wire [31:0] next_pc;

    pcreg pcreg_uut(
        .clk(in_clk),
        .ena(1'b1),
        .rst(in_rst),
        .stall(in_stall),
        .pc_in(next_pc),
        .pc_out(out_pc)
    );
       
    mux4_32 mux4_pc_sel_uut(
        .d0(out_npc),
        .d1(in_pc_baddr),
        .d2(in_pc_jaddr),
        .d3(32'bz),
        .y(next_pc),
        .s(in_pc_sel)
    );
    
    assign out_npc = out_pc + 4;

    imem imem_uut(out_pc >> 2, out_instruction);
    
endmodule