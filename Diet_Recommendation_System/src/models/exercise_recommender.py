import pandas as pd
import numpy as np

class ExerciseRecommender:
    def __init__(self, exercise_data):
        """
        Initialize exercise recommender
        """
        self.exercise_data = exercise_data
        
    def get_fitness_level(self, bmi, age, health_conditions):
        """
        Determine fitness level based on health metrics
        """
        if health_conditions or bmi > 30 or age > 60:
            return 'beginner'
        elif 25 <= bmi < 30:
            return 'intermediate'
        else:
            return 'advanced'
    
    def recommend_exercises(self, user_profile, n_exercises=5):
        """
        Recommend exercises based on user profile
        """
        fitness_level = self.get_fitness_level(
            user_profile['bmi'],
            user_profile['age'],
            user_profile.get('health_conditions', [])
        )
        
        goal = user_profile['goal']
        
        # Filter exercises
        filtered_exercises = self.exercise_data.copy()
        
        # Filter by fitness level if column exists
        if 'difficulty' in filtered_exercises.columns:
            filtered_exercises = filtered_exercises[
                filtered_exercises['difficulty'] == fitness_level
            ]
        
        # Prioritize based on goal
        if goal == 'weight_loss':
            # Prefer cardio exercises
            if 'type' in filtered_exercises.columns:
                cardio = filtered_exercises[
                    filtered_exercises['type'] == 'cardio'
                ].head(n_exercises)
                return cardio
        
        elif goal == 'muscle_gain':
            # Prefer strength training
            if 'type' in filtered_exercises.columns:
                strength = filtered_exercises[
                    filtered_exercises['type'] == 'strength'
                ].head(n_exercises)
                return strength
        
        # Default: mixed exercises
        return filtered_exercises.head(n_exercises)
    
    def generate_weekly_plan(self, user_profile):
        """
        Generate weekly exercise plan
        """
        exercises = self.recommend_exercises(user_profile, n_exercises=10)
        
        fitness_level = self.get_fitness_level(
            user_profile['bmi'],
            user_profile['age'],
            user_profile.get('health_conditions', [])
        )
        
        # Frequency based on fitness level
        days_per_week = {
            'beginner': 3,
            'intermediate': 4,
            'advanced': 5
        }
        
        workout_days = days_per_week.get(fitness_level, 3)
        
        weekly_plan = {
            'workout_days': workout_days,
            'rest_days': 7 - workout_days,
            'exercises': exercises,
            'duration_per_session': '30-45 minutes' if fitness_level == 'beginner' else '45-60 minutes'
        }
        
        return weekly_plan
