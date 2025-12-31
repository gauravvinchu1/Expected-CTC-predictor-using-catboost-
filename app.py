from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the model when the app starts
try:
    model = joblib.load("catboost_model.joblib")
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Get form data
        data = request.get_json()
        
        # Prepare features in correct order (based on model training)
        features = {
            'Total_Experience': float(data.get('Total_Experience', 0)),
            'Total_Experience_in_field_applied': float(data.get('Total_Experience_in_field_applied', 0)),
            'Department': data.get('Department', 'NaN'),
            'Role': data.get('Role', 'NaN'),
            'Industry': data.get('Industry', 'NaN'),
            'Organization': data.get('Organization', 'NaN'),
            'Designation': data.get('Designation', 'fresher'),
            'Education': data.get('Education', 'Grad'),
            'Graduation_Specialization': data.get('Graduation_Specialization', 'Others'),
            'University_Grad': data.get('University_Grad', 'Delhi'),
            'Passing_Year_Of_Graduation': float(data.get('Passing_Year_Of_Graduation', 2020)),
            'PG_Specialization': data.get('PG_Specialization', 'NaN'),
            'University_PG': data.get('University_PG', 'NaN'),
            'Passing_Year_Of_PG': float(data.get('Passing_Year_Of_PG', 0)) if data.get('Passing_Year_Of_PG') else np.nan,
            'PHD_Specialization': data.get('PHD_Specialization', 'NaN'),
            'University_PHD': data.get('University_PHD', 'NaN'),
            'Passing_Year_Of_PHD': float(data.get('Passing_Year_Of_PHD', 0)) if data.get('Passing_Year_Of_PHD') else np.nan,
            'Curent_Location': data.get('Curent_Location', 'Delhi'),
            'Preferred_location': data.get('Preferred_location', 'Delhi'),
            'Current_CTC': float(data.get('Current_CTC', 0)),
            'Inhand_Offer': data.get('Inhand_Offer', 'N'),
            'Last_Appraisal_Rating': data.get('Last_Appraisal_Rating', 'NaN'),
            'No_Of_Companies_worked': int(data.get('No_Of_Companies_worked', 0)),
            'Number_of_Publications': int(data.get('Number_of_Publications', 0)),
            'Certifications': int(data.get('Certifications', 0)),
            'International_degree_any': int(data.get('International_degree_any', 0))
        }
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # Replace empty strings with NaN for numerical columns that should be NaN
        numerical_columns = ['Passing_Year_Of_PG', 'Passing_Year_Of_PHD']
        for col in numerical_columns:
            if df[col].iloc[0] == 0:  # If default value was used
                df[col] = np.nan
        
        # Make prediction
        prediction = model.predict(df)
        predicted_salary = float(prediction[0])
        
        # Format salary in INR
        formatted_salary = f"₹{predicted_salary:,.2f}"
        
        return jsonify({
            'predicted_salary': predicted_salary,
            'formatted_salary': formatted_salary,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

if __name__ == '__main__':
    app.run(debug=True)