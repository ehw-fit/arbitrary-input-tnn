#%%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
# %%
df = pd.read_pickle("../neural-network/designs/analyze.pkl.gz")
df
# %%
import os, sys

from ariths_gen.multi_bit_circuits.others import (
    PopCountCompare, UnsignedPopCount
)

import ariths_gen.multi_bit_circuits.subtractors as agsub
import ariths_gen.multi_bit_circuits.adders as agadd
import ariths_gen.multi_bit_circuits.others as agoth
import ariths_gen.core.arithmetic_circuits as agcoreac
import ariths_gen.one_bit_circuits.logic_gates as agonebit

from ariths_gen.wire_components import (
    Bus, ConstantWireValue0, ConstantWireValue1
)
# %%

class MultibitSum(agcoreac.GeneralCircuit):
    def __init__(self, bits, cnf, prefix="", name="mbs", 
                 adder_cls = None, adder_kws = {}, 
                 sub_cls = None, sub_kws = {},
                 **kwargs):
        
        self.bits = bits
        self.cnf = cnf

        if not adder_cls:
            adder_cls = agadd.SignedRippleCarryAdder
        
        if not sub_cls:
            sub_cls = agsub.SignedRippleCarrySubtractor
        
        
        positions = [Bus(prefix=f"input_{i}", N=bits) for i in range(len(cnf))]

        out_N = bits + int(np.ceil(np.log2(len(cnf))))
        super().__init__(prefix=prefix, 
                         out_N=out_N, name=name, 
                         inputs=positions, 
                         signed_out=True,
                         **kwargs)

        self.circ_id = 0
        def recursive_create(bit, cnf, positions):
            if len(cnf) == 1:
                return positions[0], cnf == "+"
                return f"({positions[0]})", cnf == "+"
            
            if len(cnf) == 2:
                self.circ_id += 1
                if cnf == "++":
                    circ = self.add_component(
                        adder_cls(positions[0], positions[1], prefix=f"{self.prefix}_adder_{self.circ_id}", **adder_kws)                        
                    )
                    return circ.out, True
                    return f"({positions[0]} + {positions[1]})", True
                
                elif cnf == "+-":
                    circ = self.add_component(
                        sub_cls(positions[0], positions[1], prefix=f"{self.prefix}_subtractor_{self.circ_id}", **sub_kws)
                    )
                    return circ.out, True

                    return f"({positions[0]} - {positions[1]})", True
                elif cnf == "-+":
                    circ = self.add_component(
                        sub_cls(positions[1], positions[0], prefix=f"{self.prefix}_subtractor_{self.circ_id}",  **sub_kws)
                    )
                    return circ.out, True
                    return f"({positions[1]} - {positions[0]})", True
                elif cnf == "--":
                    circ = self.add_component(
                        adder_cls(positions[0], positions[1], prefix=f"{self.prefix}_adder_{self.circ_id}", **adder_kws)                        
                    )
                    return circ.out, False
                    return f"({positions[0]} + {positions[1]})", False
                else:
                    raise ValueError(f"Invalid CNF: {cnf}")


            half = len(cnf) // 2
            left = cnf[:half]
            right = cnf[half:]
            left_positions = positions[:half]
            right_positions = positions[half:]

            left_expr, left_sign = recursive_create(bit, left, left_positions)
            right_expr, right_sign = recursive_create(bit, right, right_positions)


            self.circ_id += 1
            if left_sign and right_sign:
                circ = self.add_component(
                    adder_cls(left_expr, right_expr, prefix=f"{self.prefix}_adder_{self.circ_id}", **adder_kws)                        
                )
                return circ.out, True

                return f"({left_expr} + {right_expr})", True
            elif left_sign and not right_sign:
                circ = self.add_component(
                    sub_cls(left_expr, right_expr, prefix=f"{self.prefix}_subtractor_{self.circ_id}", **sub_kws)
                )
                return circ.out, True
            
                return f"({left_expr} - {right_expr})", True
            elif not left_sign and right_sign:
                circ = self.add_component(
                    sub_cls(right_expr, left_expr, prefix=f"{self.prefix}_subtractor_{self.circ_id}", **sub_kws)
                )
                return circ.out, True
                return f"({right_expr} - {left_expr})", True
            elif not left_sign and not right_sign:
                circ = self.add_component(
                    adder_cls(left_expr, right_expr, prefix=f"{self.prefix}_adder_{self.circ_id}", **adder_kws)                        
                )
                return circ.out, False
                return f"({left_expr} + {right_expr})", False
            else:
                raise ValueError(f"Invalid CNF: {cnf}")
        
        # create new bus extended by 1 bit
        pos_extend = []
        for i, b in enumerate(positions):
            be = Bus(prefix=f"input_{i}_ext", N=bits + 1)
            for j in range(bits):
                be[j] = b[j]
            be[bits] = ConstantWireValue0()
            pos_extend.append(be)
        
        expr, sign = recursive_create(bits, cnf, pos_extend)
        print(expr, sign)
        assert sign, "Only positive comparison is supported"
        self.out.connect_bus(expr)
        


