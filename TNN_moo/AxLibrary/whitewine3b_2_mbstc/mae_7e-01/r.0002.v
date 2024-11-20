module cgp(input [2:0] input_a, input [2:0] input_b, output [0:0] cgp_out);
  wire cgp_core_008;
  wire cgp_core_010;
  wire cgp_core_011;
  wire cgp_core_014;
  wire cgp_core_018;
  wire cgp_core_023;

  assign cgp_core_008 = ~input_a[2];
  assign cgp_core_010 = ~input_a[0];
  assign cgp_core_011 = ~input_b[2];
  assign cgp_core_014 = ~(input_a[2] | input_b[2]);
  assign cgp_core_018 = input_b[0] & input_b[0];
  assign cgp_core_023 = input_a[0] & input_a[2];

  assign cgp_out[0] = input_a[2];
endmodule