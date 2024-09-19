`timescale 1ns / 1ps

module regfile(
    input 				in_clk, 
    input 				in_rst, 
    input 				in_rd_wena, 
    input 	[4:0]		in_rs_addr, 
    input 	[4:0]		in_rt_addr, 
    input 				in_rs_ena,
    input 				in_rt_ena,
    input 	[4:0] 		in_rd_addr, 
    input 	[31:0] 		in_rd_data, 
    output reg [31:0] 	out_rs_data, 
    output reg [31:0] 	out_rt_data,
    output [31:0] 		out_reg28
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
		else 
		begin
            if(in_rd_wena && (in_rd_addr != 0))
                array_reg[in_rd_addr] = in_rd_data;
        end
	end

	always@(*) 
	begin
	    if (in_rst) 
			out_rs_data <= 32'b0;
	    else if (in_rs_addr == 5'b0) 
	  		out_rs_data <= 32'b0;
	    else if((in_rs_addr == in_rd_addr) && in_rd_wena && in_rs_ena) 
	  	    out_rs_data <= in_rd_data;
	    else if(in_rs_ena) 
	        out_rs_data <= array_reg[in_rs_addr];
	    else 
	        out_rs_data <= 32'bz;
	end

	always@(*) 
    begin
	    if(in_rst) 
			out_rt_data <= 32'b0;
	    else if(in_rt_addr == 5'b0) 
	  		out_rt_data <= 32'b0;
        else if((in_rt_addr == in_rd_addr) && in_rd_wena && in_rt_ena) 
            out_rt_data <= in_rd_data;
	    else if(in_rt_ena) 
	        out_rt_data <= array_reg[in_rt_addr];
	    else 
	        out_rt_data <= 32'bz;
	end

	assign out_reg28 = array_reg[28];

endmodule

