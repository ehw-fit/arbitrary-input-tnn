module cgp(input [1:0] input_a, input [1:0] input_b, input [1:0] input_c, input [1:0] input_d, output [0:0] cgp_out);
  wire cgp_core_010;
  wire cgp_core_014;
  wire cgp_core_015_not;
  wire cgp_core_016_not;
  wire cgp_core_018;
  wire cgp_core_022;
  wire cgp_core_027;
  wire cgp_core_030;
  wire cgp_core_032;
  wire cgp_core_033;
  wire cgp_core_036;
  wire cgp_core_038;
  wire cgp_core_039;
  wire cgp_core_040;
  wire cgp_core_041;
  wire cgp_core_042;

  assign cgp_core_010 = ~input_a[0];
  assign cgp_core_014 = input_c[0] | input_a[1];
  assign cgp_core_015_not = ~input_b[1];
  assign cgp_core_016_not = ~input_d[0];
  assign cgp_core_018 = ~(input_b[0] & input_a[0]);
  assign cgp_core_022 = ~input_b[1];
  assign cgp_core_027 = ~(input_c[1] ^ input_d[0]);
  assign cgp_core_030 = input_b[0] & input_b[1];
  assign cgp_core_032 = ~input_c[1];
  assign cgp_core_033 = ~input_a[1];
  assign cgp_core_036 = ~(input_a[0] ^ input_b[0]);
  assign cgp_core_038 = ~(input_a[1] | input_a[1]);
  assign cgp_core_039 = ~(input_d[1] | input_c[0]);
  assign cgp_core_040 = input_c[0] | input_b[1];
  assign cgp_core_041 = input_a[1] & input_b[1];
  assign cgp_core_042 = ~(input_c[0] | input_a[0]);

  assign cgp_out[0] = 1'b1;
endmodule