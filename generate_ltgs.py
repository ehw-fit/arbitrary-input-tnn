

#%%%
"""
Generator of Arithmetic Tree Adders (PopCount-Compare Multibit) using ArithsGen Tool in Python
=============================================================================================
This module provides classes and functions to generate arithmetic tree adders and comparators 
using the ArithsGen tool. The main classes included are `MultibitSum`, `MultibitSumCompare`, 
`SumTree`, and `MultibitSumTreeCompare`. These classes facilitate the creation of complex 
arithmetic circuits by recursively combining simpler components such as adders and subtractors.
Classes:
--------
- MultibitSum: 
    A class to generate a multibit sum circuit based on a given configuration (CNF).
- MultibitSumCompare: 
    A class to generate a multibit sum comparator circuit that compares the sum to zero.
- SumTree: 
    A class to generate a sum tree circuit that recursively sums a list of input buses.
- MultibitSumTreeCompare: 
    A class to generate a multibit sum tree comparator circuit that compares the sum of 
    positive and negative inputs.
Usage:
------
The classes can be instantiated with specific parameters to generate the desired arithmetic 
circuits. The generated circuits can be exported to various formats such as Verilog, Python, 
and CGP (Cartesian Genetic Programming).


"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
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


# Example of generating circuits for all datasets
# of bw = 4

for uid, cnf in enumerate(["-+-+-+--", "-+--", "-+--", "-+--", "-+--"]):
    print(cnf)

    mbs = MultibitSum(4, cnf)
    mbsc = MultibitSumCompare(4, cnf)
    mbstc = MultibitSumTreeCompare(4, cnf)

    mbs.get_cgp_code_flat(open(f"mbsc4b/{uid}_mbs.cgp", "w"))
    open(f"mbsc4b/{uid}_conf.txt", "w").write(cnf)
    mbsc.get_cgp_code_flat(open(f"mbsc4b/{uid}_mbsc.cgp", "w"))
    mbstc.get_cgp_code_flat(open(f"mbsc4b/{uid}_mbstc.cgp", "w"))
    mbstc.get_v_code_flat(open(f"mbsc4b/{uid}_mbstc.v", "w"))
    

