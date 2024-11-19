#%%
import numpy as np
import csv
import os
from ariths_gen.core.cgp_circuit import UnsignedCGPCircuit

from tnn_mb_base import TNNMBbase

class TNNBreastcancer2b(TNNMBbase):
    """
    1-bit TNN for 
    """

    def __init__(self):
        super().__init__(dataset_name="breastcancer2b", bw=2, packed=True)        
    
    def get_configs(self):
        return {
            "nodes": 
    {'breastcancer2b_0': [1, -1, 1, -1, -1, -1], 'breastcancer2b_1': [1, -1, 1, 1, 1, 1], 'breastcancer2b_2': [1, 1, 1, 1, -1, -1, 1, 1], 'breastcancer2b_3': [-1, 1, -1, 1, -1], 'breastcancer2b_4': [-1, 1, 1, 1], 'breastcancer2b_5': [1, -1, 1, 1, 1, -1, 1], 'breastcancer2b_6': [1, -1, -1, 1, 1, -1, -1], 'breastcancer2b_7': [1, -1, -1, 1, -1, -1, -1, 1], 'breastcancer2b_8': [1, -1, 1, -1, 1, -1, -1], 'breastcancer2b_9': [-1, -1, 1, 1, 1, -1, 1], 'breastcancer2b_10': [1, 1, -1, -1, 1], 'breastcancer2b_11': [-1, -1, -1, 1, -1, -1, -1, 1, 1]}
,
            "sums":
{'popcount_0': 14, 'popcount_1': 14}
        }


    def tnn(self, rfeature_array, config=None):
        self.set_permutation(config["permutation"] if "permutation" in config else None)

        # Reverse the bits to align with Verilog LSB to MSB reading
        feature_array = rfeature_array[:, ::-1]
        hidden_0 = config['breastcancer2b_0'](feature_array[:, 0],feature_array[:, 2],feature_array[:, 5],feature_array[:, 6],feature_array[:, 7],feature_array[:, 8])
        hidden_1 = np.ones_like(hidden_0)
        hidden_2 = config['breastcancer2b_1'](feature_array[:, 1],feature_array[:, 2],feature_array[:, 3],feature_array[:, 4],feature_array[:, 5],feature_array[:, 7])
        hidden_3 = config['breastcancer2b_2'](feature_array[:, 1],feature_array[:, 2],feature_array[:, 3],feature_array[:, 5],feature_array[:, 6],feature_array[:, 7],feature_array[:, 8],feature_array[:, 9])
        hidden_4 = config['breastcancer2b_3'](feature_array[:, 2],feature_array[:, 3],feature_array[:, 4],feature_array[:, 7],feature_array[:, 8])
        hidden_5 = config['breastcancer2b_4'](feature_array[:, 0],feature_array[:, 2],feature_array[:, 4],feature_array[:, 6])
        hidden_6 = np.zeros_like(hidden_0)
        hidden_7 = config['breastcancer2b_5'](feature_array[:, 1],feature_array[:, 2],feature_array[:, 3],feature_array[:, 4],feature_array[:, 5],feature_array[:, 8],feature_array[:, 9])
        hidden_8 = config['breastcancer2b_6'](feature_array[:, 0],feature_array[:, 2],feature_array[:, 3],feature_array[:, 5],feature_array[:, 6],feature_array[:, 7],feature_array[:, 8])
        hidden_9 = config['breastcancer2b_7'](feature_array[:, 1],feature_array[:, 2],feature_array[:, 3],feature_array[:, 4],feature_array[:, 5],feature_array[:, 6],feature_array[:, 7],feature_array[:, 8])
        hidden_10 = config['breastcancer2b_8'](feature_array[:, 0],feature_array[:, 2],feature_array[:, 4],feature_array[:, 6],feature_array[:, 7],feature_array[:, 8],feature_array[:, 9])
        hidden_11 = config['breastcancer2b_9'](feature_array[:, 1],feature_array[:, 2],feature_array[:, 3],feature_array[:, 4],feature_array[:, 6],feature_array[:, 7],feature_array[:, 8])
        hidden_12 = config['breastcancer2b_10'](feature_array[:, 1],feature_array[:, 2],feature_array[:, 3],feature_array[:, 4],feature_array[:, 6])
        hidden_13 = config['breastcancer2b_11'](feature_array[:, 0],feature_array[:, 2],feature_array[:, 3],feature_array[:, 4],feature_array[:, 5],feature_array[:, 6],feature_array[:, 7],feature_array[:, 8],feature_array[:, 9])
        # Compute inverted hidden states
        hidden_n0 = 1 - hidden_0
        hidden_n1 = 1 - hidden_1
        hidden_n2 = 1 - hidden_2
        hidden_n3 = 1 - hidden_3
        hidden_n4 = 1 - hidden_4
        hidden_n5 = 1 - hidden_5
        hidden_n6 = 1 - hidden_6
        hidden_n7 = 1 - hidden_7
        hidden_n8 = 1 - hidden_8
        hidden_n9 = 1 - hidden_9
        hidden_n10 = 1 - hidden_10
        hidden_n11 = 1 - hidden_11
        hidden_n12 = 1 - hidden_12
        hidden_n13 = 1 - hidden_13

        # Compute popcounts
        popcount = np.zeros((rfeature_array.shape[0], 2), dtype=np.uint8)  # Adjust the second dimension based on CLASS_CNT
        popcount[:, 0] = config["popcount_0"](self.debinarize2(hidden_0,hidden_1,hidden_n2,hidden_n3,hidden_4,hidden_n5,hidden_6,hidden_7,hidden_n8,hidden_9,hidden_10,hidden_n11,hidden_12,hidden_n13))
        popcount[:, 1] = config["popcount_1"](self.debinarize2(hidden_n0,hidden_1,hidden_n2,hidden_n3,hidden_4,hidden_n5,hidden_n6,hidden_7,hidden_n8,hidden_n9,hidden_n10,hidden_n11,hidden_n12,hidden_n13))
        # scores
        scores = 2*popcount
        
        # Compute argmax to find prediction for each feature array
        predictions = np.argmax(scores, axis=1)
        return predictions

        
def main():
    tnn = TNNBreastcancer2b()
    print(tnn.get_accurate_config())
#    return
    accuracy = tnn.get_accuracy("train");# 0 for trainset or 1 for testset
    print(f"Training: {accuracy:.2%}")

    accuracy = tnn.get_accuracy("test");# 0 for trainset or 1 for testset
    print(f"Testing: {accuracy:.2%}")
    return accuracy


if __name__ == "__main__":
    acc = main()

# %%
