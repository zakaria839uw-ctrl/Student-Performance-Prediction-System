import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Step 1: Load dataset
data = pd.read_csv("student_data.csv")

print("Dataset Loaded Successfully!")
print("Dataset Shape:", data.shape)
print("Columns:", data.columns.tolist())

# Step 2: Select input and output
X = data[[
    "study_hours",
    "attendance",
    "previous_marks",
    "sleep_hours"
]]

y = data["final_marks"]

# Step 3: Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Step 4: Create model
model = LinearRegression()

# Step 5: Train model
model.fit(X_train, y_train)

# Step 6: Make predictions
predictions = model.predict(X_test)
# Save Actual vs Predicted Marks

comparison = pd.DataFrame({
    "Actual Marks": y_test.values,
    "Predicted Marks": predictions
})

comparison.to_csv(
    "model_predictions.csv",
    index=False
)

print("Comparison data saved successfully!")

# Step 7: Evaluate model
mae = mean_absolute_error(y_test, predictions)

mse = mean_squared_error(y_test, predictions)

rmse = np.sqrt(mse)

r2 = r2_score(y_test, predictions)
# Step 8: Save evaluation metrics

metrics = {
    "mae": mae,
    "mse": mse,
    "rmse": rmse,
    "r2": r2
}

with open("model_metrics.pkl", "wb") as file:
    pickle.dump(metrics, file)

print("Evaluation metrics saved successfully!")

# Step 8: Display results
print("\n========== MODEL EVALUATION ==========")

print("Actual Marks:", list(y_test))
print("Predicted Marks:", predictions)

print("\nMAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r2)

# Step 9: Save trained model
with open("student_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel trained successfully!")
print("Model saved successfully!")