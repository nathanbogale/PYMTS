import random
import datetime
import pandas as pd
from sklearn.model_selection import train_test_split



def generate_data(num_rows=50000):
    data = []
    for _ in range(num_rows):
        monthly_salary = random.uniform(5000, 150000)  # Calculate monthly salary


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
            "monthly_salary": monthly_salary,  # Use the calculated monthly salary

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
        }
        row["purchase_limit"] = calculate_purchase_limit(row, monthly_salary)  # Pass monthly_salary to the function
        data.append(row)
    return data

def calculate_purchase_limit(row, monthly_salary):
    max_limit = monthly_salary * 0.3
    base_limit = max_limit * 0.8  # Start with 80% of max
    limit_adjustment = (
        -0.1 * row["num_of_dependents"] +  # More dependents, lower limit
        0.1 * int(row["residential_area"] == "urban") +  # Urban area, higher limit
        0.05 * (50 - abs(row["person_age"] - 50)) +  # Favor ages closer to 50
        0.1 * {"Undergraduate": 0, "Graduate": 0.2, "Masters": 0.4, "PHD": 0.6, "Academician": 0.8}[row["education_level"]] +  # Higher education, higher limit
        0.3 * (row["employment_type"] == "unemployed") +  # Unemployed, lower limit
        0.1 * {"Agriculture": 0.5, "Food, and Natural Resources": 0.6, "Aviation and Airlines": 0.8,
             "Arts, Culture and Entertainment": 0.7, "Banking, Business, Management, and Administration": 1.0,
             "Communications": 0.9, "Education and Training": 0.8, "Health and medicine": 0.9,
             "Government and Public Administration": 0.6, "Law and public policy": 0.7,
             "Marketing and Sales": 0.8, "Science and technology": 0.9}[row["employmnt_sector"]]  # Sector-specific adjustments
    )
    return max(base_limit + limit_adjustment, 0)  # Ensure non-negative limit


# Generate the data
data = generate_data()

# Convert to DataFrame
df = pd.DataFrame(data)

# Split into training and test sets (80/20 split)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)  # Set random_state for reproducibility

# Save training and test data to separate CSV files
train_df.to_csv('train_data.csv', index=False)
test_df.to_csv('test_data.csv', index=False)