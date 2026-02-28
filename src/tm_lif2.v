`default_nettype none

module tm_lif2 (
    input  wire [7:0] current0,
    input  wire [7:0] current1,
    input  wire       clk,
    input  wire       rst_n,
    output reg  [7:0] state0,
    output reg        spike0,
    output reg  [7:0] state1,
    output reg        spike1
);

    // same vibe as your lif.v
    localparam [7:0] THRESHOLD = 8'd200;
    localparam [7:0] LEAK      = 8'd1;

    reg sel;  // 0 -> update neuron0, 1 -> update neuron1

    reg [7:0] next_state0, next_state1;
    reg       next_spike0, next_spike1;

    // combinational update equations for each neuron
    // (we'll *apply* only one of them each clock)
    always @(*) begin
        // default: hold
        next_state0 = state0;
        next_spike0 = 1'b0;

        next_state1 = state1;
        next_spike1 = 1'b0;

        // --- neuron0 math ---
        begin : n0_math
            reg [7:0] s;
            s = (state0 > LEAK) ? (state0 - LEAK) : 8'd0;
            s = s + current0;

            if (s >= THRESHOLD) begin
                next_spike0 = 1'b1;
                next_state0 = 8'd0;
            end else begin
                next_spike0 = 1'b0;
                next_state0 = s;
            end
        end

        // --- neuron1 math ---
        begin : n1_math
            reg [7:0] s;
            s = (state1 > LEAK) ? (state1 - LEAK) : 8'd0;
            s = s + current1;

            if (s >= THRESHOLD) begin
                next_spike1 = 1'b1;
                next_state1 = 8'd0;
            end else begin
                next_spike1 = 1'b0;
                next_state1 = s;
            end
        end
    end

    // time-muxed state updates: only write one neuron per clock
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sel    <= 1'b0;
            state0 <= 8'd0;
            spike0 <= 1'b0;
            state1 <= 8'd0;
            spike1 <= 1'b0;
        end else begin
            sel <= ~sel;

            // clear spikes unless we update that neuron this cycle
            spike0 <= 1'b0;
            spike1 <= 1'b0;

            if (sel == 1'b0) begin
                // update neuron0 this tick
                state0 <= next_state0;
                spike0 <= next_spike0;
            end else begin
                // update neuron1 this tick
                state1 <= next_state1;
                spike1 <= next_spike1;
            end
        end
    end

endmodule

`default_nettype wire