module cgp(input [2:0] input_a, input [2:0] input_b, input [2:0] input_c, output [0:0] cgp_out);
  wire cgp_core_011;
  wire cgp_core_012;
  wire cgp_core_014;
  wire cgp_core_016;
  wire cgp_core_017;
  wire cgp_core_018;
  wire cgp_core_020;
  wire cgp_core_023;
  wire cgp_core_024;
  wire cgp_core_026;
  wire cgp_core_029;
  wire cgp_core_033;
  wire cgp_core_034;
  wire cgp_core_038;
  wire cgp_core_039;
  wire cgp_core_041;
  wire cgp_core_042;

  assign cgp_core_011 = ~(input_b[1] & input_c[2]);
  assign cgp_core_012 = ~input_b[2];
  assign cgp_core_014 = input_a[2] | input_b[1];
  assign cgp_core_016 = ~(input_a[1] | input_c[0]);
  assign cgp_core_017 = input_b[1] ^ input_c[1];
  assign cgp_core_018 = input_b[2] ^ input_a[1];
  assign cgp_core_020 = ~(input_b[1] | input_b[2]);
  assign cgp_core_023 = ~input_c[2];
  assign cgp_core_024 = ~input_b[0];
  assign cgp_core_026 = input_b[1] & cgp_core_023;
  assign cgp_core_029 = ~(input_b[1] | input_c[2]);
  assign cgp_core_033 = input_b[1] & input_b[2];
  assign cgp_core_034 = ~input_a[1];
  assign cgp_core_038 = ~(input_c[1] & input_c[1]);
  assign cgp_core_039 = ~(input_b[0] & input_b[1]);
  assign cgp_core_041 = cgp_core_026 | input_b[2];
  assign cgp_core_042 = input_a[2] | cgp_core_041;

  assign cgp_out[0] = cgp_core_042;
endmodule