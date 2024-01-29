import flask
from flask import request, jsonify
import joblib

# Load the saved pipeline
pipeline = joblib.load("purchase_limit_pipeline.pkl")

app = flask.Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Ensure all required features are present
    required_features = [
        "num_dependents",
        "residential_area",
        "person_age",
        "education_level",
        "employment_type",
        "employmnt_sector",
        "monthly_salary",
        "current_balance",
        "avg_monthly_saving",
        "avg_monthly_withdrawal",
        "person_emp_length",
        "marriage_status",
        "person_home_ownership",
        "loan_intent",
        "previous_default_count",
        "recent_loan_default_amt",
        "delayed_payment_count",
        "recent_delayed_payment_amt",
        "cred_hist_avg_value",
        "emergency_contact_verified",
        "account_opened_year_month"
    ]
    if not all(feature in data for feature in required_features):
        return jsonify({"error": "Missing required features"}), 400

      # Make prediction using the pipeline
    prediction = pipeline.predict([[data[feature] for feature in required_features]])[0]
    max_purchase_limit = prediction * 5

    # Convert the results to money or ETB
    prediction_in_etb = "{:,.1f}".format(prediction * 1)  # Assuming 1 unit is equivalent to 30 ETB
    max_purchase_limit_in_etb = "{:,.1f}".format(max_purchase_limit * 1)  # Assuming 1 unit is equivalent to 30 ETB

    return jsonify({"purchase_limit": f"{prediction_in_etb} ETB", "maximum_purchase_limit": f"{max_purchase_limit_in_etb} ETB"})


if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False in production
