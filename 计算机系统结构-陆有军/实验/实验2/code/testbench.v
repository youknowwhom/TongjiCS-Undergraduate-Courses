`timescale 1ns / 1ps

module testbench();
    reg           clk, rst, ena;
    wire [7:0]    o_seg, o_sel;

    initial 
    begin
        clk = 1'b0;
        rst = 1'b1;
        ena = 1'b1;
        #1 
        rst = 1'b0;
    end

    always 
    begin
        #1 
        clk = ~clk;
    end

    wire [31:0] pc      = testbench.board_top_inst.cpu_inst.pc;
    wire [31:0] instr   = testbench.board_top_inst.cpu_inst.instr;
    wire [31:0] reg0    = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[0];
    wire [31:0] reg1    = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[1];
    wire [31:0] reg2    = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[2];   
    wire [31:0] reg3    = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[3];
    wire [31:0] reg4    = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[4];
    wire [31:0] reg5    = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[5];
    wire [31:0] reg6    = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[6];
    wire [31:0] reg7    = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[7];
    wire [31:0] reg8    = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[8];
    wire [31:0] reg9    = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[9];
    wire [31:0] reg10   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[10];
    wire [31:0] reg11   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[11];
    wire [31:0] reg12   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[12];
    wire [31:0] reg13   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[13];
    wire [31:0] reg14   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[14];
    wire [31:0] reg15   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[15];
    wire [31:0] reg16   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[16];
    wire [31:0] reg17   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[17];
    wire [31:0] reg18   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[18];
    wire [31:0] reg19   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[19];
    wire [31:0] reg20   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[20];
    wire [31:0] reg21   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[21];
    wire [31:0] reg22   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[22];
    wire [31:0] reg23   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[23];
    wire [31:0] reg24   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[24];
    wire [31:0] reg25   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[25];
    wire [31:0] reg26   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[26];
    wire [31:0] reg27   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[27];
    wire [31:0] reg28   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[28];
    wire [31:0] reg29   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[29];
    wire [31:0] reg30   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[30];
    wire [31:0] reg31   = testbench.board_top_inst.cpu_inst.pipe_id_inst.regfile_inst.array_reg[31];

    board_top board_top_inst(.clk(clk), .rst(rst), .ena(ena), .o_seg(o_seg), .o_sel(o_sel));

endmodule