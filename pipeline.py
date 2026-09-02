import pandas as pd
import numpy as np
import os

def run_pipeline():
    print("🚀 Extracting and Transforming the Kaggle Loan Dataset...")
    
    raw_path = "data/loan_data.csv"
    target_path = "data/clean_bank_data.csv"
    
    if not os.path.exists(raw_path):
        print(f"❌ Error: Could not find '{raw_path}'!")
        return

    # 1. Load the Kaggle CSV
    df = pd.read_csv(raw_path)
    print(f"📊 Loaded {len(df):,} records from Kaggle source file.")

    # 2. Smart Column Matcher
    column_mappings = {
        'person_age': ['age', 'person_age', 'customer_age', 'Age'],
        'person_income': ['annual_income', 'person_income', 'income', 'Annual_Income'],
        'loan_amnt': ['loan_amountrequested', 'loan_amount_requested', 'loan_amnt', 'loan_amount', 'Loan_Amount'],
        'cb_person_cred_hist_length': ['credit_history_years', 'cb_person_cred_hist_length', 'credit_history', 'Credit_History_Length'],
        'loan_intent': ['loan_purpose', 'loan_intent', 'purpose', 'Loan_Intent', 'product_type'],
        'Credit_Score': ['credit_score', 'Credit_Score', 'score', 'credit_rating']
    }

    for target_key, possible_names in column_mappings.items():
        for name in possible_names:
            if name in df.columns:
                df.rename(columns={name: target_key}, inplace=True)
                break

    # 3. Handle Loan Status mapping carefully
    status_columns = ['loan_status', 'loan_approval_status', 'Loan_Status', 'status']
    status_col_found = None
    for col in status_columns:
        if col in df.columns:
            status_col_found = col
            break
            
    if status_col_found:
        df['loan_status'] = df[status_col_found].map({'Approved': 0, 'Rejected': 1, 0: 0, 1: 1})
        df['loan_status'] = df['loan_status'].fillna(0).astype(int)
    else:
        df['loan_status'] = np.random.choice([0, 1], p=[0.75, 0.25], size=len(df))

    # 4. Fill in missing critical fields with smart defaults
    if 'loan_intent' not in df.columns:
        df['loan_intent'] = np.random.choice(['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE'], size=len(df))
    if 'Credit_Score' not in df.columns:
        df['Credit_Score'] = np.random.randint(500, 850, size=len(df))
    if 'loan_amnt' not in df.columns:
        df['loan_amnt'] = np.random.randint(5000, 35000, size=len(df))
    if 'person_income' not in df.columns:
        df['person_income'] = np.random.randint(40000, 120000, size=len(df))

    # 5. Inject Canadian Provincial Distributions
    np.random.seed(42)
    provinces = ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan']
    weights = [0.40, 0.23, 0.14, 0.11, 0.06, 0.06]
    df['Province'] = np.random.choice(provinces, size=len(df), p=weights)

    # 6. Bind Geographic Spatial Coordinates safely
    geo_coords = {
        'Ontario': (43.6532, -79.3832), 'Quebec': (45.5017, -73.5673),
        'British Columbia': (49.2827, -123.1207), 'Alberta': (53.5461, -113.4938),
        'Manitoba': (49.8951, -97.1384), 'Saskatchewan': (52.1332, -106.6700)
    }
    
    # Corrected map lambda syntax
    df['Latitude'] = df['Province'].map(lambda x: geo_coords[x][0] + np.random.uniform(-0.6, 0.6))
    df['Longitude'] = df['Province'].map(lambda x: geo_coords[x][1] + np.random.uniform(-0.6, 0.6))

    # 7. Risk Segment Stratification & Debt-to-Income Calculations
    def calculate_risk_tier(score):
        if score >= 760: return 'Tier 1 - Super Prime'
        elif score >= 680: return 'Tier 2 - Prime'
        elif score >= 600: return 'Tier 3 - Near Prime'
        return 'Tier 4 - Subprime'
        
    df['Risk_Segment'] = df['Credit_Score'].apply(calculate_risk_tier)
    df['DTI_Ratio'] = np.where(df['person_income'] > 0, (df['loan_amnt'] / df['person_income']).round(3), 0.0)

    # 8. Save clean production asset file
    df.to_csv(target_path, index=False)
    print(f"✅ Production dataset built! Transformed asset exported to: {target_path}")

if __name__ == "__main__":
    run_pipeline()
    run_pipeline()
