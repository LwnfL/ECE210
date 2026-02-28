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

  reg [7:0] counter;

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) counter <= 8'd0;
    else        counter <= counter + 8'd1;
  end

  // --- Internal signals for LIF modules ---
  wire [7:0] lif_state1;
  wire       lif_spike1;

  wire [7:0] lif_state2;
  wire       lif_spike2;

 
  tm_lif2 tm0 (
      .current0(ui_in),  // use ui_in as input current for neuron 0
      .current1(uio_in), // use uio_in as input current for neuron 1
      .clk(clk),
      .rst_n(rst_n),
      .state0(lif_state1),
      .spike0(lif_spike1),
      .state1(lif_state2),
      .spike1(lif_spike2)
  );

  // keep counter on uo_out, and expose spikes on uio_out
  assign uo_out  = counter;

  assign uio_out = { lif_spike2, 6'b0, lif_spike1 }; // example mapping
  assign uio_oe  = 8'hFF; 

  // If you actually want uio_out to be driven out, you MUST enable it:
  // assign uio_oe  = 8'b1111_1111;

  // Unused inputs
  wire _unused = &{ena, 1'b0};

endmodule