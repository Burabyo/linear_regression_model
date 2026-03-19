"""
predict.py
──────────
Uses the saved best model (best_model.pkl) and scaler (scaler.pkl)
to predict a student's Math Score from a single input sample.

This script is designed to be called by the API in Task 2.

Usage:
    python predict.py
"""

import joblib
import numpy as np
import pandas as pd

# ── Load saved model and scaler ───────────────────────────────────────────────
model  = joblib.load('best_model.pkl')
scaler = joblib.load('scaler.pkl')

# ── Column order must match training data (after dropping EthnicGroup & MathScore)
FEATURE_COLUMNS = [
    'Gender',
    'ParentEduc',
    'LunchType',
    'TestPrep',
    'ParentMaritalStatus',
    'PracticeSport',
    'IsFirstChild',
    'NrSiblings',
    'TransportMeans',
    'WklyStudyHours',
    'ReadingScore',
    'WritingScore'
]

# ── Example input (already label-encoded integers) ────────────────────────────
# Replace these values with real input from your API request
sample = {
    'Gender'              : 1,    # 0 = female, 1 = male
    'ParentEduc'          : 3,    # 0-5 depending on education level
    'LunchType'           : 1,    # 0 = free/reduced, 1 = standard
    'TestPrep'            : 1,    # 0 = completed, 1 = none
    'ParentMaritalStatus' : 2,    # 0-3 depending on status
    'PracticeSport'       : 2,    # 0 = never, 1 = sometimes, 2 = regularly
    'IsFirstChild'        : 1,    # 0 = no, 1 = yes
    'NrSiblings'          : 2,    # number of siblings
    'TransportMeans'      : 1,    # 0 = private, 1 = school_bus
    'WklyStudyHours'      : 2,    # 0 = < 5, 1 = 5-10, 2 = > 10
    'ReadingScore'        : 72,   # reading exam score
    'WritingScore'        : 68    # writing exam score
}


def predict_math_score(input_dict: dict) -> float:
    """
    Takes a dictionary of feature values, scales them, and returns
    the predicted Math Score.

    Args:
        input_dict: dict with keys matching FEATURE_COLUMNS

    Returns:
        float: predicted MathScore
    """
    input_df = pd.DataFrame([input_dict], columns=FEATURE_COLUMNS)
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]
    return round(float(prediction), 2)


if __name__ == '__main__':
    predicted = predict_math_score(sample)
    print('=== Student Math Score Prediction ===')
    print(f'Input sample  : {sample}')
    print(f'Predicted Math Score: {predicted}')
