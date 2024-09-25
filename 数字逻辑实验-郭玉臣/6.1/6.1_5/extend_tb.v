//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/09/19 22:19:29
// Design Name: 
// Module Name: extend_tb
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

`timescale 1ns/1ns 
    module extend_tb; 
    reg [15:0] a;
    reg sext; 
    wire [31:0] b; 
    // Instantiate the Unit Under Test (UUT) 
    extend uut (.a(a),.sext(sext),.b(b)); 
    initial 
     begin 
        // Initialize Inputs 
        a = 0; 
        sext = 0; 
        // Wait 100 ns for global reset to finish 
        #100; 
        // Add stimulus here 
        sext = 1; 
        a = 16'h0000; 
        #100; 
        sext = 0; 
        a = 16'h8000; 
        #100; 
        sext = 1; 
        a = 16'h8000; 
        #100; 
        sext = 0; 
        a = 16'hffff; 
        #100; 
        sext = 1; 
        a = 16'hffff; 
        #100;                                                                           
     end 
endmodule