#mb = MultibitSumCompare(4, "-+-+-+--")
mb = MultibitSum(4, "-+--")

mb.get_v_code_hier(open("mbsc.v", "w"))
mb.get_python_code_flat(open("mbsc.py", "w"))
mb.get_cgp_code_flat(open("mbsc.cgp", "w"))
print(mb.get_parameters_cgp())
print(0,  mb(0, 0, 0, 2))
print(1,  mb(0, 1, 0, 0))
print(-1,  mb(0, 0, 0, 1))
print(0,  mb(0, np.array([0, 1, 0]), 0, np.array([0, 0, 1])))

#mb(2,8,2,5)
mb(0, 8, 0, 0)
#%%
class MultibitSumCompare(agcoreac.GeneralCircuit):
    def __init__(self, bits, cnf, prefix="", name="mbsc", 
                 mbs_kws = {}, **kwargs):
        self.bits = bits
        positions = [Bus(prefix=f"input_{i}", N=bits) for i in range(len(cnf))]

        out_N = 1
        super().__init__(prefix=prefix, 
                         out_N=out_N, name=name, 
                         inputs=positions, 
                         signed_out=False,
                         **kwargs)
        mbs = self.add_component(MultibitSum(bits, cnf, prefix=f"{self.prefix}_mbs", **mbs_kws))
        n = self.add_component(agonebit.NotGate(mbs.out[-1], prefix=f"{self.prefix}_not"))
        self.out.connect(0, n.out)

mb = MultibitSumCompare(4, "-+--")

mb.get_v_code_hier(open("mbsc.v", "w"))
mb.get_python_code_flat(open("mbsc.py", "w"))
print(mb.get_parameters_cgp())
print(0,  mb(0, 0, 0, 0))
print(1,  mb(0, 1, 0, 0))
print(-1,  mb(0, 0, 0, 1))
#%%%
from typing import List
class SumTree(agcoreac.GeneralCircuit):
    def __init__(self, inputs : List[Bus], prefix="", name="sumtree", add_cls=None, **kwargs):
        self.inputs = inputs
        bw = max([i.N for i in inputs])
        out_N = bw + int(np.ceil(np.log2(len(inputs))))
        super().__init__(prefix=prefix, 
                         out_N=out_N, name=name, 
                         inputs=inputs, 
                         signed_out=False,
                         **kwargs)
        
        if not add_cls:
            add_cls = agadd.UnsignedRippleCarryAdder

        self.circ_id = 0
        

        def recursive_create(inputs):
            if len(inputs) == 1:
                b = Bus(N=bw, prefix=f"{self.prefix}_input_{self.circ_id}", wires_list=inputs[0].bus)
                return b
            if len(inputs) == 2:
                self.circ_id += 1
                circ = self.add_component(
                    add_cls(inputs[0], inputs[1], prefix=f"{self.prefix}_adder_{self.circ_id}")
                )
                return circ.out
            
            half = len(inputs) // 2
            left = inputs[:half]
            right = inputs[half:]

            left_expr = recursive_create(left)
            right_expr = recursive_create(right)

            self.circ_id += 1
            circ = self.add_component(
                add_cls(left_expr, right_expr, prefix=f"{self.prefix}_adder_{self.circ_id}")
            )
            return circ.out
        
        expr = recursive_create(inputs)
        self.out.connect_bus(expr)


