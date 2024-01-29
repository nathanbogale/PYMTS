import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression  # Replace with your preferred model

# Load the generated data
train_df = pd.read_csv("train_data.csv")
test_df = pd.read_csv("test_data.csv")

# Ensure consistent column names
train_df.columns = train_df.columns.astype(str)
test_df.columns = test_df.columns.astype(str)

# Identify categorical columns
categorical_cols = train_df.select_dtypes(include=["object"]).columns

# Create a pipeline with preprocessing and modeling steps
pipeline = Pipeline([
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ("scaler", StandardScaler(with_mean=False)),  # Disable mean centering
    ("model", LinearRegression())
])


# Separate features (X) and target variable (y)
X_train = train_df.drop("purchase_limit", axis=1)
y_train = train_df["purchase_limit"]

X_test = test_df.drop("purchase_limit", axis=1)
y_test = test_df["purchase_limit"]

# Train the pipeline
pipeline.fit(X_train, y_train)

# Make predictions on the test set
predictions = pipeline.predict(X_test)

# Evaluate model performance (e.g., using R-squared)
print("R-squared on test set:", pipeline.score(X_test, y_test))

# Save the pipeline for future use
import joblib
joblib.dump(pipeline, "purchase_limit_pipeline.pkl")  # Replace with your desired filename
