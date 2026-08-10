"""
Data Re-uploading Variational Quantum Classifier (VQC) for EV Battery data.
"""
import numpy as np
from qiskit.circuit import QuantumCircuit, ParameterVector
from qiskit_machine_learning.neural_networks import SamplerQNN
from qiskit_machine_learning.algorithms.classifiers import NeuralNetworkClassifier
from qiskit.primitives import Sampler
from qiskit_algorithms.optimizers import COBYLA

class ReuploadingVQCModel:
    def __init__(self, num_features, num_reuploads=2):
        """
        Initialize the Data Re-uploading VQC Model.
        
        Args:
            num_features (int): Number of input features (PCA-reduced dimensions, e.g. 6-10).
            num_reuploads (int): Number of times the data is encoded in the circuit.
        """
        self.num_features = num_features
        self.num_reuploads = num_reuploads
        
        self.circuit = self._build_reuploading_circuit()
        self.sampler = Sampler()
        
        # Define QNN
        self.qnn = SamplerQNN(
            circuit=self.circuit,
            input_params=self.inputs,
            weight_params=self.weights,
            interpret=self._interpret,
            output_shape=2
        )
        
        self.optimizer = COBYLA(maxiter=100)
        
        self.classifier = NeuralNetworkClassifier(
            neural_network=self.qnn,
            optimizer=self.optimizer,
            callback=self._callback
        )
        self.loss_history = []

    def _build_reuploading_circuit(self):
        """
        Builds a custom Parameterized Quantum Circuit with Data Re-uploading.
        Data is repeatedly encoded followed by trainable rotations and entanglement.
        """
        qc = QuantumCircuit(self.num_features)
        
        self.inputs = ParameterVector('x', self.num_features)
        self.weights = ParameterVector('w', self.num_features * self.num_reuploads * 2) 
        
        weight_idx = 0
        for rep in range(self.num_reuploads):
            # Data encoding layer
            for i in range(self.num_features):
                qc.ry(self.inputs[i], i)
                
            # Trainable parameterized layers (Ry and Rz)
            for i in range(self.num_features):
                qc.ry(self.weights[weight_idx], i)
                weight_idx += 1
                qc.rz(self.weights[weight_idx], i)
                weight_idx += 1
                
            # Entanglement layer
            for i in range(self.num_features - 1):
                qc.cx(i, i + 1)
            # Link last qubit to first for full entanglement loop
            if self.num_features > 1:
                qc.cx(self.num_features - 1, 0)
            
        return qc

    def _interpret(self, x):
        """
        Interpretation function mapping measurement bitstrings to binary labels (0 or 1).
        Uses parity of the bitstring.
        """
        return f"{x:0b}".count("1") % 2

    def _callback(self, weights, obj_func_eval):
        """
        Callback to track objective function value during optimization.
        """
        self.loss_history.append(obj_func_eval)

    def fit(self, X_train, y_train):
        """
        Fit the VQC model to the data.
        """
        self.loss_history = []
        self.classifier.fit(X_train, y_train)
        
    def predict(self, X_test):
        """
        Predict using the VQC model.
        """
        return self.classifier.predict(X_test)
        
    def score(self, X_test, y_test):
        """
        Calculate the accuracy of the VQC model.
        """
        return self.classifier.score(X_test, y_test)
