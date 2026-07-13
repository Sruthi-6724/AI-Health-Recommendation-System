import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed')
MODEL_PATH = os.path.join(BASE_DIR, 'models')
RESULTS_PATH = os.path.join(BASE_DIR, 'results')

# Health thresholds
HEALTH_THRESHOLDS = {
    'glucose_normal': 100,
    'glucose_prediabetes': 125,
    'glucose_diabetes': 126,
    'bp_normal': 120,
    'bp_elevated': 130,
    'bp_high': 140,
    'bmi_underweight': 18.5,
    'bmi_normal': 24.9,
    'bmi_overweight': 29.9,
    'bmi_obese': 30,
    'cholesterol_normal': 200,
    'cholesterol_borderline': 239,
    'cholesterol_high': 240
}

# Nutrient targets (per day)
CALORIE_ADJUSTMENT = {
    'weight_loss': -500,
    'maintenance': 0,
    'muscle_gain': 300
}

# Macronutrient ratios (percentage of total calories)
MACRO_RATIOS = {
    'balanced': {'protein': 0.30, 'carbs': 0.40, 'fats': 0.30},
    'low_carb': {'protein': 0.35, 'carbs': 0.25, 'fats': 0.40},
    'high_protein': {'protein': 0.40, 'carbs': 0.35, 'fats': 0.25}
}

# Activity level multipliers (for BMR)
ACTIVITY_MULTIPLIERS = {
    'Sedentary': 1.2,
    'Lightly Active': 1.375,
    'Moderately Active': 1.55,
    'Very Active': 1.725,
    'Extremely Active': 1.9
}
