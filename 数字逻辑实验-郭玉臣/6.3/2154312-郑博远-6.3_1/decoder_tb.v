`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/07 19:49:41
// Design Name: 
// Module Name: decoder_tb
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


module decoder_tb;
    reg [3 : 0] iData;
    reg [2 : 0] iEna;
    wire [7 : 0] oData;
    initial
    begin
        for(iEna = 0; iEna <= 2'b11; iEna = iEna + 2'b01)
            for(iData = 0; iData <= 3'b111; iData = iData + 3'b001)
                begin
                    #20;
                end
    end
    decoder
    decoder_instc(iData[2 : 0], iEna[1 : 0], oData);
endmodule
