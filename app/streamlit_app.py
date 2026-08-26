import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .risk-low {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .risk-medium {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .risk-high {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the trained model from artifacts."""
    # Get the absolute path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    model_path = os.path.join(project_root, 'artifacts', 'models', 'diabetes_model.pkl')
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)


def get_risk_level(probability):
    """Determine risk level based on probability."""
    if probability < 0.3:
        return "Low Risk", "risk-low"
    elif probability < 0.7:
        return "Medium Risk", "risk-medium"
    else:
        return "High Risk", "risk-high"


def validate_input(age, gender, bmi, hba1c, glucose, hypertension, heart_disease, smoking):
    """Validate user inputs."""
    errors = []
    
    if age < 0 or age > 120:
        errors.append("Age must be between 0 and 120")
    if bmi < 10 or bmi > 80:
        errors.append("BMI must be between 10 and 80")
    if hba1c < 3 or hba1c > 15:
        errors.append("HbA1c must be between 3% and 15%")
    if glucose < 50 or glucose > 500:
        errors.append("Blood glucose must be between 50 and 500 mg/dL")
    
    return errors


def main():
    # Header
    st.markdown('<div class="main-header">🏥 Diabetes Prediction App</div>', unsafe_allow_html=True)
    
    # Load model
    model_data = load_model()
    
    if model_data is None:
        st.error("Model not found. Please ensure the model is trained and saved in artifacts/models/")
        st.stop()
    
    # Business context
    st.markdown("""
    ---
    **Business Context:** This tool helps healthcare professionals identify patients at risk of diabetes 
    for early intervention. The model uses health indicators to predict diabetes probability.
    
    **Disclaimer:** This tool supports clinical decision-making but does not replace professional medical judgment.
    """)
    
    # Create tabs
    tab1, tab2 = st.tabs(["📋 Single Prediction", "📊 Batch Prediction"])
    
    with tab1:
        st.header("Single Patient Prediction")
        
        # Input form
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age (years)", min_value=0.0, max_value=120.0, value=45.0, step=1.0)
                gender = st.selectbox("Gender", ["Female", "Male"])
                bmi = st.number_input("BMI (kg/m²)", min_value=10.0, max_value=80.0, value=28.0, step=0.1)
                hba1c = st.number_input("HbA1c Level (%)", min_value=3.0, max_value=15.0, value=5.7, step=0.1)
            
            with col2:
                glucose = st.number_input("Blood Glucose Level (mg/dL)", min_value=50, max_value=500, value=140, step=1)
                hypertension = st.selectbox("Hypertension", ["No", "Yes"])
                heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
                smoking = st.selectbox("Smoking History", ["never", "not current", "former", "current", "ever"])
            
            submitted = st.form_submit_button("🔮 Predict Diabetes Risk")
        
        if submitted:
            # Validate inputs
            errors = validate_input(age, gender, bmi, hba1c, glucose, 
                                   1 if hypertension == "Yes" else 0,
                                   1 if heart_disease == "Yes" else 0, smoking)
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Prepare features
                smoking_map = {'never': 0, 'not current': 1, 'former': 2, 'current': 3, 'ever': 4}
                
                features = pd.DataFrame({
                    'age': [age],
                    'bmi': [bmi],
                    'HbA1c_level': [hba1c],
                    'blood_glucose_level': [glucose],
                    'hypertension': [1 if hypertension == "Yes" else 0],
                    'heart_disease': [1 if heart_disease == "Yes" else 0],
                    'gender_male': [1 if gender == "Male" else 0],
                    'smoking_history_encoded': [smoking_map[smoking]]
                })
                
                # Get prediction
                model = model_data['model']
                threshold = model_data['threshold']
                
                probability = model.predict_proba(features)[:, 1][0]
                prediction = 1 if probability >= threshold else 0
                
                # Display results
                st.markdown("---")
                st.subheader("Prediction Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Predicted Class", "Diabetes" if prediction == 1 else "No Diabetes")
                
                with col2:
                    st.metric("Diabetes Probability", f"{probability:.2%}")
                
                with col3:
                    risk_level, risk_class = get_risk_level(probability)
                    st.markdown(f'<div class="{risk_class}">{risk_level}</div>', unsafe_allow_html=True)
                
                # Risk interpretation
                st.markdown("---")
                st.subheader("Interpretation")
                
                if prediction == 1:
                    st.warning("⚠️ **High Risk**: This patient is predicted to have diabetes. Consider further diagnostic testing and lifestyle modifications.")
                else:
                    if probability > 0.3:
                        st.info("ℹ️ **Moderate Risk**: While the model predicts no diabetes, the probability is elevated. Regular monitoring is recommended.")
                    else:
                        st.success("✅ **Low Risk**: This patient is predicted not to have diabetes. Continue maintaining healthy lifestyle.")
                
                # Model notes
                st.markdown("---")
                st.caption("""
                **Model Notes:**\n
                - Model: LightGBM (tuned with Bayesian optimization)\n
                - Threshold: {:.2f} (optimized for recall ≥ 0.60)\n
                - Features used: age, BMI, HbA1c, glucose, hypertension, heart disease, gender, smoking history\n
                - Limitations: Correlation does not imply causation. This tool supports, not replaces, clinical judgment.
                """.format(threshold))
    
    with tab2:
        st.header("Batch Prediction from CSV")
        
        st.markdown("""
        Upload a CSV file with patient data. The file should contain the following columns:
        - `age`, `gender`, `bmi`, `HbA1c_level`, `blood_glucose_level`
        - `hypertension`, `heart_disease`, `smoking_history`
        """)
        
        # File uploader
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                # Read CSV
                df_uploaded = pd.read_csv(uploaded_file)
                st.success(f"File uploaded successfully: {uploaded_file.name}")
                st.write(f"Rows: {len(df_uploaded)}, Columns: {len(df_uploaded.columns)}")
                
                # Display preview
                with st.expander("Preview uploaded data"):
                    st.dataframe(df_uploaded.head(10))
                
                # Validate required columns
                required_columns = ['age', 'gender', 'bmi', 'HbA1c_level', 
                                   'blood_glucose_level', 'hypertension', 
                                   'heart_disease', 'smoking_history']
                
                missing_cols = [col for col in required_columns if col not in df_uploaded.columns]
                
                if missing_cols:
                    st.error(f"Missing required columns: {', '.join(missing_cols)}")
                else:
                    # Process predictions
                    smoking_map = {'never': 0, 'No Info': 0, 'not current': 1, 'former': 2, 'current': 3, 'ever': 4}
                    
                    df_processed = df_uploaded.copy()
                    df_processed['smoking_history_encoded'] = df_processed['smoking_history'].map(smoking_map).fillna(0)
                    df_processed['gender_male'] = (df_processed['gender'] == 'Male').astype(int)
                    
                    features = df_processed[['age', 'bmi', 'HbA1c_level', 'blood_glucose_level',
                                            'hypertension', 'heart_disease', 'gender_male', 
                                            'smoking_history_encoded']]
                    
                    # Get predictions
                    model = model_data['model']
                    threshold = model_data['threshold']
                    
                    probabilities = model.predict_proba(features)[:, 1]
                    predictions = (probabilities >= threshold).astype(int)
                    
                    # Create output dataframe
                    df_output = df_uploaded.copy()
                    df_output['diabetes_prediction'] = predictions
                    df_output['diabetes_probability'] = probabilities
                    df_output['risk_level'] = df_output['diabetes_probability'].apply(
                        lambda x: 'Low Risk' if x < 0.3 else ('Medium Risk' if x < 0.7 else 'High Risk')
                    )
                    
                    # Display results
                    st.markdown("---")
                    st.subheader("Prediction Results")
                    
                    # Summary metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Patients", len(df_output))
                    with col2:
                        st.metric("Predicted Diabetes", f"{predictions.sum()} ({predictions.mean()*100:.1f}%)")
                    with col3:
                        st.metric("High Risk Patients", 
                                 f"{(df_output['risk_level'] == 'High Risk').sum()}")
                    
                    # Display results table
                    with st.expander("View prediction results"):
                        st.dataframe(df_output)
                    
                    # Download button
                    csv = df_output.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Predictions CSV",
                        data=csv,
                        file_name="diabetes_predictions.csv",
                        mime="text/csv"
                    )
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")


if __name__ == "__main__":
    main()
