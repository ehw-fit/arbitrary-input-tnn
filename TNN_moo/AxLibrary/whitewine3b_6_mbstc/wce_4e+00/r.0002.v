module cgp(input [2:0] input_a, input [2:0] input_b, input [2:0] input_c, output [0:0] cgp_out);
  wire cgp_core_011;
  wire cgp_core_012;
  wire cgp_core_018;
  wire cgp_core_019;
  wire cgp_core_022;
  wire cgp_core_025;
  wire cgp_core_026;
  wire cgp_core_031;
  wire cgp_core_032;
  wire cgp_core_033;
  wire cgp_core_034;
  wire cgp_core_036;
  wire cgp_core_040_not;
  wire cgp_core_041;
  wire cgp_core_042;

  assign cgp_core_011 = input_b[1] ^ input_a[0];
  assign cgp_core_012 = input_c[0] & input_b[2];
  assign cgp_core_018 = ~(input_c[2] ^ input_a[0]);
  assign cgp_core_019 = input_b[0] ^ input_c[0];
  assign cgp_core_022 = input_c[2] ^ input_b[1];
  assign cgp_core_025 = input_a[2] | input_b[0];
  assign cgp_core_026 = input_b[1] & input_a[1];
  assign cgp_core_031 = ~(input_c[0] | input_a[0]);
  assign cgp_core_032 = input_c[2] | input_a[0];
  assign cgp_core_033 = ~(input_b[1] | input_c[2]);
  assign cgp_core_034 = ~(input_c[1] & input_c[1]);
  assign cgp_core_036 = input_b[1] | input_c[1];
  assign cgp_core_040_not = ~input_c[1];
  assign cgp_core_041 = cgp_core_026 | input_b[2];
  assign cgp_core_042 = input_a[2] | cgp_core_041;

  assign cgp_out[0] = cgp_core_042;
endmodule