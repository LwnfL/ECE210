`default_nettype none

module lif (
    input wire [7:0]    current,
    input wire          clk,
    input wire          rst_n,
    output wire [7:0]   state,
    output wire         spike

);
    wire[7:0] next_state;
    reg[7:0] threadhold;

    always @(posedge clk) begin
        if (!rst_n) begin
            state <= 0;
            threadhold <= 200;
        end else begin
            state <= next_state;
        end
        
    end

    assign next_state = current + (spike? state >> 1 : 0);
    assign spike = (state >= threadhold);
    
endmodule