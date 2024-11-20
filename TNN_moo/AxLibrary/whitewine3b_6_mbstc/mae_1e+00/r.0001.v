module cgp(input [2:0] input_a, input [2:0] input_b, input [2:0] input_c, output [0:0] cgp_out);
  wire cgp_core_011;
  wire cgp_core_013;
  wire cgp_core_014;
  wire cgp_core_015_not;
  wire cgp_core_016;
  wire cgp_core_019;
  wire cgp_core_023_not;
  wire cgp_core_024;
  wire cgp_core_028;
  wire cgp_core_029;
  wire cgp_core_030;
  wire cgp_core_041;
  wire cgp_core_042;

  assign cgp_core_011 = input_a[0] ^ input_b[0];
  assign cgp_core_013 = input_a[0] ^ input_b[1];
  assign cgp_core_014 = ~(input_a[1] & input_b[1]);
  assign cgp_core_015_not = ~cgp_core_013;
  assign cgp_core_016 = input_a[1] & input_a[1];
  assign cgp_core_019 = input_b[2] & input_b[2];
  assign cgp_core_023_not = ~input_b[1];
  assign cgp_core_024 = ~input_c[2];
  assign cgp_core_028 = input_c[2] & input_a[1];
  assign cgp_core_029 = ~input_c[1];
  assign cgp_core_030 = ~(input_a[1] ^ input_b[2]);
  assign cgp_core_041 = ~(input_c[1] | input_a[0]);
  assign cgp_core_042 = input_b[1] | input_b[2];

  assign cgp_out[0] = 1'b1;
endmodule