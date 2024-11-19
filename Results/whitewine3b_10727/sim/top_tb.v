`timescale 1ms/1us
module top_tb #(`include "./sim/parameters.vh") ();

localparam SUM_BITS = $clog2(HIDDEN_CNT+1);
reg clk;
reg [FEAT_CNT*FEAT_BITS-1:0] features;
wire [$clog2(CLASS_CNT)-1:0] prediction;
reg [FEAT_CNT*FEAT_BITS-1:0] testcases [0:TEST_CNT-1];
reg [$clog2(CLASS_CNT)-1:0] gold [0:TEST_CNT-1];
parameter Nsperiod = 5000;
localparam period = 200; //1000;//Nsperiod/1000;

initial $readmemh("./sim/test.memh", testcases);
initial $readmemh("./sim/gold.memh", gold);

top DUT (.features(features), .prediction(prediction));


integer i, j, file;
real correct=0;
initial begin
    for(i = 0; i < TEST_CNT; i = i + 1) begin
        features = testcases[i];
        #period
	if (prediction==gold[i]) correct=correct+1;
    end
    $display("Accuracy %.2f", 100*correct/TEST_CNT);
end

endmodule
