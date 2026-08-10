import numpy as np
from typing import Dict, Any

from qiskit_optimization.problems import QuadraticProgram
from qiskit_optimization.algorithms import WarmStartQAOAOptimizer
from qiskit_optimization.algorithms import SlsqpOptimizer
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler as Sampler


def formulate_qubo(config: Dict[str, Any]) -> QuadraticProgram:
    """
    Formulate a discrete version of the battery optimization problem as a QUBO.
    Uses categorical variables from the config to define binary variables.
    """
    qp = QuadraticProgram(name="EV_Battery_Optimization")
    
    variables = config.get("optimization", {}).get("variables", {})
    
    # Extract discrete variables (lists of strings)
    discrete_vars = {}
    for var_name, options in variables.items():
        if isinstance(options, list) and len(options) > 0 and isinstance(options[0], str):
            discrete_vars[var_name] = options
            
    # Add binary variables for each categorical option (One-hot encoding)
    for var_name, options in discrete_vars.items():
        for opt in options:
            var_id = f"{var_name}_{opt}"
            # Sanitize variable name for qiskit
            var_id = var_id.replace("-", "_")
            qp.binary_var(name=var_id)
            
    # Add constraint: exactly one option selected per categorical variable
    for var_name, options in discrete_vars.items():
        var_names = [f"{var_name}_{opt}".replace("-", "_") for opt in options]
        qp.linear_constraint(linear={v: 1 for v in var_names}, sense='==', rhs=1, name=f"one_hot_{var_name}")
        
    # Mock objective: minimize a random quadratic/linear cost based on variable correlations
    # In a real scenario, this would come from a surrogate model or empirical data
    np.random.seed(42)
    linear_obj = {v.name: np.random.uniform(-1, 1) for v in qp.variables}
    qp.minimize(linear=linear_obj)
    
    return qp


class WarmStartQAOASolver:
    def __init__(self, reps: int = 2):
        self.reps = reps
        self.sampler = Sampler()
        self.optimizer = COBYLA()
        self.qaoa = QAOA(sampler=self.sampler, optimizer=self.optimizer, reps=self.reps)
        
        # Pre-solver for warm start (classical relaxation)
        self.pre_solver = SlsqpOptimizer()
        
        self.ws_qaoa = WarmStartQAOAOptimizer(
            pre_solver=self.pre_solver,
            relax_for_pre_solver=True,
            qaoa=self.qaoa,
            epsilon=0.25
        )

    def solve(self, qp: QuadraticProgram):
        print(f"Solving QUBO with {qp.get_num_vars()} variables using Warm-Started QAOA...")
        result = self.ws_qaoa.solve(qp)
        return result
