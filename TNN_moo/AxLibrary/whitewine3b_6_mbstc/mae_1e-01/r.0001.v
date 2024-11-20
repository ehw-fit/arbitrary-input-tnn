module cgp(input [2:0] input_a, input [2:0] input_b, input [2:0] input_c, output [0:0] cgp_out);
  wire cgp_core_011;
  wire cgp_core_012_not;
  wire cgp_core_013;
  wire cgp_core_016;
  wire cgp_core_017;
  wire cgp_core_021;
  wire cgp_core_022;
  wire cgp_core_023;
  wire cgp_core_024;
  wire cgp_core_028;
  wire cgp_core_029;
  wire cgp_core_031;
  wire cgp_core_033;
  wire cgp_core_036;
  wire cgp_core_039;
  wire cgp_core_041;

  assign cgp_core_011 = ~(input_a[0] ^ input_a[2]);
  assign cgp_core_012_not = ~input_a[1];
  assign cgp_core_013 = input_a[1] & input_b[1];
  assign cgp_core_016 = input_b[0] & input_c[0];
  assign cgp_core_017 = ~(input_b[2] ^ input_c[2]);
  assign cgp_core_021 = input_c[2] | input_b[0];
  assign cgp_core_022 = input_b[2] | input_a[2];
  assign cgp_core_023 = input_a[1] | input_b[2];
  assign cgp_core_024 = ~input_c[2];
  assign cgp_core_028 = ~input_a[2];
  assign cgp_core_029 = ~(input_c[1] & input_a[2]);
  assign cgp_core_031 = ~(input_b[1] | input_a[1]);
  assign cgp_core_033 = input_b[0] & input_b[2];
  assign cgp_core_036 = ~input_b[1];
  assign cgp_core_039 = ~(input_b[2] | input_b[2]);
  assign cgp_core_041 = cgp_core_024 | cgp_core_022;

  assign cgp_out[0] = cgp_core_041;
endmodule