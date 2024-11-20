module cgp(input [2:0] input_a, input [2:0] input_b, output [0:0] cgp_out);
  wire cgp_core_008;
  wire cgp_core_010;
  wire cgp_core_011;
  wire cgp_core_013;
  wire cgp_core_016_not;
  wire cgp_core_019_not;
  wire cgp_core_021;
  wire cgp_core_022;

  assign cgp_core_008 = ~(input_b[0] | input_a[2]);
  assign cgp_core_010 = ~input_b[2];
  assign cgp_core_011 = ~(input_a[2] & input_a[1]);
  assign cgp_core_013 = input_a[0] & cgp_core_010;
  assign cgp_core_016_not = ~input_b[0];
  assign cgp_core_019_not = ~input_b[2];
  assign cgp_core_021 = input_a[2] | cgp_core_013;
  assign cgp_core_022 = input_b[0] ^ input_b[0];

  assign cgp_out[0] = cgp_core_021;
endmodule