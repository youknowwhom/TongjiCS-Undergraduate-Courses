`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/09/26 00:45:36
// Design Name: 
// Module Name: selector41
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

module selector32_1(
    input [31:0] iC0,
    input [31:0] iC1,
    input [31:0] iC2,
    input [31:0] iC3,
    input [31:0] iC4,
    input [31:0] iC5,
    input [31:0] iC6,
    input [31:0] iC7,
    input [31:0] iC8,
    input [31:0] iC9,
    input [31:0] iC10,
    input [31:0] iC11,
    input [31:0] iC12,
    input [31:0] iC13,
    input [31:0] iC14,
    input [31:0] iC15,
    input [31:0] iC16,
    input [31:0] iC17,
    input [31:0] iC18,
    input [31:0] iC19,
    input [31:0] iC20,
    input [31:0] iC21,
    input [31:0] iC22,
    input [31:0] iC23,
    input [31:0] iC24,
    input [31:0] iC25,
    input [31:0] iC26,
    input [31:0] iC27,
    input [31:0] iC28,
    input [31:0] iC29,
    input [31:0] iC30,
    input [31:0] iC31,
    input [4:0] iS,
    output reg [31:0] oZ,
    input ena
    );
    always @(*)
    begin
        if(ena)
        begin
            case(iS)
            5'd0 : oZ = iC0;
            5'd1 : oZ = iC1;
            5'd2 : oZ = iC2;
            5'd3 : oZ = iC3;
            5'd4 : oZ = iC4;
            5'd5 : oZ = iC5;
            5'd6 : oZ = iC6;
            5'd7 : oZ = iC7;
            5'd8 : oZ = iC8;
            5'd9 : oZ = iC9;
            5'd10: oZ = iC10;
            5'd11: oZ = iC11;
            5'd12: oZ = iC12;
            5'd13: oZ = iC13;
            5'd14: oZ = iC14;
            5'd15: oZ = iC15;
            5'd16: oZ = iC16;
            5'd17: oZ = iC17;
            5'd18: oZ = iC18;
            5'd19: oZ = iC19;
            5'd20: oZ = iC20;
            5'd21: oZ = iC21;
            5'd22: oZ = iC22;
            5'd23: oZ = iC23;
            5'd24: oZ = iC24;
            5'd25: oZ = iC25;
            5'd26: oZ = iC26;
            5'd27: oZ = iC27;
            5'd28: oZ = iC28;
            5'd29: oZ = iC29;
            5'd30: oZ = iC30;
            5'd31: oZ = iC31;    
            endcase      
        end
        else
            oZ = 32'bz;
    end
endmodule
