`timescale 1ns / 1ns

module clk_divider(
    input      in_clk,
    output reg out_clk = 0
);

    parameter k   = 20;
    integer   cnt = 0;

    always @(posedge in_clk)
    begin
        cnt = (cnt + 1) % (k / 2);
        if(cnt == 0)
            out_clk <= ~out_clk;
    end

endmodule