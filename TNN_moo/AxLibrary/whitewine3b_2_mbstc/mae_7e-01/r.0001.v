module cgp(input [2:0] input_a, input [2:0] input_b, output [0:0] cgp_out);
  wire cgp_core_008;
  wire cgp_core_009;
  wire cgp_core_010;
  wire cgp_core_011_not;
  wire cgp_core_016;
  wire cgp_core_019;
  wire cgp_core_020;
  wire cgp_core_021;
  wire cgp_core_022;
  wire cgp_core_023;

  assign cgp_core_008 = ~input_b[2];
  assign cgp_core_009 = input_a[0] ^ input_a[0];
  assign cgp_core_010 = ~(input_b[1] ^ input_b[1]);
  assign cgp_core_011_not = ~input_a[0];
  assign cgp_core_016 = ~(input_b[1] | input_a[1]);
  assign cgp_core_019 = input_a[1] | input_b[0];
  assign cgp_core_020 = input_b[2] ^ input_b[2];
  assign cgp_core_021 = ~input_b[0];
  assign cgp_core_022 = input_b[0] ^ input_a[2];
  assign cgp_core_023 = input_a[2] | input_b[1];

  assign cgp_out[0] = input_a[2];
endmodule