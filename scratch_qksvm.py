import sys
sys.path.append('.')
from src.quantum_ml.qksvm import QKSVMModel
import numpy as np

X_train = np.random.rand(10, 4)
y_train = np.random.randint(0, 2, 10)

model = QKSVMModel(num_features=4)
model.fit(X_train, y_train)
print("Score:", model.score(X_train, y_train))
