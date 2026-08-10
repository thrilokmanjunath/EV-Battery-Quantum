import numpy as np
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
import time
import pickle

def create_battery_qubo():
    """
    Formulate the battery pack optimization as a QUBO problem.
    To fit on near-term simulators quickly, we use 5 binary variables:
    x0, x1: Chemistry (00: LFP, 01: NCA, 10: NMC, 11: Invalid/Penalty)
    x2, x3: Cooling (00: Air, 01: Liquid, 10: Immersion, 11: Invalid/Penalty)
    x4: Pack Size (0: Standard 96s, 1: Long Range 108s)
    
    We formulate a single objective (scalarization of the 6 objectives) to minimize.
    Cost = Weight - Capacity - Cooling_Eff - Safety + Cost - Charging_Eff
    We build a simplified quadratic landscape representing these trade-offs.
    """
    qp = QuadraticProgram(name="Battery_Optimization")
    for i in range(5):
        qp.binary_var(name=f"x{i}")
        
    # Example QUBO weights simulating the trade-off surface
    # linear terms (bias)
    linear = {
        "x0": 2.0, "x1": -1.5,  # Chemistry effects
        "x2": 1.0, "x3": -2.0,  # Cooling effects
        "x4": 3.0               # Larger pack costs more but gives more capacity
    }
    
    # quadratic terms (interactions)
    # e.g., high capacity chemistry (x1=1) + large pack (x4=1) -> huge capacity but high weight/cost penalty
    quadratic = {
        ("x0", "x1"): 10.0, # Penalty for choosing 11 (Invalid chemistry)
        ("x2", "x3"): 10.0, # Penalty for choosing 11 (Invalid cooling)
        ("x1", "x3"): -3.0, # Synergistic: NCA + Immersion cooling = very good performance
        ("x1", "x4"): 2.5,  # NCA + Large Pack = High Cost penalty
        ("x2", "x4"): 1.5   # Liquid + Large Pack = Weight penalty
    }
    
    qp.minimize(linear=linear, quadratic=quadratic)
    return qp

def run_qaoa(qp):
    print("\n--- Running QAOA ---")
    start_time = time.time()
    from qiskit.primitives import StatevectorSampler
    sampler = StatevectorSampler()
    optimizer = COBYLA(maxiter=50)
    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=2)
    
    optimizer_alg = MinimumEigenOptimizer(qaoa)
    result = optimizer_alg.solve(qp)
    
    elapsed = time.time() - start_time
    print(f"QAOA Optimal Configuration: {result.x}")
    print(f"QAOA Optimal Cost: {result.fval}")
    print(f"QAOA Time: {elapsed:.2f}s")
    return result, elapsed

class BatteryProblem(Problem):
    """
    pymoo Problem definition for NSGA-II to represent the continuous
    multi-objective benchmark.
    """
    def __init__(self):
        # 5 variables (as in original continuous space):
        # cells_series (80-120), cells_parallel (1-4), chem (0-2), cool (0-2), cell_cap (2.5-5.5)
        super().__init__(n_var=5, n_obj=6, n_constr=0, xl=np.array([80, 1, 0, 0, 2.5]), xu=np.array([120, 4, 2, 2, 5.5]))

    def _evaluate(self, X, out, *args, **kwargs):
        # Vectorized evaluation matching the synthetic data generation logic
        cells_series = X[:, 0]
        cells_parallel = X[:, 1]
        chemistry = np.round(X[:, 2]).astype(int)
        cooling = np.round(X[:, 3]).astype(int)
        cell_cap = X[:, 4]
        
        total_cells = cells_series * cells_parallel
        
        # chem weights mapping
        cw = np.where(chemistry == 0, 1.2, np.where(chemistry == 1, 0.9, 1.0))
        cc = np.where(chemistry == 0, 0.8, np.where(chemistry == 1, 1.3, 1.1))
        cs = np.where(chemistry == 0, 1.5, np.where(chemistry == 1, 0.8, 1.0))
        
        cow = np.where(cooling == 0, 0.1, np.where(cooling == 1, 0.5, 0.8))
        coc = np.where(cooling == 0, 0.2, np.where(cooling == 1, 1.0, 2.0))
        coe = np.where(cooling == 0, 0.5, np.where(cooling == 1, 1.0, 1.5))

        f1 = (total_cells * 0.05 * cw) + (total_cells * 0.01 * cow) # weight (minimize)
        f2 = -(total_cells * cell_cap * 3.6 / 1000) # capacity (maximize -> minimize negative)
        f3 = -(coe * 100) # cooling eff (maximize)
        f4 = -(cs * 50 + coe * 20) # safety (maximize)
        f5 = (total_cells * 2.0 * cc) + (1000 * coc) # cost (minimize)
        f6 = -(80 + (coe * 10) - (cells_series * 0.05)) # charging eff (maximize)

        out["F"] = np.column_stack([f1, f2, f3, f4, f5, f6])

def run_nsga2():
    print("\n--- Running NSGA-II (Classical Multi-Objective Baseline) ---")
    problem = BatteryProblem()
    algorithm = NSGA2(pop_size=50)
    
    start_time = time.time()
    res = minimize(problem, algorithm, ('n_gen', 50), seed=42, verbose=False)
    elapsed = time.time() - start_time
    
    print(f"NSGA-II Pareto Front Size: {len(res.F)}")
    print(f"NSGA-II Time: {elapsed:.2f}s")
    return res, elapsed

if __name__ == "__main__":
    qp = create_battery_qubo()
    print(qp.export_as_lp_string())
    
    run_qaoa(qp)
    run_nsga2()