st = SumTree([Bus(N=4, prefix=f"input_{i}") for i in range(5)])
st.get_v_code_hier(open("st.v", "w"))
st.get_v_code_hier(open("st.v", "w"))

print(st.get_parameters_cgp())
st(15, 0, 0, 0, 0)


#%%%
class MultibitSumTreeCompare(agcoreac.GeneralCircuit):
    def __init__(self, bits, cnf, prefix="", name="mstc",
                 tree_kws={}, **kwargs):
        self.bits = bits
        positions = [Bus(prefix=f"input_{i}", N=bits) for i in range(len(cnf))]
        out_N = 1
        super().__init__(prefix=prefix, 
                         out_N=out_N, name=name, 
                         inputs=positions, 
                         signed_out=False,
                         **kwargs)
        
        positive_positions = [i for i, s in zip(positions, cnf) if s == "+"]
        negative_positions = [i for i, s in zip(positions, cnf) if s == "-"]

        
        pos_cnt = self.add_component(SumTree(positive_positions, prefix=f"{self.prefix}_pos", inner_component=True, **tree_kws))
        neg_cnt = self.add_component(SumTree(negative_positions, prefix=f"{self.prefix}_neg", inner_component=True, **tree_kws))


        pos_bus = pos_cnt.out
        neg_bus = neg_cnt.out

        for i in range(pos_bus.N):
            if pos_bus[i].is_buswire():
                #pass
                pos_bus[i].prefix = pos_bus.prefix
        #if pos_bus.parent_bus:
        #    pos_bus = pos_bus.parent_bus



        
        #print(pos_bus[3].get_wire_value_c_flat())
        self.pos_bus = pos_bus
        #if neg_bus.parent_bus:
        #    neg_bus = neg_bus.parent_bus

        #pos_cnt.out.bus_extend(N=N)
        #neg_cnt.out.bus_extend(N=N)
        cmp = self.add_component(
            agoth.UnsignedCompareGTE(pos_bus, neg_bus, 
                                     prefix=f"{self.prefix}_cmp", 
                                     inner_component=True)
        )
        self.out.connect_bus(cmp.out)

        # bug in prefixes
        for i, p in enumerate(positions):
            p.prefix = f"input_{i}"
    
mb = MultibitSumTreeCompare(4, "-+--")

mb.get_v_code_flat(open("mbsc.v", "w"))
mb.get_python_code_flat(open("mbsc.py", "w"))
print(mb.get_parameters_cgp())
print(0,  mb(0, 0, 0, 0  ))
print(1,  mb(0, 1, 0, 0 ))
print(-1,  mb(0, 0, 0, 1 ))

