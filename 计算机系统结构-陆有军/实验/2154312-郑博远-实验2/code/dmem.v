`timescale 1ns / 1ps

module dmem(
    input 				in_clk,
    input 				in_ena,
    input 				in_wena,
    input [1:0] 		in_wsel,
    input [1:0] 		in_rsel, 
    input [31:0] 		in_data,
    input [31:0] 		in_addr,
    output reg [31:0] 	out_data
    );

	reg [31:0] ram [2047:0];
	
	wire [9:0] addr_hi = (in_addr - 32'h10010000) >> 2;
	wire [1:0] addr_lo = (in_addr - 32'h10010000) & 2'b11;

    always@(*) 
	begin
        if(in_ena && ~in_wena) 
		begin
		case(in_rsel)
			2'b01:
			begin
				out_data <= ram[addr_hi];
			end
			2'b10:
			begin
				case(addr_lo)
					2'b00:out_data <= ram[addr_hi][15:0];
					2'b10:out_data <= ram[addr_hi][31:16];
				endcase
			end
			2'b11:
			begin
				case(addr_lo)
					2'b00:	out_data <= ram[addr_hi][7:0];
					2'b01:	out_data <= ram[addr_hi][15:8];
					2'b10:	out_data <= ram[addr_hi][23:16];
					2'b11:	out_data <= ram[addr_hi][31:24];
				endcase
			end
		endcase
        end
    end

    always@(posedge in_clk) 
	begin
        if(in_ena) 
		begin
            if(in_wena)
			begin
			case(in_wsel)
                2'b01:
				begin
					ram[addr_hi] <= in_data; 
				end
                2'b10:
				begin
					case(addr_lo)
						2'b00:	ram[addr_hi][15:0] 	<= in_data[15:0];
						2'b11:	ram[addr_hi][31:16] <= in_data[15:0];
					endcase
				end
                2'b11:
				begin
					case(addr_lo)
						2'b00:	ram[addr_hi][7:0] 	<= in_data[7:0];
						2'b01:	ram[addr_hi][15:8] 	<= in_data[7:0];
						2'b10:	ram[addr_hi][23:16] <= in_data[7:0];
						2'b11:	ram[addr_hi][31:24] <= in_data[7:0];
					endcase
				end
            endcase
            end
        end
    end
endmodule

module cutter(
    input [31:0] 		in,
    input [2:0] 		in_sel,
    input 				in_sign,
    output reg [31:0] 	out
    );
	
    always@(*) 
	begin
        case(in_sel)
            3'b010: 	out <= { { 24{ in_sign & in[7] } }, in[7:0] };
            3'b011: 	out <= { 24'b0, in[7:0] };
			3'b001: 	out <= { { 16{ in_sign & in[15] } }, in[15:0] };
            3'b100: 	out <= { 16'b0, in[15:0] };
            default: 	out <= in;
        endcase
    end

endmodule
