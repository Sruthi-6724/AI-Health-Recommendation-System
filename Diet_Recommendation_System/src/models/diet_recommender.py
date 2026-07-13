import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

class DietRecommender:
    def __init__(self, nutrition_data):
        """
        Initialize diet recommender with nutrition database
        """
        self.nutrition_data = nutrition_data
        self.model = NearestNeighbors(n_neighbors=10, metric='euclidean')
        
    def calculate_calorie_target(self, tdee, goal):
        """
        Calculate calorie target based on goal
        """
        adjustments = {
            'weight_loss': -500,
            'maintenance': 0,
            'muscle_gain': 300,
            'weight_gain': 500
        }
        
        target = tdee + adjustments.get(goal, 0)
        return round(target)
    
    def calculate_macros(self, calories, diet_type='balanced'):
        """
        Calculate macronutrient targets
        """
        macro_ratios = {
            'balanced': {'protein': 0.30, 'carbs': 0.40, 'fats': 0.30},
            'low_carb': {'protein': 0.35, 'carbs': 0.25, 'fats': 0.40},
            'high_protein': {'protein': 0.40, 'carbs': 0.35, 'fats': 0.25}
        }
        
        ratios = macro_ratios.get(diet_type, macro_ratios['balanced'])
        
        # Calculate grams (protein and carbs = 4 cal/g, fats = 9 cal/g)
        protein_g = round((calories * ratios['protein']) / 4)
        carbs_g = round((calories * ratios['carbs']) / 4)
        fats_g = round((calories * ratios['fats']) / 9)
        
        return {
            'protein': protein_g,
            'carbs': carbs_g,
            'fats': fats_g,
            'calories': calories
        }
    
    def recommend_foods(self, macro_targets, meal_type='breakfast', n_items=5):
        """
        Recommend foods based on macro targets
        """
        # Filter by meal type if column exists
        if 'meal_type' in self.nutrition_data.columns:
            meal_data = self.nutrition_data[
                self.nutrition_data['meal_type'] == meal_type
            ]
        else:
            meal_data = self.nutrition_data
        
        # Simple recommendation based on calorie proximity
        meal_calories = macro_targets['calories'] / 3  # Divide by 3 meals
        
        meal_data_copy = meal_data.copy()
        meal_data_copy['calorie_diff'] = abs(
            meal_data_copy['calories'] - meal_calories
        )
        
        recommendations = meal_data_copy.nsmallest(n_items, 'calorie_diff')
        
        return recommendations[['food_name', 'calories', 'protein', 'carbs', 'fats']]
    
    def generate_meal_plan(self, user_profile):
        """
        Generate complete meal plan
        """
        # Calculate targets
        calorie_target = self.calculate_calorie_target(
            user_profile['tdee'], 
            user_profile['goal']
        )
        
        macros = self.calculate_macros(
            calorie_target, 
            user_profile.get('diet_type', 'balanced')
        )
        
        # Generate recommendations for each meal
        meal_plan = {
            'targets': macros,
            'breakfast': self.recommend_foods(macros, 'breakfast', 3),
            'lunch': self.recommend_foods(macros, 'lunch', 3),
            'dinner': self.recommend_foods(macros, 'dinner', 3),
            'snacks': self.recommend_foods(macros, 'snack', 2)
        }
        
        return meal_plan
