module cgp(input [2:0] input_a, input [2:0] input_b, input [2:0] input_c, output [0:0] cgp_out);
  wire cgp_core_011;
  wire cgp_core_012;
  wire cgp_core_016;
  wire cgp_core_017;
  wire cgp_core_018;
  wire cgp_core_020;
  wire cgp_core_022;
  wire cgp_core_024;
  wire cgp_core_025;
  wire cgp_core_026_not;
  wire cgp_core_029;
  wire cgp_core_031;
  wire cgp_core_032;
  wire cgp_core_034;
  wire cgp_core_036;
  wire cgp_core_037;
  wire cgp_core_039;

  assign cgp_core_011 = ~(input_c[2] | input_a[1]);
  assign cgp_core_012 = ~(input_c[0] & input_c[0]);
  assign cgp_core_016 = ~(input_a[2] & input_c[0]);
  assign cgp_core_017 = ~(input_a[0] | input_c[1]);
  assign cgp_core_018 = input_b[1] ^ input_b[0];
  assign cgp_core_020 = ~(input_b[1] ^ input_c[2]);
  assign cgp_core_022 = input_c[2] | input_a[2];
  assign cgp_core_024 = ~cgp_core_022;
  assign cgp_core_025 = input_a[0] & input_c[1];
  assign cgp_core_026_not = ~input_a[2];
  assign cgp_core_029 = input_b[2] & cgp_core_024;
  assign cgp_core_031 = ~(input_c[1] | input_c[1]);
  assign cgp_core_032 = input_a[2] | input_a[0];
  assign cgp_core_034 = input_b[1] ^ input_c[1];
  assign cgp_core_036 = ~(input_a[2] | input_c[0]);
  assign cgp_core_037 = input_b[2] ^ input_c[2];
  assign cgp_core_039 = input_c[1] & input_b[2];

  assign cgp_out[0] = cgp_core_029;
endmodule