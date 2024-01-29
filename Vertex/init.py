import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from vertexai.experiment import Experiment
from vertexai.training import ClassificationTrainingSpec

# Load the LendingClub Loan Dataset
data = pd.read_csv('lendingclub_loan_data.csv')

# Select relevant features
features = ['loan_amnt', 'dti', 'credit_score', 'emp_length']
target_column = 'loan_status'

# Data preprocessing
# Handle missing values
data['loan_amnt'].fillna(data['loan_amnt'].median(), inplace=True)

# Normalize numerical features
scaler = StandardScaler()
data[features] = scaler.fit_transform(data[features])

# Encode categorical features
encoder = OneHotEncoder(handle_unknown='ignore')
encoded_features = encoder.fit_transform(data[['loan_status']].values.reshape(-1, 1)).toarray()

# Split data into training, validation, and testing sets
X = data[features].values
y = encoded_features[:, 0]

X_train, X_val, X_test, y_train, y_val, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Create Vertex AI experiment
experiment = Experiment(name='credit_scoring_experiment')

# Define the training specification
training_spec = ClassificationTrainingSpec(
    inputs={'train': X_train, 'target': y_train},
    model='logistic_regression',
    evaluation_metrics=['accuracy', 'precision', 'recall', 'f1_score'],
    validation_data={'validation': X_val, 'target': y_val}
)

# Start the training job
job = experiment.run(training_spec)

# Monitor the training job
job.wait()

# Evaluate model performance on the testing set
y_pred = job.get_final_metric('classification_metrics').get('predict').get('classification_metrics')

print('Accuracy:', y_pred['accuracy'])
print('Precision:', y_pred['precision'])
print('Recall:', y_pred['recall'])
print('F1-score:', y_pred['f1_score'])
