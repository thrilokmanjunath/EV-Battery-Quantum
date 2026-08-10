import sys
sys.path.append('.')
from src.optimization.qaoa_solver import formulate_qubo, WarmStartQAOASolver

config = {
    "optimization": {
        "variables": {
            "v1": ["a", "b"],
            "v2": ["x", "y"]
        }
    }
}
qp = formulate_qubo(config)
solver = WarmStartQAOASolver()
result = solver.solve(qp)
print(result)
