module cgp(input [2:0] input_a, input [2:0] input_b, input [2:0] input_c, output [0:0] cgp_out);
  wire cgp_core_011;
  wire cgp_core_013;
  wire cgp_core_014;
  wire cgp_core_015;
  wire cgp_core_017_not;
  wire cgp_core_018;
  wire cgp_core_019;
  wire cgp_core_024;
  wire cgp_core_025;
  wire cgp_core_026_not;
  wire cgp_core_029;
  wire cgp_core_030;
  wire cgp_core_032;
  wire cgp_core_034;
  wire cgp_core_035;
  wire cgp_core_037;
  wire cgp_core_039;

  assign cgp_core_011 = input_a[0] ^ input_b[0];
  assign cgp_core_013 = input_a[1] ^ input_b[1];
  assign cgp_core_014 = input_a[1] ^ input_a[2];
  assign cgp_core_015 = input_a[0] ^ input_a[0];
  assign cgp_core_017_not = ~cgp_core_013;
  assign cgp_core_018 = ~(input_b[0] | input_b[2]);
  assign cgp_core_019 = input_a[1] & input_a[2];
  assign cgp_core_024 = ~input_a[0];
  assign cgp_core_025 = ~input_a[2];
  assign cgp_core_026_not = ~input_a[1];
  assign cgp_core_029 = input_c[1] ^ input_b[0];
  assign cgp_core_030 = ~(input_a[1] & input_c[1]);
  assign cgp_core_032 = ~(input_c[2] ^ input_b[1]);
  assign cgp_core_034 = input_a[2] ^ input_c[0];
  assign cgp_core_035 = ~(input_c[2] ^ cgp_core_034);
  assign cgp_core_037 = ~(cgp_core_011 & input_c[0]);
  assign cgp_core_039 = ~input_a[1];

  assign cgp_out[0] = 1'b1;
endmodule