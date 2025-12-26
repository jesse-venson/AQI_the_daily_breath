import pandas as pd
import numpy as np
import pickle
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score

def get_aqi_category(aqi):
    if aqi <= 100:
        return 1
    elif aqi <= 200:
        return 2
    elif aqi <= 300:
        return 3
    else:
        return 4

def get_risk_level(probability):
    if probability < 0.33:
        return "LOW"
    elif probability < 0.67:
        return "MODERATE"
    else:
        return "HIGH"

def train_models():
    print("=== MODEL TRAINING ===\n")

    df = pd.read_csv("health_risk_training.csv")
    print(f"Training on {len(df)} samples")

    feature_cols = ['age', 'aqi_category', 'gender_enc', 'income_enc', 'parent_enc', 'concern_level']
    target_cols = ['Respiratory_difficulties_binary', 'Cough_binary', 'Headache_binary', 'Missed_school_or_work_binary']

    X = df[feature_cols]
    models = {}

    for target in target_cols:
        symptom_name = target.replace('_binary', '')
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        model = XGBClassifier(
            max_depth=4,
            learning_rate=0.1,
            n_estimators=100,
            min_child_weight=3,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )

        model.fit(X_train, y_train)

        y_pred_proba = model.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')

        print(f"{symptom_name}: ROC-AUC={roc_auc:.3f}, CV={cv_scores.mean():.3f}")

        models[symptom_name] = model

    model_package = {
        'models': models,
        'feature_names': feature_cols
    }

    with open('health_risk_model.pkl', 'wb') as f:
        pickle.dump(model_package, f)

    print("\n[SUCCESS] Models saved to health_risk_model.pkl\n")
    return model_package

def predict_health_risks(age, predicted_aqi, gender_enc, parent_enc, model_package=None):
    """
    Predict health risks based on age, AQI, gender, and parent status.

    Args:
        age: User's age (1-120)
        predicted_aqi: Predicted AQI value
        gender_enc: Gender encoding (0=Female, 1=Male, 2=Other)
        parent_enc: Parent status (0=No, 1=Yes)
        model_package: Pre-loaded model package (optional)

    Returns:
        Dictionary of health risk predictions for each symptom
    """
    if model_package is None:
        with open('health_risk_model.pkl', 'rb') as f:
            model_package = pickle.load(f)

    aqi_category = get_aqi_category(predicted_aqi)

    # Model trained on 6 features: age, aqi_category, gender_enc, income_enc, parent_enc, concern_level
    # User provides: age, gender_enc, parent_enc
    # Use default values for income_enc and concern_level
    features = np.array([[
        age,              # User input
        aqi_category,     # Derived from AQI prediction
        gender_enc,       # User input (0=Female, 1=Male, 2=Other)
        2,                # income_enc: 2=Middle income (default, mode from training)
        parent_enc,       # User input (0=No, 1=Yes)
        5                 # concern_level: 5=Moderate (default, mean from training)
    ]])

    results = {}
    for symptom_name, model in model_package['models'].items():
        probability = model.predict_proba(features)[0][1]
        risk_level = get_risk_level(probability)

        results[symptom_name] = {
            'probability': float(probability),
            'risk_level': risk_level
        }

    return results

if __name__ == "__main__":
    model_package = train_models()

    print("Testing prediction:")
    test_age = 35
    test_aqi = 250
    test_gender = 1  # Male
    test_parent = 1  # Yes
    results = predict_health_risks(test_age, test_aqi, test_gender, test_parent, model_package)

    print(f"\nAge={test_age}, AQI={test_aqi}, Gender={test_gender} (Male), Parent={test_parent} (Yes)")
    for symptom, data in results.items():
        print(f"  {symptom}: {data['risk_level']} ({data['probability']:.1%})")
