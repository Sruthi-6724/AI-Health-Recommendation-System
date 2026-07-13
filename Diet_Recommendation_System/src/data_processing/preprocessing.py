import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def clean_data(df):
    """
    Clean raw data by handling missing values and outliers
    """
    # Make a copy
    df_clean = df.copy()
    
    # Handle missing values
    numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    # Fill categorical missing values
    categorical_columns = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
    
    # Remove duplicates
    df_clean.drop_duplicates(inplace=True)
    
    return df_clean

def handle_outliers(df, columns, method='iqr'):
    """
    Handle outliers using IQR method
    """
    df_out = df.copy()
    
    for col in columns:
        Q1 = df_out[col].quantile(0.25)
        Q3 = df_out[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Cap outliers instead of removing
        df_out[col] = df_out[col].clip(lower_bound, upper_bound)
    
    return df_out

def normalize_features(df, columns):
    """
    Normalize numerical features
    """
    scaler = StandardScaler()
    df_normalized = df.copy()
    df_normalized[columns] = scaler.fit_transform(df[columns])
    
    return df_normalized, scaler

def encode_categorical(df, columns):
    """
    Encode categorical variables
    """
    df_encoded = df.copy()
    encoders = {}
    
    for col in columns:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    
    return df_encoded, encoders

def preprocess_data(df, numeric_cols, categorical_cols=None):
    """
    Complete preprocessing pipeline
    """
    # Clean data
    df_processed = clean_data(df)
    
    # Handle outliers
    df_processed = handle_outliers(df_processed, numeric_cols)
    
    # Encode categorical if provided
    if categorical_cols:
        df_processed, encoders = encode_categorical(df_processed, categorical_cols)
    
    return df_processed
