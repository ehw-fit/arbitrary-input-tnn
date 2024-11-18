import numpy as np
import csv
import os
from ariths_gen.core.cgp_circuit import UnsignedCGPCircuit

class PermutationWrapper:
    def __init__(self, permutation, func):
        self.permutation = permutation
        self.func = func
    
    def __call__(self, *args, **kwargs):
        assert len(args) == len(self.permutation), f"Expected {len(self.permutation)} arguments, got {len(args)}"
        args2 = [args[i] for i in self.permutation]
        return self.func(*args2, **kwargs)

class TNNMBbase:

    def __init__(self, dataset_name, bw, packed=False, feat_cnt = 19):
        self.dataset_feature_cache = {}
        self.dataset_label_cache = {}
        self.dataset_name = dataset_name
        self.permutation = None
        self.bw = bw
        self.feat_cnt = feat_cnt
        self.load_feature_array = self.load_feature_array_packed if packed else self.load_feature_array_legacy
        
    def load_feature_array_legacy(self, filename):
        """ Each character in the file is a hex digit. """
        if filename not in self.dataset_feature_cache:
            with open(filename, 'r') as file:
                self.dataset_feature_cache[filename] = np.array([list(map(lambda x: int(x, 16), line.strip())) for line in file])

        return self.dataset_feature_cache[filename]

    def load_feature_array_packed(self, filename):
        """ Each line in the file is a hex number. """
        if filename not in self.dataset_feature_cache:
            with open(filename, 'r') as file:

                x = np.array([int(line.strip(), 16) for line in file])
               # print("filename", filename, "{:x}".format(x[0]))
                
                mask = (1 <<self.bw ) - 1
                r = []
                for i in reversed(range(self.feat_cnt)):
                 #   print("i", i, (x >> (i * self.bw) ) & mask)
                    r.append(((x >> (i * self.bw) ) & mask))

                #print("r", r[0])
                self.r = r
                self.dataset_feature_cache[filename] = np.stack(r, axis=1)
                #print(self.dataset_feature_cache[filename][0, :])

        return self.dataset_feature_cache[filename]

    def load_actual_labels(self, filename):
        if filename not in self.dataset_label_cache:
            with open(filename, newline='') as file:
                reader = csv.reader(file)
                self.dataset_label_cache[filename] = np.array([int(row[0], 16) for row in reader])  
        return self.dataset_label_cache[filename]
        
    def get_dataset_files(self, dataset):
        """
        Get the input and gold files for the specified dataset.

        Args:
            dataset (int): The dataset value, "train" or "test"

        Returns:
            tuple: A tuple containing the absolute paths of the input file and gold file.
        """
        if dataset == "train":
            inpfile = f"../final_trainsets/{self.dataset_name}_train.memh"
            goldfile = f"../gold_trainsets/{self.dataset_name}_gold.csv"
        elif dataset == "test":
            inpfile = f"../final_testsets/{self.dataset_name}_test.memh"
            goldfile = f"../gold_testsets/{self.dataset_name}_gold.csv"
        else:
            raise ValueError("Invalid dataset. Use 'train' or 'test'.")

        # make inpfile absolute path
        if not os.path.isabs(inpfile):
            inpfile = os.path.join(os.path.dirname(__file__), inpfile)
        # make goldfile absolute path
        if not os.path.isabs(goldfile):
            goldfile = os.path.join(os.path.dirname(__file__), goldfile)
        return inpfile, goldfile
    
    def load_dataset(self, dataset):
        """
        Load the specified dataset.

        Args:
            dataset (int): The dataset number. 0 for training dataset, 1 for test dataset.

        Returns:
            tuple: A tuple containing the feature array and actual labels.
        """
        inpfile, goldfile = self.get_dataset_files(dataset)
        rfeature_array = self.load_feature_array(inpfile)
        actual_labels = self.load_actual_labels(goldfile)
        return rfeature_array, actual_labels


    def debinarize(self, feature_array, permutation = None):
        mask = 1 << self.get_permutation(permutation, feature_array.shape[1]) #np.arange(feature_array.shape[1])
        r = np.dot(feature_array, mask)#.reshape(-1, 1)
        return r

    def debinarize2(self, *features, permutation=None):
        #mask = 1 << np.arange(len(features))
        res = 0 #np.zeros_like(features[0])
        for i, feature in enumerate(features):
            try:
                res += feature << i
            except ValueError as e:
                self.e_res = res
                self.e_i = i
                self.e_feature = feature
                print(f"Error at {i}")
                raise e
        return res


    def set_permutation(self, permutation):
        self.permutation = permutation

    def get_permutation(self, key, length, validate=True):
        if self.permutation is None:
            assert False, "Permutation is not set"
            return np.arange(length)
        

        perm = self.permutation[key]
        if len(perm) != length:
            raise ValueError(f"Permutation length mismatch for {key}. Expected {length}, got {len(perm)}")
        
        # test all keys are in the permutation
        if validate:
            x = np.arange(length)
            b = perm == x.reshape(-1, 1)
            if not np.all(b.sum(axis=0) == 1) or not np.all(b.sum(axis=1) == 1):
                raise ValueError(f"Permutation does not contain all keys for {key}")
        return perm

    def get_configs(self):
        raise NotImplementedError("Method get_dataset_files must be implemented by the subclass.")

    
    def get_accurate_config(self):
        conf = self.get_configs()
        return {
            **{k: self.get_accurate_mbsum(k, n) for k, n in conf["nodes"].items()},
            **{i: self.get_accurate_pc(v) for i, v in  conf["sums"].items()}, 
            #**{"permutation": {k: np.arange(v)[::-1] for k, v in conf.items()}}
            }
        
    
    def get_configs_flat(self):
        conf = self.get_configs()
        ret = {}
                
        for i, sum_ in enumerate(conf["sums"]):
            ret[f"popcount_{i}"] = sum_
        return ret

    def get_accurate_pc(self, n):
        if n == 0: return lambda x: None
        return UnsignedCGPCircuit(open(f"../../circuits/pc/popcount_{n}.cgp").read(), [n])

    def get_accurate_mbsum(self, node, coefs):
        if self.bw == 1:
            return PermutationWrapper(func = UnsignedCGPCircuit(open(f"../../circuits/mbsc1b/{node}_mbstc.cgp").read(), [1] * len(coefs)), permutation= range(len(coefs)))
        if self.bw == 2:
            return UnsignedCGPCircuit(open(f"../../circuits/mbsc2b/{node}_mbstc.cgp").read(), [2] * len(coefs))
        if self.bw == 3:
            return UnsignedCGPCircuit(open(f"../../circuits/mbsc3b/{node}_mbstc.cgp").read(), [3] * len(coefs))
        if self.bw == 4:
            return UnsignedCGPCircuit(open(f"../../circuits/mbsc4b/{node}_mbstc.cgp").read(), [4] * len(coefs))
        raise ValueError(f"Invalid bitwidth {self.bw}")
    
    def tnn(self, rfeature_array, config):
        raise NotImplementedError("Method get_dataset_files must be implemented by the subclass.")



    def get_accuracy(self, dataset, config = None):

        rfeature_array, actual_labels = self.load_dataset(dataset)

        if config is None:
            config = self.get_accurate_config()

        self.set_permutation(config["permutation"] if "permutation" in config else None)
        # Define intra arrays
        predictions = self.tnn(rfeature_array, config=config)
        # Calculate accuracy
        accuracy = np.mean(predictions == actual_labels)
        return accuracy