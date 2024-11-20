module cgp(input [2:0] input_a, input [2:0] input_b, output [0:0] cgp_out);
  wire cgp_core_008;
  wire cgp_core_010;
  wire cgp_core_012;
  wire cgp_core_013;
  wire cgp_core_014;
  wire cgp_core_015;
  wire cgp_core_020;

  assign cgp_core_008 = ~(input_a[0] ^ input_b[1]);
  assign cgp_core_010 = ~(input_b[1] & input_b[2]);
  assign cgp_core_012 = input_a[1] | input_a[0];
  assign cgp_core_013 = input_a[1] ^ cgp_core_010;
  assign cgp_core_014 = ~input_b[2];
  assign cgp_core_015 = ~input_a[2];
  assign cgp_core_020 = ~(input_a[1] | input_b[2]);

  assign cgp_out[0] = 1'b0;
endmodule