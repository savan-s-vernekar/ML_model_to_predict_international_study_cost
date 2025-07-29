import sys
import json
import joblib
import pandas as pd
import os

try:
    input_data = json.loads(sys.stdin.read())
    
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    model = joblib.load(model_path)
    
    df_input = pd.DataFrame({
        "Duration_Years": [input_data["duration"]],
        "Tuition_USD": [input_data["tuition"]],
        "Living_Cost_Index": [input_data["living_cost_index"]],
        "Rent_USD": [input_data["rent"]],
        "Visa_Fee_USD": [input_data["visa_fee"]],
        "Insurance_USD": [input_data["insurance"]],
        "Exchange_Rate": [input_data["exchange_rate"]]
    })
    
    prediction = model.predict(df_input)[0]
    result = {"prediction": float(prediction)}
    print(json.dumps(result))
    
except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)