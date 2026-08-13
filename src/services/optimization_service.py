import logging
from celery import shared_task
from src.optimization.qaoa_solver import formulate_qubo, WarmStartQAOASolver

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def run_optimization_task(self, params: dict) -> dict:
    """
    Celery task to execute QAOA-based optimization.
    """
    logger.info("Starting background optimization task with params: %s", params)
    
    try:
        # Step 1: Formulate the problem
        self.update_state(
            state='PROGRESS',
            meta={'current': 1, 'total': 3, 'message': 'Formulating QUBO problem...'}
        )
        qp = formulate_qubo(params)
        
        # Step 2: Solve with WarmStartQAOASolver
        self.update_state(
            state='PROGRESS',
            meta={'current': 2, 'total': 3, 'message': 'Solving with Warm-Started QAOA...'}
        )
        solver = WarmStartQAOASolver(reps=2)
        result = solver.solve(qp)
        
        # Step 3: Extract results
        self.update_state(
            state='PROGRESS',
            meta={'current': 3, 'total': 3, 'message': 'Extracting optimal parameters...'}
        )
        
        optimal_parameters = result.x.tolist() if result.x is not None else []
        cost = float(result.fval) if result.fval is not None else 0.0
        
        logger.info("Completed optimization task")
        return {
            "status": "success",
            "message": "Optimization completed successfully.",
            "result": {
                "optimal_parameters": optimal_parameters,
                "cost": cost,
                "variables": [v.name for v in qp.variables]
            }
        }
    except Exception as e:
        logger.error(f"Optimization task failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
