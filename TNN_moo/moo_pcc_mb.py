# %%%
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
            __file__), "../../scripts/data.pc.pareto.zero.pkl.gz")
        
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
                conf[k] = self._get_cgp_circuit("../" + c["circuit"], [c["bw"]])
                #conf["permutation"][k] = x["perm_" + k]
            else:
                area += c["egfet_area"]
                #print(c)
                cgpcirc = self._get_cgp_circuit("../" + c["circuit"], [self.bw] * self.bws[k])
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


def main(circset, tnn, bw=2, n_gen=50, res_dir=None, save_history=False):
    global res, resdir

    problem = TNNopt(tnn, bw=bw, circset=f"../../scripts_mb/pareto/{bw}b_mbstc_{circset}.pkl.gz")

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
    print("Function value: %s" % res.F)

    # export res to pickle
    problem.evaluate(res.X, return_values_of=["F", "G"])

    if res_dir is not None:
        import dill

        res2 = {}
        attrs = ["CV", "F", "G", "H", "X"]

        if save_history:
            res2["history"] = []
            for p in res.history:
                l = []
                for i, e in enumerate(p.pop):
                    j = {}
                    for a in attrs:
                        j[a] = getattr(e, a)
                    l.append(j)
                
                res2["history"].append(l)

        for a in attrs:
            res2[a] = getattr(res, a)

        import dill
        #dill.dump(res2, open(os.path.join("res/tmp", "res.pkl"), "wb"))

        dill.dump(res2, open(os.path.join(res_dir, "res.pkl"), "wb"))
        if save_history:
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(1, 1, figsize=(10, 5))

            cm = plt.get_cmap("viridis")
            # pyplot get cmap with vmin and vmax
            cm = plt.get_cmap("viridis")

            for i in np.linspace(0, len(res.history) - 1, 5, endpoint=True).astype("i"):
                F = np.array([p.F for p in res.history[i].pop])
                ax.scatter(F[:, 1], 1-F[:, 0],
                        label=f"Gen {i}", color=cm(i / n_gen))

            ax.scatter(res.F[:, 1], 1 - res.F[:, 0], s=10,
                    color="red", alpha=0.7, label="Final Pareto")
            ax.set(
                xlabel="Area",
                ylabel="Accuracy",
            )
            ax.legend()
            fig.savefig(os.path.join(res_dir, "pareto_history.png"))
            plt.close()

if __name__ == "__main__":

    if False:
        print("DEBUG VERSION!!!!")
        main("mae", tnns.TNNBreastcancer2b(), 2, 50, f"res/tmp", save_history = False)
        #main("pccoptall", tnns.TNNWhitewine1b(), 1, 50, f"res/tmp")
    else:
        import json
        to_run = json.load(open("to_run.json"))
        id_run = int(os.environ.get("ID_RUN", 1)) - 1
        if id_run >= len(to_run):
            print("ID_RUN is greater than to_run")
            exit()

        
        e, ds, bw, resdir = to_run[id_run]

        if os.path.exists(f"{resdir}/res.pkl"):
            print(f"{resdir}/res.pkl exists")

            exit()
        
        tnn = None
        tnns = {
            "cardio": tnns.TNNCardio1b,
            "breastcancer": tnns.TNNBreastcancer1b,
            "redwine": tnns.TNNRedwine1b,
            "whitewine": tnns.TNNWhitewine1b,
            "arrhythmia": tnns.TNNArrhythmia1b,
            "arrhythmia2bv1": tnns.TNNArrhythmia2bV1,
            "arrhythmia2bv2": tnns.TNNArrhythmia2bV2,
            "pendigits1b": tnns.TNNPendigits1b, 
            "pendigits2b": tnns.TNNPendigits2b,
            "pn2": tnns.TNNPenDigits2b_OLD,
            "pendigits3b": tnns.TNNPendigits3b,
            "pendigits3bv2": tnns.TNNPendigits3bV2,
            "pendigits4bv2": tnns.TNNPendigits4bV2,
            "pn4": tnns.TNNPenDigits4b,
            "cardio2b": tnns.TNNCardio2b,
            "cardio3b": tnns.TNNCardio3b,
            "cardio4b": tnns.TNNCardio4b,
            "breastcancer1b": tnns.TNNBreastcancer1b,
            "breastcancer2b": tnns.TNNBreastcancer2b,
            "breastcancer3b": tnns.TNNBreastcancer3b,
            "breastcancer4b": tnns.TNNBreastcancer4b,
            "whitewine2b": tnns.TNNWhitewine2b,
            "whitewine3b": tnns.TNNWhitewine3b,
            "whitewine3bv2": tnns.TNNWhitewine3bV2,
            "redwine1b": tnns.TNNRedwine1b,
            "redwine2b": tnns.TNNRedwine2b,
            "redwine3b": tnns.TNNRedwine3b,
            "redwine4b": tnns.TNNRedwine4b,
            "seeds1b": tnns.TNNSeeds1b,
            "seeds2b": tnns.TNNSeeds2b,
            "vertebral1b": tnns.TNNVertebral1b,
            "vertebral2b": tnns.TNNVertebral2b,
            "vertebral2bv2": tnns.TNNVertebral2bV2,
            "vertebral3b": tnns.TNNVertebral3b,
        }
        tnn = tnns[ds]

        main(e, tnn(), bw, 200, resdir, save_history = False)
        


        exit()



# %%
