#%%
"""
This module defines the TNNWhitewine3b class, which implements a 3-bit TNN (Threshold Neural Network) for the whitewine3b dataset.
Classes:
    TNNWhitewine3b: A class that inherits from TNNMBbase and implements the TNN for the whitewine3b dataset.
Methods:
    __init__(self):
        Initializes the TNNWhitewine3b instance with the dataset name, bit width, and packed configuration.
    get_configs(self):
        Returns a dictionary containing the configuration for the nodes and popcounts.
    tnn(self, rfeature_array, config=None):
        Computes the predictions for the given feature array based on the provided configuration.
    main():
        Main function to create an instance of TNNWhitewine3b, print the accurate configuration, and compute the accuracy for the training and testing datasets.
"""

import numpy as np
import csv
import os
from ariths_gen.core.cgp_circuit import UnsignedCGPCircuit

from tnn_mb_base import TNNMBbase

class TNNWhitewine3b(TNNMBbase):
    """
    1-bit TNN for 
    """

    def __init__(self):
        super().__init__(dataset_name="whitewine3b", bw=3, packed=True)        
    
    def get_configs(self):
        return {
            "nodes": 
{'whitewine3b_0': [-1, 1, -1], 'whitewine3b_1': [-1, 1, 1, -1, 1], 'whitewine3b_2': [1, -1], 'whitewine3b_3': [1, 1, -1, -1, -1, -1], 'whitewine3b_4': [1, -1, -1, -1, -1], 'whitewine3b_5': [1, -1, 1, -1, 1, -1], 'whitewine3b_6': [1, 1, -1], 'whitewine3b_7': [1, 1, -1, -1, -1], 'whitewine3b_8': [1, 1, -1, -1]}
,
            "sums":
    {'popcount_0': 12, 'popcount_1': 12, 'popcount_2': 12, 'popcount_3': 12, 'popcount_4': 12, 'popcount_5': 12, 'popcount_6': 12}
        }


    def tnn(self, rfeature_array, config=None):
        self.set_permutation(config["permutation"] if "permutation" in config else None)

        # Reverse the bits to align with Verilog LSB to MSB reading
        feature_array = rfeature_array[:, ::-1]

        hidden_0 = config['whitewine3b_0'](feature_array[:, 3],feature_array[:, 7],feature_array[:, 10])
        hidden_1 = config['whitewine3b_1'](feature_array[:, 0],feature_array[:, 2],feature_array[:, 6],feature_array[:, 7],feature_array[:, 9])
        hidden_2 = config['whitewine3b_2'](feature_array[:, 0],feature_array[:, 2])
        hidden_3 = config['whitewine3b_3'](feature_array[:, 1],feature_array[:, 2],feature_array[:, 3],feature_array[:, 4],feature_array[:, 9],feature_array[:, 10])
        hidden_4 = config['whitewine3b_4'](feature_array[:, 0],feature_array[:, 1],feature_array[:, 2],feature_array[:, 3],feature_array[:, 8])
        hidden_5 = config['whitewine3b_5'](feature_array[:, 0],feature_array[:, 2],feature_array[:, 4],feature_array[:, 5],feature_array[:, 6],feature_array[:, 9])
        hidden_6 = np.ones_like(hidden_0)
        hidden_7 = np.zeros_like(hidden_0)
        hidden_8 = config['whitewine3b_6'](feature_array[:, 3],feature_array[:, 6],feature_array[:, 7])
        hidden_9 = config['whitewine3b_7'](feature_array[:, 2],feature_array[:, 4],feature_array[:, 8],feature_array[:, 9],feature_array[:, 10])
        hidden_10 = np.zeros_like(hidden_0)
        hidden_11 = config['whitewine3b_8'](feature_array[:, 1],feature_array[:, 4],feature_array[:, 7],feature_array[:, 10])

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

        # Compute popcounts
        popcount = np.zeros((rfeature_array.shape[0], 7), dtype=np.uint8)  # Adjust the second dimension based on CLASS_CNT
        popcount[:, 0] = config["popcount_0"](self.debinarize2(hidden_n0,hidden_1,hidden_n2,hidden_3,hidden_4,hidden_5,hidden_n6,hidden_7,hidden_8,hidden_9,hidden_n10,hidden_11))
        popcount[:, 1] = config["popcount_1"](self.debinarize2(hidden_n0,hidden_1,hidden_n2,hidden_n3,hidden_n4,hidden_5,hidden_n6,hidden_7,hidden_8,hidden_9,hidden_n10,hidden_11))
        popcount[:, 2] = config["popcount_2"](self.debinarize2(hidden_n0,hidden_1,hidden_n2,hidden_n3,hidden_n4,hidden_5,hidden_6,hidden_n7,hidden_8,hidden_9,hidden_n10,hidden_11))
        popcount[:, 3] = config["popcount_3"](self.debinarize2(hidden_n0,hidden_1,hidden_n2,hidden_n3,hidden_n4,hidden_5,hidden_6,hidden_n7,hidden_8,hidden_9,hidden_n10,hidden_n11))
        popcount[:, 4] = config["popcount_4"](self.debinarize2(hidden_0,hidden_1,hidden_n2,hidden_n3,hidden_4,hidden_5,hidden_6,hidden_n7,hidden_8,hidden_9,hidden_n10,hidden_n11))
        popcount[:, 5] = config["popcount_5"](self.debinarize2(hidden_n0,hidden_1,hidden_n2,hidden_n3,hidden_n4,hidden_5,hidden_n6,hidden_n7,hidden_n8,hidden_9,hidden_10,hidden_n11))
        popcount[:, 6] = config["popcount_6"](self.debinarize2(hidden_n0,hidden_1,hidden_n2,hidden_3,hidden_4,hidden_5,hidden_n6,hidden_7,hidden_n8,hidden_9,hidden_10,hidden_n11))
         # scores
        scores = 2*popcount
        


        # Compute argmax to find prediction for each feature array
        predictions = np.argmax(scores, axis=1)
        return predictions

        
def main():
    tnn = TNNWhitewine3b()
    accuracy = tnn.get_accuracy("train");# 0 for trainset or 1 for testset
    print(f"Training: {accuracy:.2%}")

    accuracy = tnn.get_accuracy("test");# 0 for trainset or 1 for testset
    print(f"Testing: {accuracy:.2%}")
    return accuracy


if __name__ == "__main__":
    acc = main()
