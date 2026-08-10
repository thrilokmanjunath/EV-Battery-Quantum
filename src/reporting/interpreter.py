"""
Reporting and Interpretation module for QML EV Battery Optimizer.
"""

def generate_recommendation(binary_vector: list[int], objectives: dict[str, float]) -> str:
    """
    Translates a binary parameter vector and its objective scores into plain-English
    engineering recommendations.
    
    Args:
        binary_vector: A list of 0s and 1s representing the discretized design choices.
            e.g., [Cell_Type, Cooling_System, Structural_Material, Arrangement]
        objectives: A dictionary containing the evaluated objective scores.
            e.g., {'energy_density': 250.5, 'weight': 450.2, 'thermal_stability': 0.95}
            
    Returns:
        A formatted string containing the engineering recommendation.
    """
    # Define the mapping of binary variables to engineering choices
    param_map = {
        0: {"name": "Cell Chemistry", 0: "LFP (Lithium Iron Phosphate)", 1: "NMC (Nickel Manganese Cobalt)"},
        1: {"name": "Cooling System", 0: "Passive Air Cooling", 1: "Active Liquid Cooling"},
        2: {"name": "Structural Material", 0: "Aluminum Alloy", 1: "Carbon Fiber Composite"},
        3: {"name": "Cell Arrangement", 0: "Series-dominant", 1: "Parallel-dominant"}
    }
    
    if len(binary_vector) > len(param_map):
        return "Error: Binary vector length exceeds known parameter mappings."

    recommendation = []
    recommendation.append("=== EV Battery Pack Design Recommendation ===\n")
    
    recommendation.append("Based on the Quantum Optimization results, the following configuration was selected to balance the multi-objective Pareto front:\n")
    
    for i, bit in enumerate(binary_vector):
        if i in param_map:
            param_name = param_map[i]["name"]
            choice = param_map[i][bit]
            
            # Generate the 'why' reasoning based on the choice
            reasoning = ""
            if param_name == "Cell Chemistry":
                if bit == 0:
                    reasoning = "Chosen to maximize thermal stability and longevity, despite a slight trade-off in peak energy density."
                else:
                    reasoning = "Chosen to prioritize high energy density and range, requiring robust thermal management."
            elif param_name == "Cooling System":
                if bit == 0:
                    reasoning = "Selected to minimize weight and parasitic power loss, suitable for lower-power applications or highly stable chemistries."
                else:
                    reasoning = "Selected to ensure safety and optimal operating temperatures under high-load conditions, mitigating thermal runaway risks."
            elif param_name == "Structural Material":
                if bit == 0:
                    reasoning = "Chosen for a balance of cost-effectiveness, manufacturability, and adequate structural integrity."
                else:
                    reasoning = "Chosen to aggressively minimize overall pack weight while maintaining high tensile strength, improving vehicle efficiency."
            elif param_name == "Cell Arrangement":
                if bit == 0:
                    reasoning = "Prioritized to achieve higher voltage levels required for high-performance traction motors."
                else:
                    reasoning = "Prioritized for increased capacity and redundancy, improving fault tolerance within the pack."
                    
            recommendation.append(f"- **{param_name}**: {choice}")
            recommendation.append(f"  *Reasoning*: {reasoning}")
    
    recommendation.append("\n--- Achieved Objectives ---")
    for obj_name, value in objectives.items():
        recommendation.append(f"- {obj_name.replace('_', ' ').title()}: {value:.2f}")
        
    recommendation.append("\n*Note: This configuration lies on the QML-derived Pareto frontier, representing an optimal trade-off in the high-dimensional design space.*")
    
    return "\n".join(recommendation)

if __name__ == "__main__":
    # Example usage
    sample_vector = [1, 1, 0, 0] # NMC, Liquid Cooling, Aluminum, Series
    sample_objectives = {"energy_density_wh_kg": 265.0, "total_weight_kg": 420.5, "thermal_safety_index": 0.88}
    print(generate_recommendation(sample_vector, sample_objectives))