#%%
mb = MultibitSum(4, "-++--+--+-+")
p = np.array([[3, 2, 3, 3, 2, 3, 0, 3, 1, 2, 3, 2, 3, 1, 3, 0],
       [3, 2, 2, 3, 0, 3, 3, 2, 3, 0, 1, 1, 2, 2, 3, 3],
       [3, 2, 3, 3, 3, 3, 1, 3, 0, 2, 2, 2, 3, 1, 3, 0],
       [3, 2, 3, 3, 2, 3, 2, 3, 3, 1, 2, 0, 0, 1, 2, 2],
       [3, 2, 3, 3, 0, 3, 1, 2, 3, 1, 0, 0, 1, 2, 3, 3],
       [3, 2, 3, 3, 0, 3, 1, 2, 3, 1, 2, 0, 2, 2, 3, 3],
       [3, 2, 3, 3, 2, 3, 2, 3, 3, 2, 3, 1, 2, 0, 0, 0],
       [3, 2, 3, 3, 0, 3, 2, 2, 3, 0, 0, 0, 1, 2, 3, 3],
       [3, 2, 3, 3, 3, 3, 3, 2, 3, 2, 3, 0, 2, 0, 0, 0],
       [3, 2, 3, 3, 0, 3, 1, 2, 3, 0, 0, 0, 0, 2, 3, 3],
       [3, 2, 2, 3, 0, 3, 3, 1, 3, 0, 0, 1, 2, 2, 3, 3],
       [3, 2, 3, 3, 0, 3, 3, 2, 3, 0, 0, 1, 2, 2, 3, 3]])

mb(*[3, 2, 3, 3, 2, 3, 0, 3, 1, 2, 3, 2, 3, 1, 3, 0])

#%%
# 4-bit
parsedCMP = []
multibit_datasets = ["breastcancer4b", "redwine4b", "whitewine4b", "cardio4b", "pendigits4b"]
multibit_datasets = ["pendigits_4b"]
multibit_datasets = ["pendigits4b_v2"]
for i, row in df.query("dataset in @multibit_datasets").iterrows():
    cnf = "".join(x for x,_ in row.features)
    print(row)
    print(cnf)

    mbs = MultibitSum(4, cnf)
    mbsc = MultibitSumCompare(4, cnf)
    mbstc = MultibitSumTreeCompare(4, cnf)

    mbs.get_cgp_code_flat(open(f"mbsc4b/{row.uname}_mbs.cgp", "w"))
    open(f"mbsc4b/{row.uname}_conf.txt", "w").write(cnf)
    row.to_json(open(f"mbsc4b/{row.uname}.json", "w"), indent=2)
    mbsc.get_cgp_code_flat(open(f"mbsc4b/{row.uname}_mbsc.cgp", "w"))
    mbstc.get_cgp_code_flat(open(f"mbsc4b/{row.uname}_mbstc.cgp", "w"))
    mbstc.get_v_code_flat(open(f"mbsc4b/{row.uname}_mbstc.v", "w"))
    


#%%
# 3-bit
parsedCMP = []
multibit_datasets = ["breastcancer3b", "cardio3b", "whitewine3b", "redwine3b", "vertebral3b", "pendigits3b"]
multibit_datasets = ["pendigits3b_v2"]
multibit_datasets = ["whitewine3b_v2"]
for i, row in df.query("dataset in @multibit_datasets").iterrows():
    cnf = "".join(x for x,_ in row.features)
    print(row)
    print(cnf)

    mbs = MultibitSum(3, cnf)
    mbsc = MultibitSumCompare(3, cnf)
    mbstc = MultibitSumTreeCompare(3, cnf)

    mbs.get_cgp_code_flat(open(f"mbsc3b/{row.uname}_mbs.cgp", "w"))
    open(f"mbsc3b/{row.uname}_conf.txt", "w").write(cnf)
    row.to_json(open(f"mbsc3b/{row.uname}.json", "w"), indent=2)
    mbsc.get_cgp_code_flat(open(f"mbsc3b/{row.uname}_mbsc.cgp", "w"))
    mbstc.get_cgp_code_flat(open(f"mbsc3b/{row.uname}_mbstc.cgp", "w"))
    mbstc.get_v_code_flat(open(f"mbsc3b/{row.uname}_mbstc.v", "w"))
#%%%
# 2-bit versions
parsedCMP = []

