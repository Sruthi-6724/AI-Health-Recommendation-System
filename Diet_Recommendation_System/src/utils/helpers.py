import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_feature_importance(importance_df, top_n=10):
    """
    Plot feature importance
    """
    plt.figure(figsize=(10, 6))
    top_features = importance_df.head(top_n)
    
    sns.barplot(data=top_features, x='importance', y='feature')
    plt.title('Top Feature Importance')
    plt.xlabel('Importance Score')
    plt.tight_layout()
    
    return plt

def plot_confusion_matrix(cm, labels):
    """
    Plot confusion matrix
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    return plt

def calculate_metrics(y_true, y_pred):
    """
    Calculate various metrics
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted'),
        'recall': recall_score(y_true, y_pred, average='weighted'),
        'f1_score': f1_score(y_true, y_pred, average='weighted')
    }
    
    return metrics

def save_results(results, filepath):
    """
    Save results to file
    """
    with open(filepath, 'w') as f:
        for key, value in results.items():
            f.write(f"{key}: {value}\n")
    print(f"Results saved to {filepath}")
