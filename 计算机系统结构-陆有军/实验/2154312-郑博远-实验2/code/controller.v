`include "mips_def.vh"
`timescale 1ns / 1ps

module controller (
    input           in_branch,
    input [31:0]    in_status,
    input [31:0]    in_instr,

    output [2:0]    out_pc_sel,
    output          out_immed_sign,
    output          out_ext5_sel,
    output          out_rs_rena,
    output          out_rt_rena,
    output          out_alu_a_sel,
    output [1:0]    out_alu_b_sel,
    output [3:0]    out_aluc,
    output          out_mul_ena,
    output          out_div_ena,
    output          out_clz_ena,
    output          out_mul_sign,
    output          out_div_sign,
    output          out_cutter_sign,
    output          out_cutter_addr_sel,
    output [2:0]    out_cutter_sel,
    output          out_dmem_ena,
    output          out_dmem_wena,
    output [1:0]    out_dmem_wsel,
    output [1:0]    out_dmem_rsel,
    output          out_eret,
    output [4:0]    out_cause,
    output          out_exception,
    output [4:0]    out_cp0_addr,
    output          out_mfc0,
    output          out_mtc0,
    output          out_hi_wena,
    output          out_lo_wena,
    output          out_rd_wena,
    output [1:0]    out_hi_sel,
    output [1:0]    out_lo_sel,
    output [2:0]    out_rd_sel,
    output [4:0]    out_rdc
    );

    wire [5:0] op   = in_instr[31:26];
    wire [5:0] func = in_instr[5:0];

    wire Addi       = (op == 6'b001000);
    wire Addiu      = (op == 6'b001001);
    wire Andi       = (op == 6'b001100);
    wire Ori        = (op == 6'b001101);
    wire Sltiu      = (op == 6'b001011);
    wire Lui        = (op == 6'b001111);
    wire Xori       = (op == 6'b001110);
    wire Slti       = (op == 6'b001010);
    wire Addu       = (op == 6'b000000 && func == 6'b100001);
    wire And        = (op == 6'b000000 && func == 6'b100100);
    wire Beq        = (op == 6'b000100);
    wire Bne        = (op == 6'b000101);
    wire J          = (op == 6'b000010);
    wire Jal        = (op == 6'b000011);
    wire Jr         = (op == 6'b000000 && func == 6'b001000);
    wire Lw         = (op == 6'b100011);
    wire Xor        = (op == 6'b000000 && func == 6'b100110);
    wire Nor        = (op == 6'b000000 && func == 6'b100111);
    wire Or         = (op == 6'b000000 && func == 6'b100101);
    wire Sll        = (op == 6'b000000 && func == 6'b000000);
    wire Sllv       = (op == 6'b000000 && func == 6'b000100);
    wire Sltu       = (op == 6'b000000 && func == 6'b101011);
    wire Sra        = (op == 6'b000000 && func == 6'b000011);
    wire Srl        = (op == 6'b000000 && func == 6'b000010);
    wire Subu       = (op == 6'b000000 && func == 6'b100011);
    wire Sw         = (op == 6'b101011);
    wire Add        = (op == 6'b000000 && func == 6'b100000);
    wire Sub        = (op == 6'b000000 && func == 6'b100010);
    wire Slt        = (op == 6'b000000 && func == 6'b101010);
    wire Srlv       = (op == 6'b000000 && func == 6'b000110);
    wire Srav       = (op == 6'b000000 && func == 6'b000111);
    wire Clz        = (op == 6'b011100 && func == 6'b100000);
    wire Divu       = (op == 6'b000000 && func == 6'b011011);
    wire Eret       = (op == 6'b010000 && func == 6'b011000);
    wire Jalr       = (op == 6'b000000 && func == 6'b001001);
    wire Lb         = (op == 6'b100000);
    wire Lbu        = (op == 6'b100100);
    wire Lhu        = (op == 6'b100101);
    wire Sb         = (op == 6'b101000);
    wire Sh         = (op == 6'b101001);
    wire Lh         = (op == 6'b100001);
    wire Mfc0       = (in_instr[31:21] == 11'b01000000000 && in_instr[10:3] == 8'b0);
    wire Mfhi       = (op == 6'b000000 && func == 6'b010000);
    wire Mflo       = (op == 6'b000000 && func == 6'b010010);
    wire Mtc0       = (in_instr[31:21] == 11'b01000000100 && in_instr[10:3] == 8'b0);
	wire Mthi       = (op == 6'b000000 && func == 6'b010001);
	wire Mtlo       = (op == 6'b000000 && func == 6'b010011);
    wire Mul        = (op == 6'b011100 && func == 6'b000010);
	wire Multu      = (op == 6'b000000 && func == 6'b011001);
	wire Syscall    = (op == 6'b000000 && func == 6'b001100);
	wire Div        = (op == 6'b000000 && func == 6'b011010);
	wire Teq        = (op == 6'b000000 && func == 6'b110100);
    wire Bgez       = (op == 6'b000001);
    wire Break      = (op == 6'b000000 && func == 6'b001101);

	// pc
    assign out_pc_sel[2] = (Beq & in_branch) | (Bne & in_branch) | (Bgez & in_branch) | Eret;
    assign out_pc_sel[1] = ~(J | Jr | Jal | Jalr | (Beq & in_branch) | (Bne & in_branch) | (Bgez & in_branch) | Eret);
    assign out_pc_sel[0] = Eret | out_exception | Jr | Jalr;

	// ext5选择、立即数扩充
    assign out_ext5_sel     = Sllv | Srav | Srlv;
    assign out_immed_sign   = Addi | Addiu | Sltiu | Slti;

	// alu
    assign out_aluc[3]      = Lui | Srl | Slt | Sltu | Sllv | Srlv | Srav | Sra | Slti | Sltiu | Sll;
    assign out_aluc[2]      = And | Or | Xor | Nor | Sll | Srl | Sra | Sllv | Srlv | Srav | Andi | Ori | Xori;
    assign out_aluc[1]      = Add | Sub | Xor | Nor | Slt | Sltu | Sll | Sllv | Addi | Xori | Beq | Bne | Slti | Sltiu | Bgez | Teq;
    assign out_aluc[0]      = Subu | Sub | Or | Nor | Slt | Sllv | Srlv | Sll | Srl | Slti | Ori | Beq | Bne | Bgez | Teq;
    assign out_alu_a_sel    = ~(Sll | Srl | Sra | Div | Divu | Mul | Multu | J | Jr | Jal | Jalr | Mfc0 | Mtc0 | Mfhi | Mflo | Mthi | Mtlo | Clz | Eret | Syscall | Break);
    assign out_alu_b_sel[1] = Bgez;
    assign out_alu_b_sel[0] = Addi | Addiu | Andi | Ori | Xori | Slti | Sltiu | Lb | Lbu | Lh | Lhu | Lw | Sb | Sh | Sw | Lui;

    // 乘除、clz
    assign out_mul_ena   = Mul | Multu;
    assign out_div_ena   = Div | Divu;
    assign out_mul_sign  = Mul;
    assign out_div_sign  = Div;
    assign out_clz_ena   = Clz;

    // dmem
    assign out_dmem_ena     = Lw | Sw | Lh | Sh | Lb | Sb | Lhu | Lbu;
    assign out_dmem_wena    = Sw | Sh | Sb;
    assign out_dmem_wsel[1] = Sh | Sb;
    assign out_dmem_wsel[0] = Sw | Sb;
    assign out_dmem_rsel[1] = Lh | Lb | Lhu | Lbu;
    assign out_dmem_rsel[0] = Lw | Lb | Lbu;     
    assign out_cutter_sign  = Lh | Lb;
    
	// cutter
    assign out_cutter_addr_sel  = ~(Sb | Sh | Sw);
    assign out_cutter_sel[2]    = Sh;
    assign out_cutter_sel[1]    = Lb | Lbu | Sb;
    assign out_cutter_sel[0]    = Lh | Lhu | Sb;

	// regfile
    assign out_rs_rena   = Addi | Addiu | Andi | Ori | Sltiu | Xori | Slti | Addu | And | Beq | Bne | Jr | Lw | Xor | Nor | Or | Sllv | Sltu | Subu | Sw | Add | Sub | Slt | Srlv | Srav | Clz | Divu | Jalr | Lb | Lbu | Lhu | Sb | Sh | Lh | Mul | Multu | Teq | Div;
    assign out_rt_rena   = Addu | And | Beq | Bne | Xor | Nor | Or | Sll | Sllv | Sltu | Sra | Srl | Subu | Sw | Add | Sub | Slt | Srlv | Srav | Divu | Sb | Sh | Mtc0 | Mul | Multu | Teq | Div;
    assign out_rd_wena   = Addi | Addiu | Andi | Ori | Sltiu | Lui | Xori | Slti | Addu | And | Xor | Nor | Or | Sll | Sllv | Sltu | Sra | Srl | Subu | Add | Sub | Slt | Srlv | Srav | Lb | Lbu | Lh | Lhu | Lw | Mfc0 | Clz | Jal | Jalr | Mfhi | Mflo | Mul;
    assign out_rdc = (Add | Addu | Sub | Subu | And | Or | Xor | Nor | Slt | Sltu | Sll | Srl | Sra | Sllv | Srlv | Srav | Clz | Jalr | Mfhi | Mflo | Mul) ? 
                   in_instr[15:11] : (( Addi | Addiu | Andi | Ori | Xori | Lb | Lbu | Lh | Lhu | Lw | Slti | Sltiu | Lui | Mfc0) ? 
                   in_instr[20:16] : (Jal ? 5'd31 : 5'b0));
    assign out_rd_sel[2] = ~(Beq | Bne | Bgez | Div | Divu | Sb | Multu | Sh | Sw | J | Jr | Jal | Jalr | Mfc0 | Mtc0 | Mflo | Mthi | Mtlo | Clz | Eret | Syscall | Teq | Break);
    assign out_rd_sel[1] = Mul | Mfc0 | Mtc0 | Clz | Mfhi;
    assign out_rd_sel[0] = ~(Beq | Bne | Bgez | Div | Divu | Multu | Lb | Lbu | Lh | Lhu | Lw | Sb | Sh | Sw | J | Mtc0 | Mfhi | Mflo | Mthi | Mtlo | Clz | Eret | Syscall | Teq | Break);
    
	// hi, lo
    assign out_hi_wena   = Mul | Multu | Div | Divu | Mthi;
    assign out_hi_sel[1] = Mthi;
    assign out_hi_sel[0] = Mul | Multu;
    assign out_lo_wena   = Mul | Multu | Div | Divu | Mtlo; 
    assign out_lo_sel[1] = Mtlo;
    assign out_lo_sel[0] = Mul | Multu;
	
    assign out_mfc0  = Mfc0;
    assign out_mtc0  = Mtc0;

    assign out_cause        = Break ? `CAUSE_BREAK : (Syscall ? `CAUSE_SYSCALL : (Teq ? `CAUSE_TEQ : 5'bz));
    assign out_eret         = Eret; 
    assign out_cp0_addr     = in_instr[15:11];
    assign out_exception    = in_status[0] && ((Syscall && in_status[1]) || (Break && in_status[2]) || (Teq && in_status[3]));

endmodule
