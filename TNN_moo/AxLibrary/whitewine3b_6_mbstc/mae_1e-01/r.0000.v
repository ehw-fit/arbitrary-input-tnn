module cgp(input [2:0] input_a, input [2:0] input_b, input [2:0] input_c, output [0:0] cgp_out);
  wire cgp_core_011;
  wire cgp_core_013;
  wire cgp_core_014;
  wire cgp_core_016;
  wire cgp_core_019;
  wire cgp_core_020;
  wire cgp_core_023;
  wire cgp_core_025;
  wire cgp_core_029;
  wire cgp_core_030;
  wire cgp_core_031;
  wire cgp_core_033;
  wire cgp_core_036;
  wire cgp_core_037;
  wire cgp_core_040;
  wire cgp_core_041;
  wire cgp_core_042;

  assign cgp_core_011 = ~input_b[1];
  assign cgp_core_013 = input_b[0] | input_c[0];
  assign cgp_core_014 = input_c[2] ^ input_c[1];
  assign cgp_core_016 = input_a[1] & input_a[0];
  assign cgp_core_019 = ~(input_b[0] & input_b[0]);
  assign cgp_core_020 = ~(input_c[1] ^ input_b[0]);
  assign cgp_core_023 = ~input_c[2];
  assign cgp_core_025 = input_a[0] ^ input_a[1];
  assign cgp_core_029 = ~(input_b[2] | input_a[0]);
  assign cgp_core_030 = ~(input_a[1] & input_c[0]);
  assign cgp_core_031 = input_b[1] & input_c[2];
  assign cgp_core_033 = ~(input_b[2] & input_c[2]);
  assign cgp_core_036 = ~(input_c[1] ^ input_c[0]);
  assign cgp_core_037 = ~(input_c[1] ^ input_a[2]);
  assign cgp_core_040 = input_a[1] ^ input_b[0];
  assign cgp_core_041 = cgp_core_023 | input_b[2];
  assign cgp_core_042 = input_a[2] | cgp_core_041;

  assign cgp_out[0] = cgp_core_042;
endmodule