import random
import datetime

def generate_data(num_rows=50000):
    data = []
    for _ in range(num_rows):
        row = {
            "num_of_dependents": random.randint(0, 7),  # Follow Ethiopian household size stats
            "residential_area": random.choices(["urban", "rural"], weights=[0.212, 0.788])[0],  # Follow Ethiopian urban/rural population stats
            "person_age": random.randint(18, 80),  # Follow Ethiopian age stats
            "education_level": random.choice(["Undergraduate", "Graduate", "Masters", "PHD", "Academician"]),  # Follow Ethiopian literacy stats
            "employment_type": random.choice(["full time", "part time", "contractual", "temporary", "freelance", "unemployed"]),  # Follow Ethiopian employment stats
            "employmnt_sector": random.choice([
                "Agriculture", "Food, and Natural Resources", "Aviation and Airlines",
                "Arts, Culture and Entertainment", "Banking, Business, Management, and Administration",
                "Communications", "Education and Training", "Health and medicine",
                "Government and Public Administration", "Law and public policy",
                "Marketing and Sales", "Science and technology"
            ]),  # Adjust sector distribution as needed
            "monthly_salary": random.uniform(5000, 150000),  # Adjust salary range based on Ethiopian income levels
            "current_balance": random.uniform(0, 20000),  # Adjust based on Ethiopian bank account stats
            "avg_monthly_saving": random.uniform(0, monthly_salary * 0.4),  # Adjust based on Ethiopian savings stats
            "avg_monthly_withdrawal": random.uniform(0, monthly_salary * 0.5),  # Adjust based on Ethiopian withdrawal stats
            "person_emp_length": random.randint(1, 20),  # Follow Ethiopian job tenure stats
            "marriage_status": random.choice(["married", "divorced", "single"]),  # Follow Ethiopian marriage stats
            "person_home_ownership": random.choice(["own", "family", "mortgage", "rent"]),  # Follow Ethiopian home ownership stats
            "loan_intent": random.choice(["electronics", "furniture", "home improvement", "medical", "beauty and fashion", "others"]),  # Adjust loan purposes as needed
            "previous_default_count": 0,  # Always 0 as instructed
            "recent_loan_default_amt": 0,  # Always 0 as instructed
            "delayed_payment_count": 0,  # Always 0 as instructed
            "recent_delayed_payment_amt": 0,  # Always 0 as instructed
            "cred_hist_avg_value": random.uniform(0, 1),  # Follow Ethiopian credit score range
            "emergency_contact_verified": random.choices(["yes", "no"], weights=[0.72, 0.28])[0],  # Follow 72% yes as instructed
            "account_opened_year_month": random.choice([
                f"{year}-{month:02d}" for year in range(2017, 2024) for month in range(1, 13)
            ]),  # Follow Ethiopian bank account stats
            "purchase_limit": calculate_purchase_limit(row)  # Calculate based on other factors
        }
        data.append(row)
    return data

def calculate_purchase_limit(row):
    # Implement your purchase limit calculation logic here, considering:
    # - Maximum of 30% of monthly_salary
    # - Points from other columns affecting purchase limit
    # Example (adjust as needed):
    max_limit = row["monthly_salary"] * 0.3
    base_limit = max_limit * 0.8  # Start with 80% of max
    # Adjust based on other factors (adjust weights and logic as needed):
    limit_adjustment = (
        -0.1 * row["num_of_dependents"]  # More dependents, lower limit
        + 0.1 * int
