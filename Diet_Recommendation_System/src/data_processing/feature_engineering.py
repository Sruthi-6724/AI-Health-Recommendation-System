import pandas as pd
import numpy as np

def create_risk_score(df):
    """
    Create composite health risk score
    """
    df_risk = df.copy()
    risk_score = 0
    
    # BMI risk
    if 'BMI' in df_risk.columns:
        bmi_risk = df_risk['BMI'].apply(lambda x: 
            0 if 18.5 <= x < 25 else 
            1 if 25 <= x < 30 else 2
        )
        risk_score += bmi_risk
    
    # Glucose risk
    if 'Glucose' in df_risk.columns:
        glucose_risk = df_risk['Glucose'].apply(lambda x:
            0 if x < 100 else 
            1 if x < 126 else 2
        )
        risk_score += glucose_risk
    
    # BP risk
    if 'BloodPressure' in df_risk.columns:
        bp_risk = df_risk['BloodPressure'].apply(lambda x:
            0 if x < 120 else 
            1 if x < 140 else 2
        )
        risk_score += bp_risk
    
    df_risk['Risk_Score'] = risk_score
    df_risk['Risk_Level'] = df_risk['Risk_Score'].apply(lambda x:
        'Low' if x <= 2 else 
        'Medium' if x <= 4 else 'High'
    )
    
    return df_risk

def create_interaction_features(df):
    """
    Create interaction features
    """
    df_interact = df.copy()
    
    # Age-BMI interaction
    if 'Age' in df_interact.columns and 'BMI' in df_interact.columns:
        df_interact['Age_BMI'] = df_interact['Age'] * df_interact['BMI']
    
    # Glucose-BMI interaction
    if 'Glucose' in df_interact.columns and 'BMI' in df_interact.columns:
        df_interact['Glucose_BMI'] = df_interact['Glucose'] * df_interact['BMI']
    
    return df_interact

def engineer_features(df):
    """
    Complete feature engineering pipeline
    """
    df_eng = df.copy()
    
    # Create risk scores
    df_eng = create_risk_score(df_eng)
    
    # Create interaction features
    df_eng = create_interaction_features(df_eng)
    
    return df_eng
