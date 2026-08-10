import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score
import time
import pickle

from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit_algorithms.optimizers import COBYLA
from qiskit_machine_learning.algorithms.classifiers import VQC
from qiskit_aer.primitives import Sampler
from qiskit_aer import AerSimulator

def train_and_evaluate(data_dir="datasets", model_dir="models", sample_size=200):
    """
    Train VQC and classical baselines (SVM, MLP) to predict if a battery configuration
    achieves 'better than median' performance for each objective.
    We use a subset of data (sample_size) due to quantum simulation time limits.
    """
    os.makedirs(model_dir, exist_ok=True)
    
    # Load PCA features (6 components) and scaled objectives
    X = pd.read_csv(f"{data_dir}/X_pca.csv").values[:sample_size]
    Y_raw = pd.read_csv(f"{data_dir}/Y_scaled.csv").values[:sample_size]
    
    # Binarize objectives (1 if better than median, 0 if worse)
    # Objectives to maximize: capacity, cooling_efficiency, safety_score, charging_efficiency
    # Objectives to minimize: weight, manufacturing_cost
    Y = np.zeros_like(Y_raw)
    for i in range(Y_raw.shape[1]):
        median_val = np.median(Y_raw[:, i])
        if i in [0, 4]: # minimize weight (0) and cost (4)
            Y[:, i] = (Y_raw[:, i] <= median_val).astype(int)
        else: # maximize others
            Y[:, i] = (Y_raw[:, i] > median_val).astype(int)
            
    num_features = X.shape[1] # Should be 6
    print(f"Dataset loaded. Features: {num_features}, Samples: {sample_size}")
    
    # Quantum setup: Angle Encoding (using Pauli Z or ZZFeatureMap) and Hardware Efficient Ansatz
    feature_map = ZZFeatureMap(feature_dimension=num_features, reps=1)
    ansatz = RealAmplitudes(num_qubits=num_features, reps=2)
    optimizer = COBYLA(maxiter=50) # Keep low for simulation feasibility
    sampler = Sampler() # Uses AerSimulator implicitly in Qiskit Aer
    
    results = {}
    
    # We will train a model for each objective
    objective_names = ['weight', 'capacity', 'cooling', 'safety', 'cost', 'charging']
    
    for i, obj_name in enumerate(objective_names):
        print(f"\n--- Training models for Objective: {obj_name} ---")
        y_obj = Y[:, i]
        
        # Format labels for VQC (one-hot encoding required by some VQC implementations)
        # Using binary labels directly with NeuralNetworkClassifier or two classes VQC
        
        X_train, X_test, y_train, y_test = train_test_split(X, y_obj, test_size=0.2, random_state=42)
        
        # 1. Classical Baseline: SVM
        start_time = time.time()
        svm = SVC(probability=True, kernel='rbf')
        svm.fit(X_train, y_train)
        svm_preds = svm.predict(X_test)
        svm_time = time.time() - start_time
        svm_acc = accuracy_score(y_test, svm_preds)
        print(f"SVM - Acc: {svm_acc:.4f}, Time: {svm_time:.2f}s")
        
        # 2. Classical Baseline: MLP
        start_time = time.time()
        mlp = MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=200, random_state=42)
        mlp.fit(X_train, y_train)
        mlp_preds = mlp.predict(X_test)
        mlp_time = time.time() - start_time
        mlp_acc = accuracy_score(y_test, mlp_preds)
        print(f"MLP - Acc: {mlp_acc:.4f}, Time: {mlp_time:.2f}s")
        
        # 3. Quantum VQC
        start_time = time.time()
        # VQC needs one-hot labels for classification
        y_train_oh = np.zeros((y_train.size, 2))
        y_train_oh[np.arange(y_train.size), y_train.astype(int)] = 1
        
        vqc = VQC(
            feature_map=feature_map,
            ansatz=ansatz,
            optimizer=optimizer
        )
        vqc.fit(X_train, y_train_oh)
        
        # Predict returns one-hot, convert to class index
        vqc_preds_oh = vqc.predict(X_test)
        vqc_preds = np.argmax(vqc_preds_oh, axis=1)
        vqc_time = time.time() - start_time
        vqc_acc = accuracy_score(y_test, vqc_preds)
        print(f"VQC - Acc: {vqc_acc:.4f}, Time: {vqc_time:.2f}s")
        
        results[obj_name] = {
            'SVM': {'acc': svm_acc, 'time': svm_time, 'model': svm},
            'MLP': {'acc': mlp_acc, 'time': mlp_time, 'model': mlp},
            'VQC': {'acc': vqc_acc, 'time': vqc_time, 'model': vqc}
        }
        
    # Save the classical models for the QAOA stage (VQC is hard to save/load cleanly in quick scripts, 
    # but we can use SVM as a proxy for QAOA cost landscape to save simulation time, or we can use 
    # the trained VQC directly if we combine the scripts. For now, we save classical).
    with open(f"{model_dir}/classical_models.pkl", 'wb') as f:
        # Save only SVM and MLP to avoid qiskit serialization issues
        safe_results = {k: {m: v for m, v in models.items() if m != 'VQC'} for k, models in results.items()}
        pickle.dump(safe_results, f)

    print("\n--- Summary Benchmarking ---")
    print(f"{'Objective':<15} | {'SVM Acc':<10} | {'MLP Acc':<10} | {'VQC Acc':<10}")
    for obj in objective_names:
        print(f"{obj:<15} | {results[obj]['SVM']['acc']:<10.4f} | {results[obj]['MLP']['acc']:<10.4f} | {results[obj]['VQC']['acc']:<10.4f}")

if __name__ == "__main__":
    train_and_evaluate()
