`timescale 1ns / 1ns

module controller(
    input           in_branch,
    input [31:0]    in_instruction,
    
    output          out_rs_rena,
    output          out_rt_rena,
    output          out_rd_wena,
    output [4:0]    out_rd_addr,
    output          out_rd_sel,

    output          out_dmem_ena,
    output          out_dmem_wena,
    output [1:0]    out_dmem_type,

    output          out_ext_signed, 
    output          out_alu_a_sel,
    output          out_alu_b_sel,
    output [3:0]    out_alu_sel,
    output [1:0]    out_pc_sel
    );

    wire [5:0] op      = in_instruction[31:26];
    wire [5:0] func    = in_instruction[5:0];
    wire [4:0] rs_addr = in_instruction[25:21];
    wire [4:0] rt_addr = in_instruction[20:16];
    wire [4:0] rd_addr = in_instruction[15:11];

    // R-type
    wire Add    = (op == 6'b000000 && func == 6'b100000);
    wire Addu   = (op == 6'b000000 && func == 6'b100001);
    wire Sub    = (op == 6'b000000 && func == 6'b100010);
    wire Subu   = (op == 6'b000000 && func == 6'b100011);
    wire And    = (op == 6'b000000 && func == 6'b100100);
    wire Or     = (op == 6'b000000 && func == 6'b100101);
    wire Xor    = (op == 6'b000000 && func == 6'b100110);
    wire Nor    = (op == 6'b000000 && func == 6'b100111);
    wire Slt    = (op == 6'b000000 && func == 6'b101010);
    wire Sltu   = (op == 6'b000000 && func == 6'b101011);
    wire Sll    = (op == 6'b000000 && func == 6'b000000);
    wire Srl    = (op == 6'b000000 && func == 6'b000010);
    wire Sra    = (op == 6'b000000 && func == 6'b000011);
    wire Sllv   = (op == 6'b000000 && func == 6'b000100);
    wire Srlv   = (op == 6'b000000 && func == 6'b000110);
    wire Srav   = (op == 6'b000000 && func == 6'b000111);
    wire Jr     = (op == 6'b000000 && func == 6'b001000);
    wire Rtype  = (op == 6'b000000);
        
    // I-type
    wire Addi   = (op == 6'b001000);
    wire Addiu  = (op == 6'b001001);
    wire Andi   = (op == 6'b001100);
    wire Ori    = (op == 6'b001101);
    wire Xori   = (op == 6'b001110);
    wire Lw     = (op == 6'b100011);
    wire Sw     = (op == 6'b101011);
    wire Beq    = (op == 6'b000100);
    wire Bne    = (op == 6'b000101);
    wire Slti   = (op == 6'b001010);
    wire Sltiu  = (op == 6'b001011);
    wire Lui    = (op == 6'b001111);
    wire Itype  = Addi | Addiu | Andi | Ori | Xori | Lw | Sw | Beq | Bne | Slti | Sltiu | Lui;
    
    // J-type
    wire J      = (op == 6'b000010);
    wire Jal    = (op == 6'b000011);
    wire Jtype  = J | Jal;

    assign out_rs_rena = Add | Addu | Sub | Subu | And | Or | Xor | Nor | Slt | Sltu | Sllv | Srlv | Jr | Addi | Addiu | Andi | Ori | Xori | Lw | Sw | Beq | Bne | Slti | Sltiu;
    assign out_rt_rena = Add | Addu | Sub | Subu | And | Or | Xor | Nor | Slt | Sltu | Sll | Srl | Sra | Sllv | Srlv | Srav | Beq | Bne | Sw;
    assign out_rd_wena = Add | Addu | Sub | Subu | And | Or | Xor | Nor | Slt | Sltu | Sll | Srl | Sra | Sllv | Srlv | Srav | Addi | Addiu | Andi | Ori | Xori | Lw | Slti | Sltiu | Lui | Jal;
    assign out_rd_sel  = ~Lw;

    assign out_dmem_ena  = Sw | Lw;
    assign out_dmem_wena = Sw;
    assign out_dmem_type = 2'b00;

    assign out_ext_signed = Addi | Addiu | Lw | Sw | Slti | Sltiu;

    assign out_alu_a_sel = Sll | Srl | Sra;
    assign out_alu_b_sel = Addi | Addiu | Andi | Ori | Xori | Lw | Sw | Slti | Sltiu | Lui;

    assign out_pc_sel[1] = J;
    assign out_pc_sel[0] = (Beq | Bne) & in_branch;

    assign out_alu_sel[3] = Slt | Sltu | Sll | Srl | Sra | Sllv | Srlv | Srav | Slti | Sltiu | Lui;
    assign out_alu_sel[2] = And | Or | Xor | Nor | Sra | Srav | Andi | Ori | Xori | Lui;
    assign out_alu_sel[1] = Sub | Subu | Xor | Nor | Sll | Srl | Sllv | Srlv | Xori | Beq | Bne;
    assign out_alu_sel[0] = Addu | Subu | Or | Nor | Sltu | Srl | Srlv | Addiu | Ori | Sltiu | Lui;

    mux4_5 mux_rd_addr_urrt(
        .d0(5'bz),
        .d1(rt_addr),
        .d2(rd_addr),
        .d3(5'bz),
        .s({Rtype, Itype}),
        .y(out_rd_addr)
    );

endmodule
