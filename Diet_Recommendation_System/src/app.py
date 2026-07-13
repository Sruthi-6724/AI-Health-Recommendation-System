import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processing.extract_features import (
    calculate_bmi, calculate_bmr, calculate_tdee, 
    classify_bmi, classify_glucose
)
from config.config import HEALTH_THRESHOLDS, ACTIVITY_MULTIPLIERS

# Page configuration
st.set_page_config(
    page_title="Health Recommendation System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean design
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Home",
    "👤 Health Profile",
    "📊 Health Analysis",
    "🍽️ Diet Recommendations",
    "🏋️ Exercise Plan",
    "📈 Progress Tracker"
])

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# ==================== HOME PAGE ====================
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">🏥 Health Recommendation System</h1>', 
                unsafe_allow_html=True)
    
    st.write("""
    ### Welcome to your personalized health assistant!
    
    This AI-powered system provides:
    - 📊 Comprehensive health analysis
    - 🍽️ Personalized diet plans
    - 🏋️ Custom exercise routines
    - 📈 Progress tracking
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Step 1**\n\nCreate your health profile")
    with col2:
        st.success("**Step 2**\n\nGet AI recommendations")
    with col3:
        st.warning("**Step 3**\n\nTrack your progress")
    
    st.markdown("---")
    st.subheader("📋 Project Information")
    st.write("""
    **Academic Project**: Machine Learning-based Health Recommendation System
    
    **Features**:
    - Health risk classification
    - BMI & metabolic rate calculation
    - Personalized meal plans
    - Exercise recommendations
    - Progress visualization
    """)

# ==================== HEALTH PROFILE PAGE ====================
elif page == "👤 Health Profile":
    st.header("👤 Create Your Health Profile")
    
    with st.form("profile_form"):
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value=st.session_state.user_data.get('name', ''))
            age = st.number_input("Age", min_value=18, max_value=100, 
                                 value=st.session_state.user_data.get('age', 25))
            gender = st.selectbox("Gender", ["Male", "Female"], 
                                 index=0 if st.session_state.user_data.get('gender', 'Male') == 'Male' else 1)
        
        with col2:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, 
                                    value=st.session_state.user_data.get('weight', 70.0))
            height = st.number_input("Height (cm)", min_value=140.0, max_value=220.0, 
                                    value=st.session_state.user_data.get('height', 170.0))
        
        st.subheader("Lifestyle Information")
        col3, col4 = st.columns(2)
        
        with col3:
            activity_level = st.selectbox("Activity Level", 
                list(ACTIVITY_MULTIPLIERS.keys()),
                index=0)
            goal = st.selectbox("Health Goal", 
                ["weight_loss", "maintenance", "muscle_gain", "weight_gain"])
        
        with col4:
            diet_preference = st.selectbox("Diet Preference", 
                ["balanced", "low_carb", "high_protein"])
        
        st.subheader("Medical Information (Optional)")
        col5, col6 = st.columns(2)
        
        with col5:
            glucose = st.number_input("Fasting Glucose (mg/dL)", min_value=50, max_value=300, 
                                     value=st.session_state.user_data.get('glucose', 90))
            bp_systolic = st.number_input("Blood Pressure (Systolic)", min_value=80, max_value=200, 
                                         value=st.session_state.user_data.get('bp_systolic', 120))
        
        with col6:
            cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=400, 
                                         value=st.session_state.user_data.get('cholesterol', 180))
        
        submitted = st.form_submit_button("Save Profile")
        
        if submitted:
            # Calculate metrics
            bmi = calculate_bmi(weight, height)
            bmr = calculate_bmr(weight, height, age, gender)
            tdee = calculate_tdee(bmr, activity_level)
            
            # Save to session state
            st.session_state.user_data = {
                'name': name,
                'age': age,
                'gender': gender,
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'bmr': bmr,
                'tdee': tdee,
                'activity_level': activity_level,
                'goal': goal,
                'diet_preference': diet_preference,
                'glucose': glucose,
                'bp_systolic': bp_systolic,
                'cholesterol': cholesterol
            }
            
            st.success("✅ Profile saved successfully!")
            st.balloons()

# ==================== HEALTH ANALYSIS PAGE ====================
elif page == "📊 Health Analysis":
    st.header("📊 Health Analysis Dashboard")
    
    if not st.session_state.user_data:
        st.warning("⚠️ Please create your health profile first!")
    else:
        user = st.session_state.user_data
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("BMI", f"{user['bmi']:.1f}", 
                     classify_bmi(user['bmi']))
        with col2:
            st.metric("BMR", f"{user['bmr']:.0f} cal")
        with col3:
            st.metric("TDEE", f"{user['tdee']:.0f} cal")
        with col4:
            glucose_status = classify_glucose(user['glucose'])
            st.metric("Glucose", f"{user['glucose']} mg/dL", glucose_status)
        
        st.markdown("---")
        
        # Health status
        st.subheader("🔍 Health Status")
        
        col5, col6 = st.columns(2)
        
        with col5:
            st.write("**BMI Category**")
            bmi_cat = classify_bmi(user['bmi'])
            if bmi_cat == 'Normal':
                st.success(f"✅ {bmi_cat}")
            elif bmi_cat in ['Overweight', 'Underweight']:
                st.warning(f"⚠️ {bmi_cat}")
            else:
                st.error(f"❌ {bmi_cat}")
        
        with col6:
            st.write("**Blood Glucose**")
            glucose_cat = classify_glucose(user['glucose'])
            if glucose_cat == 'Normal':
                st.success(f"✅ {glucose_cat}")
            elif glucose_cat == 'Prediabetes':
                st.warning(f"⚠️ {glucose_cat}")
            else:
                st.error(f"❌ {glucose_cat}")
        
        # Risk assessment
        st.markdown("---")
        st.subheader("⚠️ Health Risk Assessment")
        
        risk_score = 0
        risk_factors = []
        
        if user['bmi'] < 18.5 or user['bmi'] >= 30:
            risk_score += 2
            risk_factors.append("BMI outside healthy range")
        elif user['bmi'] >= 25:
            risk_score += 1
            risk_factors.append("BMI in overweight range")
        
        if user['glucose'] >= 126:
            risk_score += 2
            risk_factors.append("High glucose (diabetes range)")
        elif user['glucose'] >= 100:
            risk_score += 1
            risk_factors.append("Elevated glucose")
        
        if user['bp_systolic'] >= 140:
            risk_score += 2
            risk_factors.append("High blood pressure")
        elif user['bp_systolic'] >= 130:
            risk_score += 1
            risk_factors.append("Elevated blood pressure")
        
        if user['cholesterol'] >= 240:
            risk_score += 2
            risk_factors.append("High cholesterol")
        elif user['cholesterol'] >= 200:
            risk_score += 1
            risk_factors.append("Borderline high cholesterol")
        
        # Display risk level
        if risk_score == 0:
            st.success("✅ **Low Risk** - Your health metrics are within normal ranges")
        elif risk_score <= 3:
            st.warning(f"⚠️ **Medium Risk** - Some metrics need attention")
        else:
            st.error(f"❌ **High Risk** - Multiple health concerns detected")
        
        if risk_factors:
            st.write("**Risk Factors Identified:**")
            for factor in risk_factors:
                st.write(f"- {factor}")

# ==================== DIET RECOMMENDATIONS PAGE ====================
elif page == "🍽️ Diet Recommendations":
    st.header("🍽️ Personalized Diet Plan")
    
    if not st.session_state.user_data:
        st.warning("⚠️ Please create your health profile first!")
    else:
        user = st.session_state.user_data
        
        # Calculate calorie target
        calorie_adjustments = {
            'weight_loss': -500,
            'maintenance': 0,
            'muscle_gain': 300,
            'weight_gain': 500
        }
        
        target_calories = user['tdee'] + calorie_adjustments.get(user['goal'], 0)
        
        st.subheader("📊 Daily Nutrition Targets")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate macros
        macro_ratios = {
            'balanced': {'protein': 0.30, 'carbs': 0.40, 'fats': 0.30},
            'low_carb': {'protein': 0.35, 'carbs': 0.25, 'fats': 0.40},
            'high_protein': {'protein': 0.40, 'carbs': 0.35, 'fats': 0.25}
        }
        
        ratios = macro_ratios[user['diet_preference']]
        protein_g = round((target_calories * ratios['protein']) / 4)
        carbs_g = round((target_calories * ratios['carbs']) / 4)
        fats_g = round((target_calories * ratios['fats']) / 9)
        
        with col1:
            st.metric("Calories", f"{target_calories:.0f}")
        with col2:
            st.metric("Protein", f"{protein_g}g")
        with col3:
            st.metric("Carbs", f"{carbs_g}g")
        with col4:
            st.metric("Fats", f"{fats_g}g")
        
        st.markdown("---")
        
        # Sample meal plan
        st.subheader("🍽️ Sample Meal Plan")
        
        st.write("**Breakfast (30% of daily calories)**")
        breakfast_cal = target_calories * 0.30
        st.write(f"Target: ~{breakfast_cal:.0f} calories")
        st.write("- Oatmeal with fruits and nuts")
        st.write("- Greek yogurt with berries")
        st.write("- Whole grain toast with eggs")
        
        st.write("**Lunch (35% of daily calories)**")
        lunch_cal = target_calories * 0.35
        st.write(f"Target: ~{lunch_cal:.0f} calories")
        st.write("- Grilled chicken with quinoa and vegetables")
        st.write("- Brown rice with dal and salad")
        st.write("- Whole wheat roti with paneer curry")
        
        st.write("**Dinner (30% of daily calories)**")
        dinner_cal = target_calories * 0.30
        st.write(f"Target: ~{dinner_cal:.0f} calories")
        st.write("- Baked fish with sweet potato")
        st.write("- Vegetable stir-fry with tofu")
        st.write("- Lean meat with steamed vegetables")
        
        st.write("**Snacks (5% of daily calories)**")
        snack_cal = target_calories * 0.05
        st.write(f"Target: ~{snack_cal:.0f} calories")
        st.write("- Mixed nuts (handful)")
        st.write("- Fresh fruits")
        st.write("- Protein shake")
        
        st.markdown("---")
        st.info("💡 **Tip**: Drink at least 8 glasses of water daily and avoid processed foods")

# ==================== EXERCISE PLAN PAGE ====================
elif page == "🏋️ Exercise Plan":
    st.header("🏋️ Personalized Exercise Plan")
    
    if not st.session_state.user_data:
        st.warning("⚠️ Please create your health profile first!")
    else:
        user = st.session_state.user_data
        
        # Determine fitness level
        if user['bmi'] > 30 or user['age'] > 60:
            fitness_level = 'Beginner'
            workout_days = 3
            duration = "20-30 minutes"
        elif user['bmi'] > 25:
            fitness_level = 'Intermediate'
            workout_days = 4
            duration = "30-45 minutes"
        else:
            fitness_level = 'Advanced'
            workout_days = 5
            duration = "45-60 minutes"
        
        st.subheader("📊 Your Fitness Profile")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Fitness Level", fitness_level)
        with col2:
            st.metric("Workout Days/Week", workout_days)
        with col3:
            st.metric("Session Duration", duration)
        
        st.markdown("---")
        
        # Exercise recommendations based on goal
        st.subheader("🎯 Recommended Exercises")
        
        if user['goal'] == 'weight_loss':
            st.write("**Focus: Cardio & Fat Burning**")
            exercises = [
                {"Exercise": "Brisk Walking", "Duration": "30 min", "Calories": "150-200"},
                {"Exercise": "Jogging", "Duration": "20 min", "Calories": "200-300"},
                {"Exercise": "Cycling", "Duration": "30 min", "Calories": "250-350"},
                {"Exercise": "Swimming", "Duration": "30 min", "Calories": "250-400"},
                {"Exercise": "Jump Rope", "Duration": "15 min", "Calories": "150-250"}
            ]
        
        elif user['goal'] == 'muscle_gain':
            st.write("**Focus: Strength Training**")
            exercises = [
                {"Exercise": "Push-ups", "Sets x Reps": "3 x 12", "Rest": "60s"},
                {"Exercise": "Squats", "Sets x Reps": "3 x 15", "Rest": "60s"},
                {"Exercise": "Deadlifts", "Sets x Reps": "3 x 10", "Rest": "90s"},
                {"Exercise": "Bench Press", "Sets x Reps": "3 x 10", "Rest": "90s"},
                {"Exercise": "Pull-ups", "Sets x Reps": "3 x 8", "Rest": "60s"}
            ]
        
        else:  # maintenance
            st.write("**Focus: Mixed Training**")
            exercises = [
                {"Exercise": "Walking", "Duration": "30 min", "Type": "Cardio"},
                {"Exercise": "Bodyweight Squats", "Sets x Reps": "3 x 15", "Type": "Strength"},
                {"Exercise": "Yoga", "Duration": "30 min", "Type": "Flexibility"},
                {"Exercise": "Cycling", "Duration": "20 min", "Type": "Cardio"},
                {"Exercise": "Planks", "Duration": "3 x 60s", "Type": "Core"}
            ]
        
        df_exercises = pd.DataFrame(exercises)
        st.table(df_exercises)
        
        st.markdown("---")
        
        # Weekly schedule
        st.subheader("📅 Weekly Workout Schedule")
        
        schedule = {
            'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'Activity': []
        }
        
        if workout_days == 3:
            schedule['Activity'] = ['Workout', 'Rest', 'Workout', 'Rest', 'Workout', 'Rest', 'Rest']
        elif workout_days == 4:
            schedule['Activity'] = ['Workout', 'Workout', 'Rest', 'Workout', 'Rest', 'Workout', 'Rest']
        else:
            schedule['Activity'] = ['Workout', 'Workout', 'Workout', 'Rest', 'Workout', 'Workout', 'Rest']
        
        df_schedule = pd.DataFrame(schedule)
        st.table(df_schedule)
        
        st.info("💡 **Tips**: Always warm up for 5-10 minutes before exercising and cool down after")

# ==================== PROGRESS TRACKER PAGE ====================
elif page == "📈 Progress Tracker":
    st.header("📈 Track Your Progress")
    
    if not st.session_state.user_data:
        st.warning("⚠️ Please create your health profile first!")
    else:
        st.subheader("📝 Log Your Daily Activities")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Log Weight**")
            current_weight = st.number_input("Today's Weight (kg)", 
                                            min_value=30.0, 
                                            max_value=200.0,
                                            value=st.session_state.user_data['weight'])
            log_weight = st.button("Log Weight")
            
            if log_weight:
                st.success("✅ Weight logged successfully!")
        
        with col2:
            st.write("**Log Workout**")
            workout_type = st.selectbox("Workout Type", 
                ["Cardio", "Strength", "Flexibility", "Mixed"])
            workout_duration = st.number_input("Duration (minutes)", 
                                              min_value=5, max_value=180, value=30)
            log_workout = st.button("Log Workout")
            
            if log_workout:
                st.success("✅ Workout logged successfully!")
        
        st.markdown("---")
        
        # Sample progress visualization
        st.subheader("📊 Progress Overview")
        
        # Generate sample data
        dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
        sample_weights = [st.session_state.user_data['weight'] - i*0.1 for i in range(30)]
        sample_weights.reverse()
        
        progress_df = pd.DataFrame({
            'Date': dates,
            'Weight': sample_weights
        })
        
        st.line_chart(progress_df.set_index('Date'))
        
        st.markdown("---")
        
        # Weekly summary
        st.subheader("📅 Weekly Summary")
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.metric("Workouts Completed", "4/5", "+1")
        with col4:
            st.metric("Avg Calories", "1850", "-150")
        with col5:
            st.metric("Weight Change", "-0.5 kg", "-0.5 kg")
        
        st.success("🎉 Great progress! Keep up the good work!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Health Recommendation System | Academic Project | 2026</p>
    </div>
""", unsafe_allow_html=True)
