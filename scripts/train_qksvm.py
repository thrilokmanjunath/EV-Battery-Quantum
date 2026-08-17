import pandas as pd
import numpy as np
import pickle
import os
import sys

# Add src to path so we can import the model
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.quantum_ml.qksvm import QKSVMModel

def train_model():
    print("Loading dataset...")
    df = pd.read_csv("datasets/battery_materials.csv")
    
    # We only need a very small subset for QKSVM training locally to avoid hours of simulation
    # Ensure balanced classes
    df_high = df[df['is_high_performance'] == 1].sample(20, random_state=42)
    df_low = df[df['is_high_performance'] == 0].sample(20, random_state=42)
    df_train = pd.concat([df_high, df_low]).sample(frac=1, random_state=42)
    
    # One-hot encode the categorical variables (to match the QUBO representation)
    categories = {
        "anode": ["Silicon-Dominant (Si)", "Graphite", "Lithium-Metal"],
        "cathode": ["Li-Rich NMC 811", "LFP", "NCA"],
        "electrolyte": ["LLZO", "Polymer", "Liquid"]
    }
    
    X = []
    y = df_train['is_high_performance'].values
    
    for _, row in df_train.iterrows():
        feature_vector = []
        for cat_name, options in categories.items():
            for opt in options:
                feature_vector.append(1.0 if row[cat_name] == opt else 0.0)
        X.append(feature_vector)
        
    X = np.array(X)
    num_features = X.shape[1] # Should be 9
    
    print(f"Initializing QKSVM with {num_features} features (9 qubits)...")
    # Initialize the model
    model = QKSVMModel(num_features=num_features, entanglement='linear')
    
    print("Fitting QKSVM model... (this may take a few minutes)")
    model.fit(X, y)
    
    # Evaluate
    score = model.score(X, y)
    print(f"Training accuracy: {score * 100:.2f}%")
    
    # Extract the underlying support vector coefficients (alpha * y)
    dual_coef = model.svc.dual_coef_[0]
    # For custom kernel SVC, support_vectors_ is empty, so we must extract them using the indices
    support_indices = model.svc.support_
    support_vectors = X[support_indices]
    intercept = model.svc.intercept_[0]
    
    print("Saving model weights for QAOA QUBO construction...")
    os.makedirs("models", exist_ok=True)
    with open("models/qksvm_weights.pkl", "wb") as f:
        pickle.dump({
            "dual_coef": dual_coef,
            "support_vectors": support_vectors,
            "intercept": intercept,
            "feature_names": [f"{cat}_{opt}".replace("-", "_") for cat, opts in categories.items() for opt in opts]
        }, f)
        
    print("Training complete and weights saved to models/qksvm_weights.pkl")

if __name__ == "__main__":
    train_model()
