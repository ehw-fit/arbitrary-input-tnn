module cgp(input [2:0] input_a, input [2:0] input_b, input [2:0] input_c, output [0:0] cgp_out);
  wire cgp_core_014;
  wire cgp_core_015;
  wire cgp_core_016;
  wire cgp_core_017;
  wire cgp_core_018;
  wire cgp_core_022;
  wire cgp_core_023;
  wire cgp_core_024;
  wire cgp_core_026;
  wire cgp_core_028;
  wire cgp_core_030;
  wire cgp_core_034;
  wire cgp_core_035_not;
  wire cgp_core_036;
  wire cgp_core_038_not;
  wire cgp_core_039;
  wire cgp_core_041;

  assign cgp_core_014 = ~(input_a[0] & input_b[0]);
  assign cgp_core_015 = input_c[1] ^ input_a[2];
  assign cgp_core_016 = input_c[2] & input_c[2];
  assign cgp_core_017 = cgp_core_014 | input_a[2];
  assign cgp_core_018 = input_a[2] | input_c[0];
  assign cgp_core_022 = input_a[0] | input_b[0];
  assign cgp_core_023 = ~(input_a[0] ^ input_b[1]);
  assign cgp_core_024 = input_a[1] ^ input_b[1];
  assign cgp_core_026 = input_a[1] & input_b[2];
  assign cgp_core_028 = ~input_b[0];
  assign cgp_core_030 = input_c[1] & input_a[0];
  assign cgp_core_034 = ~(input_b[2] & input_c[1]);
  assign cgp_core_035_not = ~input_a[2];
  assign cgp_core_036 = ~(input_a[2] ^ input_c[1]);
  assign cgp_core_038_not = ~input_a[0];
  assign cgp_core_039 = ~(input_c[2] | input_b[0]);
  assign cgp_core_041 = ~input_a[0];

  assign cgp_out[0] = 1'b0;
endmodule