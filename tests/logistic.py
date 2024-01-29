import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

# Load and preprocess data (replace with your actual data loading and feature engineering)
data = pd.read_csv("your_data.csv")
X = data[["income", "employment_status", "transactional_features", "social_features"]]  # Replace with actual features
y = data["purchase_limit"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling (if necessary)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# One-hot encoding categorical features (if applicable)
encoder = OneHotEncoder(handle_unknown="ignore")
categorical_feature_indices = [1, 2]  # Replace with the actual indices of categorical features
X_train_encoded = encoder.fit_transform(X_train_scaled[:, categorical_feature_indices])
X_test_encoded = encoder.transform(X_test_scaled[:, categorical_feature_indices])

# Train model
model = RandomForestRegressor(n_estimators=100, max_depth=5)
model.fit(X_train_encoded, y_train)

# Evaluate model performance (e.g., using R-squared, mean squared error)
predictions = model.predict(X_test_encoded)
# ... (evaluate performance metrics)

# Use the model for credit scoring and purchase limit prediction
def predict_purchase_limit(new_data):
    # Preprocess new data and get relevant features
    new_data_scaled = scaler.transform(new_data)
    new_data_encoded = encoder.transform(new_data_scaled[:, categorical_feature_indices])
    predicted_limit = model.predict(new_data_encoded)[0]
    # Ensure limit doesn't exceed 30% of income
    return min(predicted_limit, 0.3 * new_data["income"])

# Integrate with your BNPL application and dashboard
# ...
