`timescale 1ns / 1ns

module pcreg(
    input               clk,
    input               ena,
    input               rst,
    input               stall,
    input      [31:0]   pc_in,
    output reg [31:0]   pc_out
    );
    
    always@(posedge clk or posedge rst)
    begin
        if(rst)
        begin
            pc_out <= 32'h00400000;
        end
        else if(ena)
        begin
            if(stall)
            begin
                pc_out <= pc_out;
            end
            else
            begin
                pc_out <= pc_in;
            end
        end
        else
        begin
            pc_out <= 32'bz;
        end
    end
    
endmodule