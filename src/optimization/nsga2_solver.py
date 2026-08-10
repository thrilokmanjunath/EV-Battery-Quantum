import numpy as np
from typing import Dict, Any

from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination


class EVBatteryProblem(Problem):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.variables = config.get("optimization", {}).get("variables", {})
        self.continuous_vars = {}
        self.discrete_vars = {}
        
        for var_name, bounds in self.variables.items():
            if isinstance(bounds, list) and len(bounds) == 2 and isinstance(bounds[0], (int, float)):
                self.continuous_vars[var_name] = bounds
            elif isinstance(bounds, list) and isinstance(bounds[0], str):
                self.discrete_vars[var_name] = bounds

        # Determine number of variables and objectives
        n_var = len(self.continuous_vars)
        
        objectives = config.get("optimization", {}).get("objectives", {})
        self.minimize_objs = objectives.get("minimize", [])
        self.maximize_objs = objectives.get("maximize", [])
        n_obj = len(self.minimize_objs) + len(self.maximize_objs)
        
        xl = [bounds[0] for bounds in self.continuous_vars.values()]
        xu = [bounds[1] for bounds in self.continuous_vars.values()]

        super().__init__(n_var=n_var, 
                         n_obj=n_obj, 
                         n_ieq_constr=0,
                         xl=xl, 
                         xu=xu)

    def _evaluate(self, X, out, *args, **kwargs):
        # Dummy evaluation: using random synthetic functions
        # For a real implementation, this would query a physics-based simulation or surrogate model.
        n_samples = X.shape[0]
        F = np.zeros((n_samples, self.n_obj))
        
        # Synthesize objective values based on continuous variables
        for i in range(n_samples):
            x = X[i, :]
            
            idx = 0
            # Evaluate minimize objectives
            for obj in self.minimize_objs:
                # Mock function: sum of scaled variables + noise
                val = np.sum(x * np.random.uniform(0.1, 1.0, size=self.n_var))
                F[i, idx] = val
                idx += 1
                
            # Evaluate maximize objectives (pymoo minimizes by default, so we negate)
            for obj in self.maximize_objs:
                val = -np.sum(x * np.random.uniform(0.1, 1.0, size=self.n_var))
                F[i, idx] = val
                idx += 1
                
        out["F"] = F


class NSGA2Solver:
    def __init__(self, pop_size: int = 100):
        self.pop_size = pop_size
        self.algorithm = NSGA2(
            pop_size=self.pop_size,
            n_offsprings=50,
            sampling=FloatRandomSampling(),
            crossover=SBX(prob=0.9, eta=15),
            mutation=PM(eta=20),
            eliminate_duplicates=True
        )
        self.termination = get_termination("n_gen", 100)

    def solve(self, config: Dict[str, Any]):
        print("Initializing EV Battery Problem with continuous variables...")
        problem = EVBatteryProblem(config)
        print(f"Problem defined with {problem.n_var} variables and {problem.n_obj} objectives.")
        
        print("Running NSGA-II optimization...")
        res = minimize(problem,
                       self.algorithm,
                       self.termination,
                       seed=1,
                       save_history=True,
                       verbose=True)
        
        print(f"Optimization completed. Found {len(res.F)} non-dominated solutions.")
        return res
