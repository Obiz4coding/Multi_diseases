
import streamlit as st
import pickle
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="FUOYE Multiple Disease Prediction System", layout="wide", page_icon="🏥")

# --- CUSTOM COLORFUL CSS (FUOYE BRANDING: GREEN & GOLD) ---
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #022d15 0%, #004d25 50%, #03381a 100%);
        color: #f4f7f4;
    }
    
    /* Sidebar styling - Dark Emerald */
    section[data-testid="stSidebar"] {
        background-color: #012311 !important;
        color: white;
        border-right: 1px solid #d4af37;
    }
    
    section[data-testid="stSidebar"] .st-at {
        color: white;
    }

    /* Titles and Headers */
    h1 {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        border-bottom: 3px solid #d4af37;
        padding-bottom: 10px;
    }
    
    h2, h3, .stSubheader {
        color: #f0e6d2 !important;
    }

    /* Card-like containers for inputs */
    .stNumberInput, .stSelectbox, .stTextInput {
        background-color: rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        padding: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid rgba(212, 175, 55, 0.4);
    }
    
    /* Input labels text color */
    .stNumberInput label, .stSelectbox label, .stTextInput label {
        color: #f4f7f4 !important;
        font-weight: 500;
    }

    /* Predict Button Styling - FUOYE Gold Accent */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #d4af37, #f3e5ab);
        color: #004d25;
        border-radius: 20px;
        width: 100%;
        font-weight: bold;
        border: 2px solid #ffffff;
        transition: 0.3s;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #ffffff, #d4af37);
        color: #012311;
        transform: scale(1.02);
        border: 2px solid #d4af37;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MODEL LOADING ---
