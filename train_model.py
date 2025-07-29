import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os
import sys
import json

def train_model(csv_path):
    # Load the dataset
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), csv_path)
    
    df = pd.read_csv(csv_path)
    
    # Features and target
    features = ["Duration_Years", "Tuition_USD", "Living_Cost_Index", "Rent_USD", "Visa_Fee_USD", "Insurance_USD", "Exchange_Rate"]
    target = "Total Annual Cost (USD)"
    
    X = df[features]
    y = df[target]
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    joblib.dump(model, model_path)
    
    return True

if __name__ == "__main__":
    try:
        input_data = json.loads(sys.stdin.read())
        csv_path = input_data.get('csvPath', 'International_Education_Costs_with_Calculations.csv')
        success = train_model(csv_path)
        print(json.dumps({"success": success}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)