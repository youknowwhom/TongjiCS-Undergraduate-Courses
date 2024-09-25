`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/07 23:55:09
// Design Name: 
// Module Name: encoder83_Pri
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


module encoder83_Pri(
    input [7:0] iData,
    input iEI,
    output reg [2:0] oData,
    output reg oEO
);
    always@ (*)
    begin
        if(iEI == 1)
            {oData, oEO} =  4'b1110;
        else
        begin
            casex(iData)
                8'b11111111 : {oData, oEO} = 4'b1110;
                8'b11111110 : {oData, oEO} = 4'b1111;
                8'b1111110x : {oData, oEO} = 4'b1101;
                8'b111110xx : {oData, oEO} = 4'b1011;
                8'b11110xxx : {oData, oEO} = 4'b1001;
                8'b1110xxxx : {oData, oEO} = 4'b0111;
                8'b110xxxxx : {oData, oEO} = 4'b0101;
                8'b10xxxxxx : {oData, oEO} = 4'b0011;               
                8'b0xxxxxxx : {oData, oEO} = 4'b0001;
            endcase
        end
     end
  
endmodule
