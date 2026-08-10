import pytest
from src.optimization.qaoa_solver import formulate_qubo
from qiskit_optimization.problems import QuadraticProgram

def test_formulate_qubo(mock_optimization_config):
    qp = formulate_qubo(mock_optimization_config)
    
    assert isinstance(qp, QuadraticProgram)
    
    # Calculate expected number of binary variables
    expected_num_vars = sum(len(opts) for opts in mock_optimization_config["optimization"]["variables"].values())
    
    # Ensure it returns discrete variables (binary)
    assert qp.get_num_vars() == expected_num_vars
    assert qp.get_num_binary_vars() == expected_num_vars
    
    # Check that linear constraints are added (one for each categorical variable)
    expected_num_constraints = len(mock_optimization_config["optimization"]["variables"])
    assert qp.get_num_linear_constraints() == expected_num_constraints
