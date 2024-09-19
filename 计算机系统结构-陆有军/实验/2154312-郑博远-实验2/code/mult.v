`timescale 1ns / 1ps

module mult(  
    input           in_rst,
    input           in_ena,     
    input           in_sign, 
    input [31:0]    in_a,
    input [31:0]    in_b,
    output [31:0]   out_hi,
    output [31:0]   out_lo
    );

	reg [31:0] a_tmp;
	reg [31:0] b_tmp;
    reg [63:0] ans_tmp;
    reg [63:0] ans;
    reg neg;

    integer i;
	
    always@(*) 
    begin
        if(in_rst) 
        begin
		    a_tmp   <= 0;
            b_tmp   <= 0;
            ans     <= 0;
            neg     <= 0;
        end 
        else if(in_ena) 
        begin
            if(in_a == 0 || in_b == 0) 
            begin
                ans <= 0;
            end 
            else if(~in_sign) 
            begin
                ans = 0;
                for(i = 0; i < 32; i = i + 1) 
                begin
                    ans_tmp = in_b[i] ?({ 32'b0, in_a } << i) : 64'b0;
                    ans = ans + ans_tmp;       
                end
            end 
            else 
            begin
                ans = 0;
                neg = in_a[31] ^ in_b[31];
                a_tmp = in_a;
                b_tmp = in_b;
                if(in_a[31]) 
                begin
                    a_tmp = in_a ^ 32'hffffffff;
                    a_tmp = a_tmp + 1;
                end
                if(in_b[31]) 
                begin
                    b_tmp = in_b ^ 32'hffffffff;
                    b_tmp = b_tmp + 1;
                end
                for(i = 0; i < 32; i = i + 1) 
                begin
                    ans_tmp = b_tmp[i] ?({ 32'b0, a_tmp } << i):64'b0;
                    ans = ans + ans_tmp;       
                end
                if(neg) 
                begin
                    ans = ans ^ 64'hffffffffffffffff;
                    ans = ans + 1;
                end
            end
        end
    end

	assign out_lo = in_ena ? ans[31:0]  : 32'b0;
    assign out_hi = in_ena ? ans[63:32] : 32'b0;
    
endmodule
