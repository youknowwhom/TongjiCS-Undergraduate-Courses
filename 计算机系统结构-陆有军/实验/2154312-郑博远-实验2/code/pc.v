`timescale 1ns / 1ps

module pc(
    input               in_clk,
    input               in_rst,
    input               in_ena,
    input               in_stall,
    input  [31:0]       in_pc,
    output reg [31:0]   out_pc
    );

    always@(posedge in_clk or posedge in_rst)
    begin
        if(in_rst) 
            out_pc <= 32'h00400000;
        else if(~in_stall) 
        begin
            if(in_ena) 
                out_pc <= in_pc;
        end
    end

endmodule