module cgp(input [1:0] input_a, input [1:0] input_b, input [1:0] input_c, input [1:0] input_d, output [0:0] cgp_out);
  wire cgp_core_011;
  wire cgp_core_012;
  wire cgp_core_016;
  wire cgp_core_018;
  wire cgp_core_019;
  wire cgp_core_021;
  wire cgp_core_023;
  wire cgp_core_024;
  wire cgp_core_029;
  wire cgp_core_030;
  wire cgp_core_031;
  wire cgp_core_033;
  wire cgp_core_040;
  wire cgp_core_041;

  assign cgp_core_011 = ~(input_d[0] & input_b[1]);
  assign cgp_core_012 = input_d[0] & input_b[1];
  assign cgp_core_016 = input_b[1] | input_b[1];
  assign cgp_core_018 = ~input_c[1];
  assign cgp_core_019 = ~(input_a[0] & input_c[1]);
  assign cgp_core_021 = ~(input_a[1] | input_b[1]);
  assign cgp_core_023 = ~(input_b[1] ^ input_c[1]);
  assign cgp_core_024 = ~input_d[0];
  assign cgp_core_029 = ~(input_b[1] ^ input_b[1]);
  assign cgp_core_030 = input_d[1] | input_c[0];
  assign cgp_core_031 = ~(input_c[1] | input_d[0]);
  assign cgp_core_033 = ~cgp_core_021;
  assign cgp_core_040 = ~(input_d[0] | input_c[0]);
  assign cgp_core_041 = input_b[1] ^ input_c[0];

  assign cgp_out[0] = 1'b1;
endmodule