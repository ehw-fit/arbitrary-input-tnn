"""
Class for pymoo problem with mixed variables

In contrast to the baseline implementation it allows to have a permutation variable in the problem.
"""

import math
import numpy as np

from pymoo.core.infill import InfillCriterion
from pymoo.core.population import Population
from pymoo.core.individual import Individual
from pymoo.core.duplicate import ElementwiseDuplicateElimination
from pymoo.core.variable import Variable, Binary, Choice, Integer, Real
from pymoo.core.problem import Problem
from pymoo.core.crossover import Crossover
from pymoo.core.mixed import MixedVariableSampling


from pymoo.operators.selection.rnd import RandomSelection
from pymoo.operators.crossover.ux import UX
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.rm import ChoiceRandomMutation
from pymoo.operators.mutation.pm import PM
from pymoo.operators.mutation.bitflip import BFM

from pymoo.operators.repair.rounding import RoundingRepair
from random import randint


class Permutation(Variable):
    vtype = list[float]

    def __init__(self, n, **kwargs):
        super().__init__(**kwargs)
        self.n = n

    def _sample(self, n):
        return [np.random.permutation(np.arange(self.n)) for _ in range(n)]


class PermMixedVariableSampling(MixedVariableSampling):
    pass


class PermDuplicationElimination(ElementwiseDuplicateElimination):

    def is_equal(self, a, b):
        a, b = a.X, b.X
        for k, v in a.items():
            if k not in b:
                return False
            # if b[k] is numpy array and v is numpy array
            if isinstance(b[k], np.ndarray) or isinstance(v, np.ndarray):
                if not np.array_equal(b[k], v):
                    return False
            elif b[k] != v:
                return False
        return True


class SwapCrossover(Crossover):

    def __init__(self, shift=False, **kwargs):
        super().__init__(2, 2, **kwargs)
        self.shift = shift

    def _do(self, problem, X, **kwargs):
        _, n_matings, n_var = X.shape
        Y = np.full((self.n_offsprings, n_matings, n_var), -1, dtype=int)

        for i in range(n_matings):
            a, b = X[:, i, :]

            swap = randint(0, 2)

            Y[0, i, :] = a if swap == 0 else b
            Y[1, i, :] = b if swap == 0 else a

        return Y


class PermMixedVariableMating(InfillCriterion):

    def __init__(self,
                 selection=RandomSelection(),
                 crossover=None,
                 mutation=None,
                 repair=None,
                 eliminate_duplicates=True,
                 n_max_iterations=100,
                 **kwargs):

        super().__init__(repair, eliminate_duplicates, n_max_iterations, **kwargs)

        if crossover is None:
            crossover = {
                Binary: UX(),
                Real: SBX(),
                Integer: SBX(vtype=float, repair=RoundingRepair()),
                Choice: UX(),
                Permutation: SwapCrossover(),

            }

        if mutation is None:
            mutation = {
                Binary: BFM(),
                Real: PM(),
                Integer: PM(vtype=float, repair=RoundingRepair()),
                Choice: ChoiceRandomMutation(),
                Permutation: None,

            }

        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation

    def _do(self, problem, pop, n_offsprings, parents=False, **kwargs):

        # So far we assume all crossover need the same amount of parents and create the same number of offsprings
        XOVER_N_PARENTS = 2
        XOVER_N_OFFSPRINGS = 2

        # the variables with the concrete information
        vars = problem.vars

        # group all the variables by their types
        vars_by_type = {}
        for k, v in vars.items():
            clazz = type(v)

            if clazz not in vars_by_type:
                vars_by_type[clazz] = []
            vars_by_type[clazz].append(k)

        # # all different recombinations (the choices need to be split because of data types)
        recomb = []
        for clazz, list_of_vars in vars_by_type.items():
            if clazz == Choice or clazz == Permutation:
                for e in list_of_vars:
                    recomb.append((clazz, [e]))
            else:
                recomb.append((clazz, list_of_vars))

        # create an empty population that will be set in each iteration
        off = Population.new(X=[{} for _ in range(n_offsprings)])

        if not parents:
            n_select = math.ceil(n_offsprings / XOVER_N_OFFSPRINGS)
            pop = self.selection(problem, pop, n_select,
                                 XOVER_N_PARENTS, **kwargs)

        for clazz, list_of_vars in recomb:

            crossover = self.crossover[clazz]
            assert crossover.n_parents == XOVER_N_PARENTS and crossover.n_offsprings == XOVER_N_OFFSPRINGS

            if clazz == Permutation:

                _parents = [
                    [Individual(X=np.array(parent.X[list_of_vars[0]]))
                     for parent in parents]
                    for parents in pop
                ]

            else:
                _parents = [
                    [Individual(X=np.array([parent.X[var] for var in list_of_vars], dtype="O" if clazz is Choice else None))
                     for parent in parents]
                    for parents in pop
                ]

            _vars = {e: vars[e] for e in list_of_vars}
            _xl = np.array([vars[e].lb if hasattr(vars[e], "lb")
                           else None for e in list_of_vars])
            _xu = np.array([vars[e].ub if hasattr(vars[e], "ub")
                           else None for e in list_of_vars])

            if clazz == Permutation:
                assert len(list_of_vars) == 1
                _var_perm = vars[list_of_vars[0]]
                _problem = Problem(n_var=_var_perm.n, xl=_xl, xu=_xu)
            else:
                _problem = Problem(vars=_vars, xl=_xl, xu=_xu)

            _off = crossover(_problem, _parents, **kwargs)

            mutation = self.mutation[clazz]
            if mutation:
                _off = mutation(_problem, _off, **kwargs)

            for k in range(n_offsprings):
                if clazz == Permutation:
                    off[k].X[list_of_vars[0]] = _off[k].X
                else:
                    for i, name in enumerate(list_of_vars):
                        off[k].X[name] = _off[k].X[i]

        return off
