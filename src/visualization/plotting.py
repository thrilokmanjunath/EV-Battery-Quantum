import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from typing import List, Tuple

def plot_pareto_front(objective_1: np.ndarray, objective_2: np.ndarray, 
                      obj1_name: str, obj2_name: str, 
                      save_path: str = "docs/figures/pareto_front.png"):
    """
    Generate an IEEE-style Pareto front plot comparing two conflicting objectives.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    plt.style.use('seaborn-v0_8-paper')
    
    plt.scatter(objective_1, objective_2, c='blue', alpha=0.6, edgecolors='none', label='Simulated Designs')
    
    # Simple Pareto front extraction (assuming minimization for both to find front logic, adjust as needed)
    # For visualization, we'll plot a convex hull or highlight non-dominated points
    
    plt.title(f'Pareto Front: {obj1_name} vs {obj2_name}', fontsize=14, weight='bold')
    plt.xlabel(obj1_name, fontsize=12)
    plt.ylabel(obj2_name, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()

def plot_circuit_depth_vs_accuracy(depths: List[int], accuracies: List[float], 
                                   save_path: str = "docs/figures/depth_vs_acc.png"):
    """
    Plots the accuracy of QML models vs the circuit depth to visualize NISQ limitations.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    plt.style.use('seaborn-v0_8-paper')
    
    plt.plot(depths, accuracies, marker='o', linestyle='-', color='purple', linewidth=2)
    plt.axhline(y=0.5, color='r', linestyle='--', label='Random Guessing')
    
    plt.title('NISQ Hardware Impact: Circuit Depth vs Accuracy', fontsize=14, weight='bold')
    plt.xlabel('Circuit Depth (CNOT Gates)', fontsize=12)
    plt.ylabel('Test Accuracy', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()

def plot_confusion_matrix(cm: np.ndarray, class_names: List[str], 
                          title: str = "QKSVM Confusion Matrix",
                          save_path: str = "docs/figures/confusion_matrix.png"):
    """
    Plots a high-quality confusion matrix for QML classification.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    
    plt.title(title, fontsize=14, weight='bold')
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()

def plot_engineering_tradeoffs(corr_matrix: pd.DataFrame, 
                               save_path: str = "docs/figures/tradeoffs_heatmap.png"):
    """
    Plots a heatmap of correlations between different engineering variables and objectives.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0)
    
    plt.title('Engineering Parameter Tradeoffs (Pearson Correlation)', fontsize=14, weight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
