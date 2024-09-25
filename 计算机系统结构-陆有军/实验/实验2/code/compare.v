`include "mips_def.vh"
`timescale 1ns / 1ps

module compare(
    input 			in_clk,
    input 			in_rst,
    input 	[31:0] 	in_a, 
    input 	[31:0] 	in_b,
    input 	[5:0] 	in_op,
    input 	[5:0] 	in_func,
    input 			in_exception,
    output reg 		out_branch 
    );
	
	always@(*) 
	begin
	    if(in_rst)
	        out_branch <= 1'b0;
		else if(in_op == `OP_BEQ) 
			out_branch <= (in_a == in_b);
	    else if(in_op == `OP_BNE) 
			out_branch <= (in_a != in_b);
		else if(in_op == `OP_BGEZ) 
			out_branch <= (in_a >= 0);
	    else if(in_op == `OP_J)
			out_branch <= 1'b1;
	    else if(in_op == `OP_JR && in_func == `FUNC_JR)
            out_branch <= 1'b1;
	    else if(in_op == `OP_JAL)
	        out_branch <= 1'b1;
        else if(in_op == `OP_JALR && in_func == `FUNC_JALR)
            out_branch <= 1'b1;
		else if(in_op == `OP_TEQ && in_func == `FUNC_TEQ)
			out_branch <= (in_a == in_b);
        else if(in_exception)
            out_branch <= 1'b1;
        else
            out_branch <= 1'b0;
	end
	
endmodule
