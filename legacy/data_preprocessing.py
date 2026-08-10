import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

def generate_synthetic_battery_data(num_samples=1000, seed=42):
    """
    Generate a synthetic dataset of EV battery configurations and their performance across 
    6 objectives. This simulates data derived from longitudinal studies like NASA PCoE and CALCE.
    
    Features (X):
    - cells_series: Number of cells in series (e.g., 96, 108, 120)
    - cells_parallel: Number of cells in parallel (e.g., 1, 2, 4)
    - chemistry: 0 (LFP), 1 (NCA), 2 (NMC)
    - cooling_type: 0 (Air), 1 (Liquid), 2 (Immersion)
    - cell_capacity_ah: Nominal cell capacity in Ah (e.g., 3.0 to 5.0)
    
    Objectives (Y):
    - weight: Total pack weight (minimize)
    - capacity: Total pack energy capacity (maximize)
    - cooling_efficiency: Thermal management performance (maximize)
    - safety_score: Derived safety rating based on chem & cooling (maximize)
    - manufacturing_cost: Total cost (minimize)
    - charging_efficiency: Fast charging capability (maximize)
    """
    np.random.seed(seed)
    
    # Generate Features
    cells_series = np.random.randint(80, 120, num_samples)
    cells_parallel = np.random.randint(1, 5, num_samples)
    chemistry = np.random.randint(0, 3, num_samples)
    cooling_type = np.random.randint(0, 3, num_samples)
    cell_capacity_ah = np.random.uniform(2.5, 5.5, num_samples)
    
    X = pd.DataFrame({
        'cells_series': cells_series,
        'cells_parallel': cells_parallel,
        'chemistry': chemistry,
        'cooling_type': cooling_type,
        'cell_capacity_ah': cell_capacity_ah
    })
    
    # Constants for simulation
    # Weights for different chemistries: LFP is heavier, NCA lighter
    chem_weight_factor = {0: 1.2, 1: 0.9, 2: 1.0}
    # Cost for chemistries: LFP cheapest, NCA expensive
    chem_cost_factor = {0: 0.8, 1: 1.3, 2: 1.1}
    # Safety for chemistries: LFP safest
    chem_safety_factor = {0: 1.5, 1: 0.8, 2: 1.0}
    # Cooling performance: Immersion best, Air worst
    cooling_eff_factor = {0: 0.5, 1: 1.0, 2: 1.5}
    cooling_cost_factor = {0: 0.2, 1: 1.0, 2: 2.0}
    cooling_weight_factor = {0: 0.1, 1: 0.5, 2: 0.8}
    
    # Generate Objectives (Y) based on Features + noise
    total_cells = cells_series * cells_parallel
    
    weight = (total_cells * 0.05 * np.vectorize(chem_weight_factor.get)(chemistry)) + \
             (total_cells * 0.01 * np.vectorize(cooling_weight_factor.get)(cooling_type)) + \
             np.random.normal(0, 2, num_samples)
             
    capacity = (total_cells * cell_capacity_ah * 3.6 / 1000) + np.random.normal(0, 1, num_samples) # kWh
    
    cooling_efficiency = np.vectorize(cooling_eff_factor.get)(cooling_type) * 100 + \
                         np.random.normal(0, 5, num_samples)
                         
    safety_score = np.vectorize(chem_safety_factor.get)(chemistry) * 50 + \
                   np.vectorize(cooling_eff_factor.get)(cooling_type) * 20 + \
                   np.random.normal(0, 5, num_samples)
                   
    manufacturing_cost = (total_cells * 2.0 * np.vectorize(chem_cost_factor.get)(chemistry)) + \
                         (1000 * np.vectorize(cooling_cost_factor.get)(cooling_type)) + \
                         np.random.normal(0, 100, num_samples)
                         
    charging_efficiency = 80 + (np.vectorize(cooling_eff_factor.get)(cooling_type) * 10) - \
                          (cells_series * 0.05) + np.random.normal(0, 2, num_samples)
                          
    Y = pd.DataFrame({
        'weight': weight,
        'capacity': capacity,
        'cooling_efficiency': cooling_efficiency,
        'safety_score': safety_score,
        'manufacturing_cost': manufacturing_cost,
        'charging_efficiency': charging_efficiency
    })
    
    return X, Y

def preprocess_and_save(data_dir="datasets", n_components=6):
    """
    Generate, preprocess (scale & PCA), and save datasets for VQC and QAOA.
    The VQC will use the PCA-reduced features (6-8 qubits).
    """
    os.makedirs(data_dir, exist_ok=True)
    X, Y = generate_synthetic_battery_data()
    
    # One-hot encode categorical variables for classical baseline fairness
    X_encoded = pd.get_dummies(X, columns=['chemistry', 'cooling_type'])
    
    # Scale features
    scaler_X = StandardScaler()
    X_scaled = scaler_X.fit_transform(X_encoded)
    
    # Scale objectives for optimization (all between 0 and 1)
    scaler_Y = MinMaxScaler()
    Y_scaled = scaler_Y.fit_transform(Y)
    
    # Dimensionality Reduction for VQC (Angle Encoding on limited qubits)
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)
    
    print(f"PCA explained variance ratio ({n_components} components): {np.sum(pca.explained_variance_ratio_):.4f}")
    
    # Save datasets
    pd.DataFrame(X_pca).to_csv(f"{data_dir}/X_pca.csv", index=False)
    pd.DataFrame(X_scaled, columns=X_encoded.columns).to_csv(f"{data_dir}/X_scaled.csv", index=False)
    pd.DataFrame(Y_scaled, columns=Y.columns).to_csv(f"{data_dir}/Y_scaled.csv", index=False)
    
    print(f"Saved preprocessed data to {data_dir}/")

if __name__ == "__main__":
    preprocess_and_save()