@st.cache_resource 
def load_model(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

models = {
    "Diabetes Prediction": "diabetes_model.pkl",
    "Heart Disease Prediction": "heart_disease_model.pkl",
    "Parkinson's Prediction": "parkinsons_model.pkl",
    "Lung Cancer Prediction": "lung_cancer_model.pkl",
    "Breast Cancer Prediction": "breast_cancer_model.pkl"
}

# --- SIDEBAR ---
with st.sidebar:
    st.image("download.jpg", width=100)
    st.title("FUOYE Health Portal")
    st.markdown("<p style='color: #d4af37; font-weight: bold;'>Federal University Oye-Ekiti</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Symptom / Keyword Search Box
    st.subheader("🔍 Symptom Search")
    search_query = st.text_input("Type symptom (e.g. sugar, chest pain, cough)").lower()
    
    # Match search query to disease tool if applicable
    default_index = 0
    if search_query:
        if any(kw in search_query for kw in ["sugar", "glucose", "insulin", "diabetes", "fat"]):
            default_index = 0
        elif any(kw in search_query for kw in ["chest", "heart", "cardio", "blood pressure", "bp"]):
            default_index = 1
        elif any(kw in search_query for kw in ["voice", "vocal", "shake", "parkinson", "tremor"]):
            default_index = 2
        elif any(kw in search_query for kw in ["lung", "cough", "smoke", "breathing", "wheezing"]):
            default_index = 3
        elif any(kw in search_query for kw in ["breast", "lump", "biopsy", "tumor"]):
            default_index = 4

    selected_disease = st.selectbox("Select Diagnostic Tool", list(models.keys()), index=default_index)
    
    if search_query:
        st.success(f"Matched tool for: '{search_query}'")

    st.markdown("---")
    st.info("Federal University Oye-Ekiti (FUOYE) Medical Diagnostics Center: Preliminary analysis system powered by clinical intelligence.")

# --- MAIN CONTENT ---
st.markdown("<h1 style='text-align: center; font-size: 2.2rem;'>Multistage Classification of Medical Symptoms Using a Web-based System</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align: center; color: #d4af37 !important;'>🔍 {selected_disease}</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #f0e6d2; font-style: italic;'>Developed under the auspices of Federal University Oye-Ekiti (FUOYE) academic software initiatives.</p>", unsafe_allow_html=True)
st.markdown("---")

if selected_disease == "Diabetes Prediction":
    st.subheader("Patient Clinical Metrics")
    with st.container():
        cols = st.columns(3)
        preg = cols[0].number_input("Pregnancies", min_value=0)
        gluc = cols[1].number_input("Glucose Level", min_value=0)
        bp = cols[2].number_input("Blood Pressure", min_value=0)
        skin = cols[0].number_input("Skin Thickness", min_value=0)
        ins = cols[1].number_input("Insulin Level", min_value=0)
        bmi = cols[2].number_input("BMI Index", format="%.2f")
        dpf = cols[0].number_input("Diabetes Pedigree Function", format="%.3f")
        age = cols[1].number_input("Patient Age", min_value=1)
    
    if st.button("Generate Diagnostic Report"):
        model = load_model(models[selected_disease])
        prediction = model.predict([[preg, gluc, bp, skin, ins, bmi, dpf, age]])
        if prediction[0] == 1:
            st.error("### Result: High Risk of Diabetes")
        else:
            st.success("### Result: Low Risk / Negative")

elif selected_disease == "Heart Disease Prediction":
    st.subheader("Cardiovascular Parameters")
    with st.container():
        cols = st.columns(3)
        age = cols[0].number_input("Age", min_value=1)
        sex = cols[1].selectbox("Sex", ["Male", "Female"])
        sex_val = 1 if sex == "Male" else 0
        cp = cols[2].number_input("Chest Pain Type (0-3)", 0, 3)
        trestbps = cols[0].number_input("Resting BP", min_value=0)
        chol = cols[1].number_input("Cholesterol", min_value=0)
        fbs = cols[2].selectbox("Fasting Sugar > 120", ["No", "Yes"])
        fbs_val = 1 if fbs == "Yes" else 0
        restecg = cols[0].number_input("Resting ECG (0-2)", 0, 2)
        thalach = cols[1].number_input("Max Heart Rate", min_value=0)
        exang = cols[2].selectbox("Angina during Exercise", ["No", "Yes"])
        exang_val = 1 if exang == "Yes" else 0
        oldpeak = cols[0].number_input("ST Depression", format="%.2f")
        slope = cols[1].number_input("ST Slope (0-2)", 0, 2)
        ca = cols[2].number_input("Major Vessels (0-4)", 0, 4)
        thal = cols[0].number_input("Thal (0-3)", 0, 3)
    
    if st.button("Analyze Cardiac Risk"):
        model = load_model(models[selected_disease])
        prediction = model.predict([[age, sex_val, cp, trestbps, chol, fbs_val, restecg, thalach, exang_val, oldpeak, slope, ca, thal]])
        if prediction[0] == 1:
            st.error("### Warning: Cardiovascular Disease Detected")
        else:
            st.success("### Result: Healthy Heart Pattern")

elif selected_disease == "Parkinson's Prediction":
    st.info("Note: This model analyzes acoustic vocal patterns.")
    f_names = ["MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Jitter(Abs)", 
               "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", "MDVP:Shimmer(dB)", 
               "Shimmer:APQ3", "Shimmer:APQ5", "MDVP:APQ", "Shimmer:DDA", "NHR", "HNR", 
               "RPDE", "DFA", "spread1", "spread2", "D2", "PPE"]
    
    inputs = []
    cols = st.columns(4)
    for i, f in enumerate(f_names):
        inputs.append(cols[i % 4].number_input(f, format="%.5f"))
        
    if st.button("Run Vocal Stability Analysis"):
        model = load_model(models[selected_disease])
        prediction = model.predict([inputs])
        if prediction[0] == 1:
            st.error("### High Probability of Parkinson's Symptoms")
        else:
            st.success("### Vocal Patterns Appear Normal")

elif selected_disease == "Lung Cancer Prediction":
    cols = st.columns(2)
    gender = cols[0].selectbox("Gender", ["Male", "Female"])
    gender_val = 1 if gender == "Male" else 0
    age = cols[1].number_input("Age", 1, 100)
    
    symptoms = ["Smoking", "Yellow Fingers", "Anxiety", "Peer Pressure", "Chronic Disease", 
                "Fatigue", "Allergy", "Wheezing", "Alcohol", "Coughing", "Shortness of Breath", 
                "Swallowing Difficulty", "Chest Pain"]
    
    symp_vals = []
    s_cols = st.columns(3)
    for i, s in enumerate(symptoms):
        res = s_cols[i % 3].selectbox(s, ["No", "Yes"])
        symp_vals.append(2 if res == "Yes" else 1) 

    if st.button("Check Pulmonary Risk"):
        model = load_model(models[selected_disease])
        features = [gender_val, age] + symp_vals
        prediction = model.predict([features])
        if prediction[0] == 1:
            st.error("### Risk Level: Positive for Lung Cancer")
        else:
            st.success("### Risk Level: Negative")

elif selected_disease == "Breast Cancer Prediction":
    st.write("### Clinical Biopsy Features")
    features_bc = ["radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
                   "compactness_mean", "concavity_mean", "concave points_mean", "symmetry_mean", "fractal_dimension_mean",
                   "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
                   "compactness_se", "concavity_se", "concave points_se", "symmetry_se", "fractal_dimension_se",
                   "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
                   "compactness_worst", "concavity_worst", "concave points_worst", "symmetry_worst", "fractal_dimension_worst"]
    
    inputs_bc = []
    b_cols = st.columns(5)
    for i, f in enumerate(features_bc):
        inputs_bc.append(b_cols[i % 5].number_input(f, format="%.4f"))
        
    if st.button("Perform Malignancy Check"):
        model = load_model(models[selected_disease])
        prediction = model.predict([inputs_bc])
        if prediction[0] == 1:
            st.error("### Diagnosis: Malignant (Cancerous)")
        else:
            st.success("### Diagnosis: Benign (Non-Cancerous)")


