
# %%%
"""
This module performs multiobjective optimization for assigning components from the AxLibrary to the TNNs.
It optimizes two objectives: area and accuracy drop.
Classes:
    TNNopt: Defines the optimization problem for TNNs.
Functions:
    main(tnn, bw=2, n_gen=50, res_dir=None, save_history=False): Main function to run the optimization.
TNNopt:
    __init__(self, tnn, bw, circset = "../../scripts_mb/pareto/2b_mbsc_mae.pkl.gz", **kwargs):
        Initializes the TNNopt problem with the given TNN, bit width, and circuit set.
    _get_circuit(self, ks, idx):
        Retrieves the circuit from the subset based on the key and index.
    _get_cgp_circuit(self, fn, bw):
        Retrieves or loads the CGP circuit based on the filename and bit width.
    _evaluate(self, x, out, *args, **kwargs):
        Evaluates the given solution and computes the objectives (accuracy drop and area).
main(tnn, bw=2, n_gen=50, res_dir=None, save_history=False):
    Runs the multiobjective optimization using NSGA2 algorithm.
    Plots and saves the Pareto front if res_dir is specified.
"""
import os
import numpy as np


from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.visualization.scatter import Scatter
from perm_mixed_variable import Permutation, MixedVariableSampling, PermMixedVariableMating, PermDuplicationElimination
import sys

from ariths_gen.core.cgp_circuit import UnsignedCGPCircuit
import pandas as pd

from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Choice
import tnns
from tnn_mb_base import PermutationWrapper
from tqdm.auto import tqdm

class TNNopt(ElementwiseProblem):

    def __init__(self, tnn, bw, circset = "../../scripts_mb/pareto/2b_mbsc_mae.pkl.gz", **kwargs):
        self.tnn = tnn
        self.bw = bw
        # Load circuits absolute path of "../../scripts/data.pc.pareto.zero.pkl.gz"
        circuits = os.path.join(os.path.dirname(
            __file__), "AxLibrary/popcount.pkl.gz")
        
        self.circuits_pc = pd.read_pickle(circuits)
        self.circuits_pc.set_index(self.circuits_pc.circuit, inplace=True)
        
        circuits = os.path.join(os.path.dirname(
            __file__), circset)
        self.circuits_nodes = pd.read_pickle(circuits)
        self.circuits_nodes.set_index(self.circuits_nodes.circuit, inplace=True)
        self.circuits_nodes = self.circuits_nodes[~self.circuits_nodes.index.duplicated(keep='first')] # remove duplicates
        self.subsets = {}
        self.keys = []
        self.xu = []

        vars = {}

        conf = tnn.get_configs()

        print(conf)
        self.bws = {}
        accurate = tnn.get_accurate_config()
        for node, coefs in conf["nodes"].items():
            sel = self.circuits_nodes.query(f"neuron == '{node}'").copy()


            if sel.empty:
                print(f"Empty PCC subset for {node}")
                print("current nodes", self.circuits_nodes.neuron.unique())
                #raise ValueError(f"Empty subset for {node}")
            
            self.subsets[node] = sel
            self.bws[node] = len(coefs)
            self.keys.append(node)
            vars[f"circ_{node}"] = Choice(options=sel.index.tolist())
        
        for t, b in conf["sums"].items():
            self.subsets[t] = self.circuits_pc.query(f"bw == {b}")

            if self.subsets[t].empty:
                raise ValueError(f"Empty subset for {t} with bw {b}")
            self.keys.append(t)

            #vars[f"perm_{t}"] = Permutation(b)
            vars[f"circ_{t}"] = Choice(options=self.subsets[t].index.tolist())

        self.cgp_cache = {}
        print("done")

        super().__init__(vars=vars, n_obj=2, **kwargs)

    def _get_circuit(self, ks, idx):
        return self.subsets[ks].loc[idx]

    def _get_cgp_circuit(self, fn, bw):
        if bw == 0:
            return None
        #print("Loading", fn)
        if fn in self.cgp_cache:
            return self.cgp_cache[fn]
        c = UnsignedCGPCircuit(open(fn).read(), bw)
        self.cgp_cache[fn] = c
        if len(self.cgp_cache) > 3000:
            while len(self.cgp_cache) > 2500:
                self.cgp_cache.popitem()
        return c

    def _evaluate(self, x, out, *args, **kwargs):
        assert isinstance(x, dict)
        area = 0
        conf = {"permutation": {}}

        for k in self.keys:
            c = self._get_circuit(k, x["circ_" + k])
            
            if k.startswith("popcount_"):
                area += c["egfet_area"]
                conf[k] = self._get_cgp_circuit(c["circuit"], [c["bw"]])
                #conf["permutation"][k] = x["perm_" + k]
            else:
                area += c["egfet_area"]
                #print(c)
                cgpcirc = self._get_cgp_circuit(c["circuit"], [self.bw] * self.bws[k])
                if "permutation" in c:
          #          print("Permutation found", c["permutation"])
                    conf[f"{k}"] = PermutationWrapper(func = cgpcirc, permutation = c["permutation"])
                else:
                    conf[f"{k}"] = cgpcirc



        acc = self.tnn.get_accuracy("test", conf)


        vals = [1 - acc, area]
        out["F"] = np.array(vals)
        # out["REPR"] = np.array(configs)

        # out["G"] = x[:, 0] + x[:, 1] - 10


def main(tnn, bw=2, n_gen=50, res_dir=None, save_history=False):
    global res, resdir

    problem = TNNopt(tnn, bw=bw, circset=f"AxLibrary/mbstc{bw}b.pkl.gz")

    algorithm = NSGA2(pop_size=50,
                      sampling=MixedVariableSampling(),
                      mating=PermMixedVariableMating(
                          eliminate_duplicates=PermDuplicationElimination()),
                      eliminate_duplicates=PermDuplicationElimination(),
                      )

    res = minimize(problem,
                   algorithm,
                   ('n_gen', n_gen),
                   # seed=1,
                   verbose=True, save_history=save_history)

    if res_dir is not None:
        plot = Scatter()
        plot.add(problem.pareto_front(), plot_type="line",
                 color="black", alpha=0.7)
        plot.add(res.F, facecolor="none", edgecolor="red")
        if not os.path.exists(res_dir):
            os.makedirs(res_dir, exist_ok=True)
        plot.save(os.path.join(res_dir, "pareto.png"))

    print("Best solution found: %s" % res.X)
    print("Function value: (accuracy_drop, est_area) %s" % res.F)

    # export res to pickle
    problem.evaluate(res.X, return_values_of=["F", "G"])

if __name__ == "__main__":
    main(tnns.TNNWhitewine3b(), 3, 50, f"res", save_history = False)
