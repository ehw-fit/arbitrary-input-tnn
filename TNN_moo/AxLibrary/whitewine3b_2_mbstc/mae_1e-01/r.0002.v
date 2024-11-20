module cgp(input [2:0] input_a, input [2:0] input_b, output [0:0] cgp_out);
  wire cgp_core_008;
  wire cgp_core_009;
  wire cgp_core_010;
  wire cgp_core_012_not;
  wire cgp_core_014;
  wire cgp_core_017;
  wire cgp_core_019;
  wire cgp_core_020;
  wire cgp_core_021_not;
  wire cgp_core_022;

  assign cgp_core_008 = ~input_b[2];
  assign cgp_core_009 = input_a[2] & cgp_core_008;
  assign cgp_core_010 = ~(input_a[2] ^ input_b[2]);
  assign cgp_core_012_not = ~input_a[1];
  assign cgp_core_014 = input_b[1] | input_b[0];
  assign cgp_core_017 = ~(input_b[1] ^ input_b[1]);
  assign cgp_core_019 = input_a[2] & input_a[1];
  assign cgp_core_020 = input_a[1] & cgp_core_010;
  assign cgp_core_021_not = ~input_b[2];
  assign cgp_core_022 = cgp_core_009 | cgp_core_020;

  assign cgp_out[0] = cgp_core_022;
endmodule