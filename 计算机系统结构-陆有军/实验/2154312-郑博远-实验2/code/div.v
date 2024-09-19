`timescale 1ns / 1ps

module div(
    input           in_rst,
    input           in_ena,
    input           in_sign,
    input [31:0]    in_a,
    input [31:0]    in_b,
    output [31:0]   out_q,
    output [31:0]   out_r
    );

    reg neg;
    reg div_neg;
    reg [63:0] dividend_tmp;
    reg [63:0] divisor_tmp;

    integer i;
	
    always@(*) 
    begin
        if(in_rst) 
        begin
            dividend_tmp    <= 0;
            divisor_tmp     <= 0;
            neg             <= 0;
            div_neg         <= 0;
        end 
        else if(in_ena) 
        begin
            if(in_sign) 
            begin
                dividend_tmp = in_a;
                divisor_tmp = { in_b, 32'b0 }; 
                for(i = 0; i < 32; i = i + 1)
                begin
                    dividend_tmp = dividend_tmp << 1;
                    if(dividend_tmp >= divisor_tmp)
                    begin
                        dividend_tmp = dividend_tmp - divisor_tmp;
                        dividend_tmp = dividend_tmp + 1;
                    end
                end
                i = 0;
            end 
            else 
            begin
                dividend_tmp    <= in_a;
                divisor_tmp     <= { in_b, 32'b0 };
                neg             <= in_a[31] ^ in_b[31];
                div_neg         <= in_a[31];
                
                if(in_a[31]) 
                begin
					dividend_tmp = in_a ^ 32'hffffffff;
					dividend_tmp = dividend_tmp + 1;
                end
                if(in_b[31]) 
                begin
                    divisor_tmp = {in_b ^ 32'hffffffff, 32'b0};
                    divisor_tmp = divisor_tmp + 64'h0000000100000000;
                end 
                for(i = 0; i < 32; i = i + 1) 
                begin
                    dividend_tmp = dividend_tmp << 1;
                    if(dividend_tmp >= divisor_tmp) 
                    begin
                        dividend_tmp = dividend_tmp - divisor_tmp;
                        dividend_tmp = dividend_tmp + 1;
                    end
                end
                if(div_neg) 
                begin
                    dividend_tmp = dividend_tmp ^ 64'hffffffff00000000;
                    dividend_tmp = dividend_tmp + 64'h0000000100000000;
                end          
                if(neg) 
                begin
                    dividend_tmp = dividend_tmp ^ 64'h00000000ffffffff;
                    dividend_tmp = dividend_tmp + 64'h0000000000000001;
                    if(dividend_tmp[31:0] == 32'b0) 
                        dividend_tmp = dividend_tmp - 64'h0000000100000000;

                end
            end
        end
    end
    
	assign out_q = in_ena ? dividend_tmp[31:0] : 32'b0;
    assign out_r = in_ena ? dividend_tmp[63:32]: 32'b0;

endmodule
