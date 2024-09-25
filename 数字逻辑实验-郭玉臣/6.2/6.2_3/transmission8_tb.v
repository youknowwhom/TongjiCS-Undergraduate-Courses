`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/09/26 11:32:12
// Design Name: 
// Module Name: transmission8_tb
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


module transmission8_tb();
    wire [7:0] iData;
    wire A, B, C;
    wire [7:0] oData;
    reg [7:0] iDatatot;
    reg [2:0] ctrl;
    assign iData = iDatatot;
    assign {A, B, C} = ctrl;
    
    initial
    begin
        iDatatot = 8'b00000000;
        #10;
        for(iDatatot = 8'b00000001; iDatatot <= 8'b10000000; iDatatot = iDatatot << 1)
        begin
            #20;
        end
    end
    
    initial
    begin
        for(ctrl = 3'b000; ctrl <= 3'b111; ctrl = ctrl + 3'b001)
        begin
            #20;
        end
    end
    
    transmission8 transmission8_instc(iData, A, B, C, oData);
endmodule
