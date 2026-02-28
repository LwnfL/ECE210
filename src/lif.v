`default_nettype none

module lif (
    input  wire [7:0] current,
    input  wire       clk,
    input  wire       rst_n,
    output reg  [7:0] state,
    output reg        spike
);

    localparam [7:0] THRESHOLD = 8'd200;  
    localparam [7:0] LEAK      = 8'd1;    

    reg [7:0] next_state;
    reg       next_spike;

    always @(*) begin
        // leak
        if (state > LEAK)
            next_state = state - LEAK;
        else
            next_state = 8'd0;

        // integrate input
        next_state = next_state + current;

        // threshold check
        if (next_state >= THRESHOLD) begin
            next_spike = 1'b1;
            next_state = 8'd0;   // reset after spike
        end else begin
            next_spike = 1'b0;
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= 8'd0;
            spike <= 1'b0;
        end else begin
            state <= next_state;
            spike <= next_spike;
        end
    end

endmodule

`default_nettype wire