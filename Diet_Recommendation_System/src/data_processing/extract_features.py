import pandas as pd
import numpy as np

def calculate_bmi(weight, height):
    """
    Calculate BMI
    weight: kg, height: cm
    """
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def calculate_bmr(weight, height, age, gender):
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
    """
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    return round(bmr, 2)

def calculate_tdee(bmr, activity_level):
    """
    Calculate Total Daily Energy Expenditure
    """
    activity_multipliers = {
        'Sedentary': 1.2,
        'Lightly Active': 1.375,
        'Moderately Active': 1.55,
        'Very Active': 1.725,
        'Extremely Active': 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.2)
    tdee = bmr * multiplier
    
    return round(tdee, 2)

def classify_bmi(bmi):
    """
    Classify BMI category
    """
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Normal'
    elif bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

def classify_blood_pressure(systolic, diastolic):
    """
    Classify blood pressure
    """
    if systolic < 120 and diastolic < 80:
        return 'Normal'
    elif systolic < 130 and diastolic < 80:
        return 'Elevated'
    elif systolic < 140 or diastolic < 90:
        return 'High BP Stage 1'
    else:
        return 'High BP Stage 2'

def classify_glucose(glucose, fasting=True):
    """
    Classify blood glucose levels
    """
    if fasting:
        if glucose < 100:
            return 'Normal'
        elif glucose < 126:
            return 'Prediabetes'
        else:
            return 'Diabetes'
    else:
        if glucose < 140:
            return 'Normal'
        elif glucose < 200:
            return 'Prediabetes'
        else:
            return 'Diabetes'

def extract_health_features(df):
    """
    Extract health-related features from raw data
    """
    df_features = df.copy()
    
    # Calculate BMI if not present
    if 'BMI' not in df_features.columns:
        df_features['BMI'] = df_features.apply(
            lambda row: calculate_bmi(row['Weight'], row['Height']), axis=1
        )
    
    # BMI Category
    df_features['BMI_Category'] = df_features['BMI'].apply(classify_bmi)
    
    # Calculate BMR
    df_features['BMR'] = df_features.apply(
        lambda row: calculate_bmr(row['Weight'], row['Height'], 
                                   row['Age'], row['Gender']), axis=1
    )
    
    # Calculate TDEE if activity level present
    if 'Activity_Level' in df_features.columns:
        df_features['TDEE'] = df_features.apply(
            lambda row: calculate_tdee(row['BMR'], row['Activity_Level']), axis=1
        )
    
    return df_features
