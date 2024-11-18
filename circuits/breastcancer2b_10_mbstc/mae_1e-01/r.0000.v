module cgp(input [1:0] input_a, input [1:0] input_b, input [1:0] input_c, input [1:0] input_d, input [1:0] input_e, output [0:0] cgp_out);
  wire cgp_core_014;
  wire cgp_core_017;
  wire cgp_core_018;
  wire cgp_core_019;
  wire cgp_core_021;
  wire cgp_core_022;
  wire cgp_core_028;
  wire cgp_core_030_not;
  wire cgp_core_033;
  wire cgp_core_036;
  wire cgp_core_039;
  wire cgp_core_041;
  wire cgp_core_043;
  wire cgp_core_044_not;
  wire cgp_core_048;
  wire cgp_core_052;
  wire cgp_core_054;

  assign cgp_core_014 = input_b[1] | input_e[1];
  assign cgp_core_017 = ~(input_a[1] ^ input_e[1]);
  assign cgp_core_018 = ~(input_a[0] & input_c[1]);
  assign cgp_core_019 = ~(input_a[1] ^ input_a[1]);
  assign cgp_core_021 = input_a[1] | cgp_core_014;
  assign cgp_core_022 = input_a[1] & cgp_core_014;
  assign cgp_core_028 = ~(input_c[0] | input_d[1]);
  assign cgp_core_030_not = ~input_a[0];
  assign cgp_core_033 = ~input_a[1];
  assign cgp_core_036 = input_c[1] ^ input_e[0];
  assign cgp_core_039 = ~(input_c[1] & input_d[1]);
  assign cgp_core_041 = ~(input_a[0] & input_b[0]);
  assign cgp_core_043 = cgp_core_021 & cgp_core_039;
  assign cgp_core_044_not = ~input_a[0];
  assign cgp_core_048 = input_b[0] ^ input_b[1];
  assign cgp_core_052 = input_e[1] | input_b[0];
  assign cgp_core_054 = cgp_core_043 | cgp_core_022;

  assign cgp_out[0] = cgp_core_054;
endmodule