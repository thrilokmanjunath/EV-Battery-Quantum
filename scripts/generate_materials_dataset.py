import pandas as pd
import numpy as np
import os

def generate_dataset(num_samples=500):
    np.random.seed(42)
    
    anodes = ["Silicon-Dominant (Si)", "Graphite", "Lithium-Metal"]
    cathodes = ["Li-Rich NMC 811", "LFP", "NCA"]
    electrolytes = ["LLZO", "Polymer", "Liquid"]
    
    # Baseline energy density contributions (Wh/kg)
    anode_energy = {
        "Graphite": 100,
        "Silicon-Dominant (Si)": 150,
        "Lithium-Metal": 200
    }
    
    cathode_energy = {
        "LFP": 120,
        "NCA": 180,
        "Li-Rich NMC 811": 210
    }
    
    # Electrolytes affect safety and slightly density
    electrolyte_energy = {
        "Liquid": 0,
        "Polymer": -10,
        "LLZO": -20  # Solid state is heavier, slightly lowers specific energy
    }
    
    data = []
    for _ in range(num_samples):
        anode = np.random.choice(anodes)
        cathode = np.random.choice(cathodes)
        electrolyte = np.random.choice(electrolytes)
        
        # Calculate base energy density
        base_density = anode_energy[anode] + cathode_energy[cathode] + electrolyte_energy[electrolyte]
        
        # Add some noise (experimental variance)
        noise = np.random.normal(0, 15)
        energy_density = base_density + noise
        
        # We also might want a binary classification label for "High Performance" (e.g., > 350 Wh/kg)
        # Because QKSVM usually does binary classification out of the box in Qiskit
        is_high_performance = 1 if energy_density > 340 else 0
        
        data.append({
            "anode": anode,
            "cathode": cathode,
            "electrolyte": electrolyte,
            "energy_density": energy_density,
            "is_high_performance": is_high_performance
        })
        
    df = pd.DataFrame(data)
    
    # Ensure datasets dir exists
    os.makedirs("datasets", exist_ok=True)
    df.to_csv("datasets/battery_materials.csv", index=False)
    print(f"Dataset with {num_samples} samples generated at datasets/battery_materials.csv")
    print("\nSample Distribution:")
    print(df['is_high_performance'].value_counts())

if __name__ == "__main__":
    generate_dataset()
