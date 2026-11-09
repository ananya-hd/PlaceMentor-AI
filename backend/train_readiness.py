
# ==============================================
# PlaceMentor AI - Placement Readiness Model
# Training script
# ==============================================

import numpy as np
import joblib

from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

# Reproducibility
rng = np.random.default_rng(42)

# ==============================================
# 1. GENERATE SIMULATED TRAINING DATA
# ==============================================

N = 3000

# Scores between 0 and 100
resume = rng.uniform(0, 100, N)
interview = rng.uniform(0, 100, N)
aptitude = rng.uniform(0, 100, N)

# Aptitude is optional
aptitude_taken = rng.integers(0, 2, N)

# Missing aptitude is represented by a neutral
# placeholder plus an explicit availability flag.
aptitude_input = np.where(
    aptitude_taken == 1,
    aptitude,
    50.0
)

# Demonstration readiness rubric:
# Resume 40%, Interview 40%, Aptitude 20%
#
# When aptitude is missing, redistribute weights
# equally across resume and interview.

readiness = np.where(
    aptitude_taken == 1,
    0.4 * resume + 0.4 * interview + 0.2 * aptitude,
    0.5 * resume + 0.5 * interview
)

# Small variation for demonstration purposes
readiness += rng.normal(0, 2, N)
readiness = np.clip(readiness, 0, 100)

# Model inputs:
# Resume, Interview, Aptitude, Aptitude Available
X = np.column_stack([
    resume,
    interview,
    aptitude_input,
    aptitude_taken
])

y = readiness

# ==============================================
# 2. TRAIN-TEST SPLIT
# ==============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==============================================
# 3. FEATURE SCALING
# ==============================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==============================================
# 4. BUILD MLP NEURAL NETWORK
# ==============================================

model = MLPRegressor(
    hidden_layer_sizes=(32, 16),
    activation="relu",
    solver="adam",
    learning_rate_init=0.001,
    max_iter=1000,
    early_stopping=True,
    validation_fraction=0.15,
    random_state=42
)

# ==============================================
# 5. TRAIN MODEL
# ==============================================

print("Training PlaceMentor AI readiness model...")

model.fit(X_train_scaled, y_train)

# ==============================================
# 6. EVALUATE MODEL
# ==============================================

predictions = model.predict(X_test_scaled)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\n========== MODEL RESULTS ==========")
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R2 Score: {r2:.4f}")
print(f"Training Iterations: {model.n_iter_}")
print("===================================")

print(
    "\nNOTE: Results measure performance on "
    "simulated rubric-based data, not real "
    "student placement outcomes."
)

# ==============================================
# 7. SAVE TRAINED MODEL
# ==============================================

joblib.dump(model, "readiness_model.pkl")
joblib.dump(scaler, "readiness_scaler.pkl")

print("\nModel saved successfully!")
print("readiness_model.pkl")
print("readiness_scaler.pkl")
