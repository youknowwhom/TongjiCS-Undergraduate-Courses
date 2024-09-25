`timescale 1ns / 1ns

module regfile(
    input               in_clk,
    input               in_rst,

    input               in_rs_rena,
    input               in_rt_rena,
    input               in_rd_wena,
    input   [4:0]       in_rd_addr,
    input   [4:0]       in_rs_addr,
    input   [4:0]       in_rt_addr,
    input   [31:0]      in_rd_data,

    input   [31:0]      init_floors,
    input   [31:0]      init_resistance,

    output reg [31:0]   out_rs_data,
    output reg [31:0]   out_rt_data,

    output  [31:0]      result_attempt_count,
    output  [31:0]      result_broken_count,
    output              result_is_last_broken
);

    assign result_attempt_count     = array_reg[4];
    assign result_broken_count      = array_reg[5];
    assign result_is_last_broken    = array_reg[6][0];

    reg [31:0] array_reg[31:0];

    always @(posedge in_clk or posedge in_rst)
    begin
        if (in_rst)
            begin
                array_reg[0]  <= 32'b0;
                array_reg[1]  <= 32'b0;
                array_reg[2]  <= init_floors;
                array_reg[3]  <= init_resistance;
                array_reg[4]  <= 32'b0;
                array_reg[5]  <= 32'b0;
                array_reg[6]  <= 32'b0;
                array_reg[7]  <= 32'b0;
                array_reg[8]  <= 32'b0;
                array_reg[9]  <= 32'b0;
                array_reg[10] <= 32'b0;
                array_reg[11] <= 32'b0;
                array_reg[12] <= 32'b0;
                array_reg[13] <= 32'b0;
                array_reg[14] <= 32'b0;
                array_reg[15] <= 32'b0;
                array_reg[16] <= 32'b0;
                array_reg[17] <= 32'b0;
                array_reg[18] <= 32'b0;
                array_reg[19] <= 32'b0;
                array_reg[20] <= 32'b0;
                array_reg[21] <= 32'b0;
                array_reg[22] <= 32'b0;
                array_reg[23] <= 32'b0;
                array_reg[24] <= 32'b0;
                array_reg[25] <= 32'b0;
                array_reg[26] <= 32'b0;
                array_reg[27] <= 32'b0;
                array_reg[28] <= 32'b0;
                array_reg[29] <= 32'b0;
                array_reg[30] <= 32'b0;
                array_reg[31] <= 32'b0;
            end
        else if(in_rd_wena && in_rd_addr != 0)
        begin
            array_reg[in_rd_addr] <= in_rd_data;
        end
    end

    always @(negedge in_clk)
    begin
        if(in_rst) 
        begin
            out_rs_data <= 0;
            out_rt_data <= 0;
        end
        else 
        begin
            if(in_rs_rena)
            begin
                out_rs_data <= ((in_rd_wena && (in_rd_addr == in_rs_addr)) ? in_rd_data : array_reg[in_rs_addr]);
            end
            else
            begin
                out_rs_data <= 32'b0;
            end

            if(in_rt_rena)
            begin
                out_rt_data <= ((in_rd_wena && (in_rd_addr == in_rt_addr)) ? in_rd_data : array_reg[in_rt_addr]);
            end
            else
            begin
                out_rt_data <= 32'b0;
            end
        end
    end

endmodule