module cgp(input [1:0] input_a, input [1:0] input_b, input [1:0] input_c, input [1:0] input_d, input [1:0] input_e, output [0:0] cgp_out);
  wire cgp_core_012;
  wire cgp_core_013;
  wire cgp_core_016;
  wire cgp_core_018;
  wire cgp_core_021;
  wire cgp_core_023;
  wire cgp_core_024;
  wire cgp_core_025;
  wire cgp_core_032;
  wire cgp_core_034;
  wire cgp_core_035;
  wire cgp_core_041;
  wire cgp_core_042;
  wire cgp_core_045;
  wire cgp_core_050;
  wire cgp_core_052;
  wire cgp_core_054;

  assign cgp_core_012 = ~(input_a[1] | input_e[1]);
  assign cgp_core_013 = ~(input_b[0] | input_a[1]);
  assign cgp_core_016 = ~(input_c[1] & input_d[1]);
  assign cgp_core_018 = input_a[0] | input_c[1];
  assign cgp_core_021 = input_c[1] | input_e[0];
  assign cgp_core_023 = ~(input_e[1] & input_e[0]);
  assign cgp_core_024 = ~(input_d[1] ^ input_c[0]);
  assign cgp_core_025 = ~(input_d[0] | input_b[0]);
  assign cgp_core_032 = ~input_d[1];
  assign cgp_core_034 = input_a[0] ^ input_e[1];
  assign cgp_core_035 = input_c[0] ^ input_d[0];
  assign cgp_core_041 = ~(input_a[0] & input_b[0]);
  assign cgp_core_042 = ~input_d[1];
  assign cgp_core_045 = input_e[0] ^ input_a[0];
  assign cgp_core_050 = input_b[0] | input_b[1];
  assign cgp_core_052 = ~(input_c[0] | input_b[0]);
  assign cgp_core_054 = ~input_e[0];

  assign cgp_out[0] = cgp_core_016;
endmodule