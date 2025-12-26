import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def calculate_aqi_from_pm25(pm25):
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500)
    ]

    for pm_low, pm_high, aqi_low, aqi_high in breakpoints:
        if pm_low <= pm25 <= pm_high:
            aqi = ((aqi_high - aqi_low) / (pm_high - pm_low)) * (pm25 - pm_low) + aqi_low
            return int(round(aqi))
    return 500

def main():
    print("=== DATA PREPARATION ===\n")

    # Load survey data
    survey_df = pd.read_csv("Cleaned_Air_Pollution.csv")
    print(f"Loaded {len(survey_df)} survey samples")

    # Convert age groups to numeric
    age_map = {
        '0 to 4': 2, '5 to 9': 7, '10 to 14': 12, '15 to 19': 17,
        '20 to 24': 22, '25 to 34': 29, '35 to 44': 39, '45 to 54': 49, '55+': 62
    }
    survey_df['age'] = survey_df['Age_group'].map(age_map)

    # Assign AQI categories based on historical distribution
    # Survey context: "High Air Pollution" means AQI > 150
    # Categories: 2 (150-200), 3 (200-300), 4 (300+)
    np.random.seed(42)
    distribution = [2, 3, 4]
    probabilities = [0.45, 0.40, 0.15]
    survey_df['aqi_category'] = np.random.choice(distribution, size=len(survey_df), p=probabilities)

    # Encode categorical features
    survey_df['gender_enc'] = LabelEncoder().fit_transform(survey_df['Gender'])
    survey_df['income_enc'] = LabelEncoder().fit_transform(survey_df['Monthly_income'])
    survey_df['parent_enc'] = LabelEncoder().fit_transform(survey_df['Parent'])

    # Create binary targets
    target_cols = ['Respiratory_difficulties', 'Cough', 'Headache', 'Missed_school_or_work ']
    for col in target_cols:
        clean_name = col.strip() + '_binary'
        survey_df[clean_name] = (survey_df[col] == 'Yes').astype(int)

    # Select final features
    feature_cols = ['age', 'aqi_category', 'gender_enc', 'income_enc', 'parent_enc', 'High_air_pollution_concern']
    target_cols_binary = ['Respiratory_difficulties_binary', 'Cough_binary', 'Headache_binary', 'Missed_school_or_work_binary']

    training_df = survey_df[feature_cols + target_cols_binary].copy()
    training_df.rename(columns={'High_air_pollution_concern': 'concern_level'}, inplace=True)

    # Save
    training_df.to_csv("health_risk_training.csv", index=False)
    print(f"Saved training data: {training_df.shape}")
    print(f"\nTarget distributions:")
    for col in target_cols_binary:
        pos_count = training_df[col].sum()
        print(f"  {col}: {pos_count} ({pos_count/len(training_df):.1%})")

    print("\n[SUCCESS] Data preparation complete!\n")

if __name__ == "__main__":
    main()
