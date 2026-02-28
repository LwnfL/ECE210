`default_nettype none

module tt_um_lif (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

  // --- Internal wires for the time-multiplexed LIF core ---
  wire [7:0] lif_state1;
  wire       lif_spike1;

  wire [7:0] lif_state2;
  wire       lif_spike2;

  tm_lif2 tm0 (
      .current0(ui_in),  
      .current1(uio_in), 
      .clk(clk),
      .rst_n(rst_n),
      .state0(lif_state1),
      .spike0(lif_spike1),
      .state1(lif_state2),
      .spike1(lif_spike2)
  );

  // Neuron 0 state on uo_out[5:0], spikes on uo_out[7:6]
  assign uo_out = { lif_spike2, lif_spike1, lif_state1[5:0] };

  // All bidirectional pins are inputs (neuron 1 current)
  assign uio_out = 8'b0;
  assign uio_oe  = 8'b0;

  // Unused inputs
  wire _unused = &{ena, 1'b0};

endmodule