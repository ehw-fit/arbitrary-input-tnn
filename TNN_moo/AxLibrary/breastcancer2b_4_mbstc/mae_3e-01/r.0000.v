module cgp(input [1:0] input_a, input [1:0] input_b, input [1:0] input_c, input [1:0] input_d, output [0:0] cgp_out);
  wire cgp_core_010;
  wire cgp_core_011;
  wire cgp_core_012;
  wire cgp_core_014;
  wire cgp_core_015;
  wire cgp_core_017;
  wire cgp_core_019_not;
  wire cgp_core_020;
  wire cgp_core_021_not;
  wire cgp_core_022;
  wire cgp_core_030;
  wire cgp_core_031;
  wire cgp_core_033;
  wire cgp_core_035;
  wire cgp_core_036;

  assign cgp_core_010 = input_b[1] ^ input_d[0];
  assign cgp_core_011 = input_c[1] & input_d[0];
  assign cgp_core_012 = input_c[1] ^ input_d[1];
  assign cgp_core_014 = input_c[1] ^ cgp_core_011;
  assign cgp_core_015 = ~(cgp_core_012 | cgp_core_011);
  assign cgp_core_017 = input_b[0] | cgp_core_010;
  assign cgp_core_019_not = ~input_b[1];
  assign cgp_core_020 = input_b[1] & input_d[1];
  assign cgp_core_021_not = ~input_b[0];
  assign cgp_core_022 = cgp_core_019_not & input_c[0];
  assign cgp_core_030 = ~input_a[1];
  assign cgp_core_031 = cgp_core_021_not & cgp_core_030;
  assign cgp_core_033 = ~(cgp_core_021_not | input_a[1]);
  assign cgp_core_035 = ~input_a[0];
  assign cgp_core_036 = input_b[0] & cgp_core_035;

  assign cgp_out[0] = 1'b1;
endmodule