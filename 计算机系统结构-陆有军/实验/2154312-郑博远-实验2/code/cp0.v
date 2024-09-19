`include "mips_def.vh"
`timescale 1ns / 1ps

module cp0(
    input           in_clk,
    input           in_rst,
    input           in_mfc0,
    input           in_mtc0,
    input   [31:0]  in_pc,
    input   [4:0]   in_rdc,
    input   [31:0]  in_wdata,
    input           in_exception,
    input           in_eret,
    input   [4:0]   in_cause,
    output  [31:0]  out_rdata,
    output  [31:0]  out_status,
    output  [31:0]  out_eaddr
);

    reg [31:0] array_reg [31:0];
    integer i;

    always@(posedge in_clk or posedge in_rst)
    begin
        if(in_rst)
        begin
            for(i = 0; i < 32; i = i + 1)
                array_reg[i] <= 32'b0;
        end
        else if(in_mtc0)
        begin
            array_reg[in_rdc] <= in_wdata;
        end
        else if(in_exception)
        begin
            array_reg[`STATUS] <= { array_reg[`STATUS][26:0], 5'b0 };
            array_reg[`CAUSE]  <= { 25'd0, in_cause, 2'd0 };
            array_reg[`EPC]    <= in_pc;
        end
        else if(in_eret)
        begin
            array_reg[`STATUS] <= { 5'b0, array_reg[`STATUS][31:5] };
        end    
    end
   
    
    assign out_status  = array_reg[`STATUS];
    assign out_eaddr   = in_eret ? array_reg[`EPC] : 32'h00400004;  
    assign out_rdata   = in_mfc0 ? array_reg[in_rdc] : 32'bz;

endmodule
