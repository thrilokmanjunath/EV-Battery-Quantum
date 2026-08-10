"""
Quantum Kernel Support Vector Machine (QKSVM) for EV Battery data.
"""
from sklearn.svm import SVC
from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_algorithms.state_fidelities import ComputeUncompute
from qiskit.primitives import StatevectorSampler as Sampler

class QKSVMModel:
    def __init__(self, num_features, entanglement='linear'):
        """
        Initialize the Quantum Kernel Support Vector Machine.
        
        Args:
            num_features (int): Number of features (dimensions) of the input data (e.g. 6-10 after PCA).
            entanglement (str): Entanglement strategy for the ZZFeatureMap.
        """
        self.num_features = num_features
        # Create a feature map (using ZZFeatureMap)
        self.feature_map = ZZFeatureMap(feature_dimension=num_features, reps=2, entanglement=entanglement)
        
        # Instantiate a sampler
        self.sampler = Sampler()
        
        # Compute fidelity
        self.fidelity = ComputeUncompute(sampler=self.sampler)
        
        # Instantiate quantum kernel
        self.qkernel = FidelityQuantumKernel(fidelity=self.fidelity, feature_map=self.feature_map)
        
        # Instantiate SVC
        self.svc = SVC(kernel=self.qkernel.evaluate)

    def fit(self, X_train, y_train):
        """
        Fit the QKSVM model.
        """
        self.svc.fit(X_train, y_train)

    def predict(self, X_test):
        """
        Predict using the QKSVM model.
        """
        return self.svc.predict(X_test)
        
    def score(self, X_test, y_test):
        """
        Calculate the accuracy of the QKSVM model.
        """
        return self.svc.score(X_test, y_test)
