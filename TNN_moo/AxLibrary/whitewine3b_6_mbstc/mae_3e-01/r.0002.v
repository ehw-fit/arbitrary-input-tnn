module cgp(input [2:0] input_a, input [2:0] input_b, input [2:0] input_c, output [0:0] cgp_out);
  wire cgp_core_015;
  wire cgp_core_017;
  wire cgp_core_018;
  wire cgp_core_019;
  wire cgp_core_025;
  wire cgp_core_026;
  wire cgp_core_029;
  wire cgp_core_030;
  wire cgp_core_032;
  wire cgp_core_035;
  wire cgp_core_037;
  wire cgp_core_038_not;
  wire cgp_core_039;
  wire cgp_core_040;
  wire cgp_core_041;

  assign cgp_core_015 = input_b[2] | input_a[2];
  assign cgp_core_017 = ~(input_c[0] ^ input_c[1]);
  assign cgp_core_018 = input_b[1] & input_c[2];
  assign cgp_core_019 = ~input_b[0];
  assign cgp_core_025 = input_b[1] & input_c[2];
  assign cgp_core_026 = ~(input_b[2] | input_b[2]);
  assign cgp_core_029 = ~(input_b[1] ^ input_c[1]);
  assign cgp_core_030 = ~(input_a[0] & input_c[0]);
  assign cgp_core_032 = ~input_c[0];
  assign cgp_core_035 = ~(input_a[0] ^ input_b[0]);
  assign cgp_core_037 = input_b[1] | input_a[2];
  assign cgp_core_038_not = ~input_c[0];
  assign cgp_core_039 = input_b[2] ^ input_b[0];
  assign cgp_core_040 = ~input_b[2];
  assign cgp_core_041 = input_a[1] ^ input_a[0];

  assign cgp_out[0] = cgp_core_015;
endmodule