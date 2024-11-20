module cgp(input [2:0] input_a, input [2:0] input_b, input [2:0] input_c, output [0:0] cgp_out);
  wire cgp_core_011;
  wire cgp_core_015;
  wire cgp_core_016;
  wire cgp_core_018_not;
  wire cgp_core_019;
  wire cgp_core_020;
  wire cgp_core_021;
  wire cgp_core_028;
  wire cgp_core_030_not;
  wire cgp_core_031;
  wire cgp_core_036;
  wire cgp_core_037;
  wire cgp_core_040;

  assign cgp_core_011 = ~(input_b[1] ^ input_c[1]);
  assign cgp_core_015 = input_c[2] ^ input_b[2];
  assign cgp_core_016 = input_a[2] & input_a[1];
  assign cgp_core_018_not = ~input_c[0];
  assign cgp_core_019 = input_b[0] | input_b[1];
  assign cgp_core_020 = ~(cgp_core_018_not ^ input_b[2]);
  assign cgp_core_021 = input_b[0] & input_b[0];
  assign cgp_core_028 = ~input_c[0];
  assign cgp_core_030_not = ~input_c[1];
  assign cgp_core_031 = input_b[2] & input_c[2];
  assign cgp_core_036 = ~(input_a[2] ^ input_b[2]);
  assign cgp_core_037 = ~(input_c[0] ^ input_a[0]);
  assign cgp_core_040 = input_a[0] | input_c[0];

  assign cgp_out[0] = 1'b0;
endmodule