multibit_datasets = ["breastcancer2b", "redwine2b", "vertebral2b", "seeds2b"]
multibit_datasets += ["pendigits", "cardio2b", "whitewine2b"]
multibit_datasets = ["pendigits2b"]
multibit_datasets = [ "arrhythmia2b_v2", "arrhythmia2b_v1", "vertebral2b_v2" ]
for i, row in df.query("dataset in @multibit_datasets").iterrows():
    cnf = "".join(x for x,_ in row.features)
    print(row)
    print(cnf)

    mbs = MultibitSum(2, cnf)
    mbsc = MultibitSumCompare(2, cnf)
    mbstc = MultibitSumTreeCompare(2, cnf)

    mbs.get_cgp_code_flat(open(f"mbsc2b/{row.uname}_mbs.cgp", "w"))
    open(f"mbsc2b/{row.uname}_conf.txt", "w").write(cnf)
    row.to_json(open(f"mbsc2b/{row.uname}.json", "w"), indent=2)
    mbsc.get_cgp_code_flat(open(f"mbsc2b/{row.uname}_mbsc.cgp", "w"))
    mbstc.get_cgp_code_flat(open(f"mbsc2b/{row.uname}_mbstc.cgp", "w"))
    mbstc.get_v_code_flat(open(f"mbsc2b/{row.uname}_mbstc.v", "w"))
    


#%%%
# 1-bit versions
parsedCMP = []
onebit_datasets = ['arrhythmia', 'breastcancer', 'cardio', 'redwine', 'whitewine']
onebit_datasets += ["breastcancer1b", "pendigits1b", "seeds1b", "vertebral1b"]
onebit_datasets = ["redwine1b"]
for i, row in df.query("dataset in @onebit_datasets").iterrows():
    cnf = "".join(x for x,_ in row.features)
    print(row)
    print(cnf)

    mbs = MultibitSum(1, cnf)
    mbsc = MultibitSumCompare(1, cnf)
    mbstc = MultibitSumTreeCompare(1, cnf)

    mbs.get_cgp_code_flat(open(f"mbsc1b/{row.uname}_mbs.cgp", "w"))
    open(f"mbsc1b/{row.uname}_conf.txt", "w").write(cnf)
    row.to_json(open(f"mbsc1b/{row.uname}.json", "w"), indent=2)
    #mbsc.get_cgp_code_flat(open(f"mbsc2b/{row.uname}_mbsc.cgp", "w"))
    mbstc.get_cgp_code_flat(open(f"mbsc1b/{row.uname}_mbstc.cgp", "w"))
    mbstc.get_v_code_flat(open(f"mbsc1b/{row.uname}_mbstc.v", "w"))

# %%
mbs(1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1)
# %%
from ariths_gen.core.cgp_circuit import UnsignedCGPCircuit
mbs2 = UnsignedCGPCircuit(open("mbsc/pendigits_0_mbs.cgp", "r").read(), [4] * 10)
# %%
from ariths_gen.core.logic_gate_circuits import OneInputLogicGate
mbs.get_circuit_wires()

";".join([g.get_triplet_cgp(
            a_id=mbs.get_circuit_wire_index(g.a), out_id=mbs.get_circuit_wire_index(g.out)) if isinstance(g, OneInputLogicGate) else
                       g.get_triplet_cgp(a_id=mbs.get_circuit_wire_index(g.a), b_id=mbs.get_circuit_wire_index(g.b), out_id=mbs.get_circuit_wire_index(g.out)) for g in mbs.circuit_gates])

# %%
first = mbs.circuit_gates[0]
first
# %%
first

#%%%
mbs.get_circuit_wires()

vv = [g for g in mbs.circuit_gates if hasattr(g, "b") and mbs.get_circuit_wire_index(g.b) == 42]
vv
# %%
sel = vv[0].b
sel
#%%
sel.is_constant()
# %%
list(filter(lambda x: x[0] == vv[0].b, mbs.circuit_wires))

# %%
