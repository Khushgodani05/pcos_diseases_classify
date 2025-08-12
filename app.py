import streamlit as st
import numpy as np
import joblib

# Load model
pipeline = joblib.load("../PCOS_project.pkl")

# Set Streamlit config
st.set_page_config(page_title="PCOS Prediction App", layout="centered")

# Inject custom CSS for blue theme
st.markdown("""
    <style>
        body {
            background-color: white;
        }
        .main {
            background-color: white;
        }
        h1, h2, h3 {
            color: #1F4E79;
        }
        .stForm {
            background: #f0f8ff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,255,0.05);
        }
        .prediction-box {
            padding: 1.5rem;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📝 Patient Form"])

# -------------------- HOME PAGE --------------------
if page == "🏠 Home":
    st.title("💊 Understanding Polycystic Ovary Syndrome (PCOS)")

    st.markdown("""
    ## 🌸 What is PCOS?
    **Polycystic Ovary Syndrome (PCOS)** is a hormonal disorder affecting women during their reproductive years. It involves problems with ovulation, elevated androgen levels, and enlarged ovaries containing follicles.

    ## ⚠️ Why It Matters
    PCOS can increase your risk of:
    - Infertility
    - Metabolic syndrome
    - Type 2 diabetes
    - Cardiovascular disease
    - Depression and anxiety

    ## 🩺 Common Symptoms
    - Irregular or missed periods
    - Excess facial or body hair
    - Weight gain or difficulty losing weight
    - Acne or oily skin
    - Hair thinning or baldness

    ## 🧪 Diagnosis & Treatment
    Diagnosis is done through blood tests and ultrasound. Treatments include:
    - Lifestyle changes (healthy diet, regular exercise)
    - Hormonal medications
    - Diabetes medications

    ---
    🔍 This application uses a machine learning model to help assess your PCOS risk based on clinical and lifestyle data.
    """)

# -------------------- FORM PAGE --------------------
elif page == "📝 Patient Form":
    st.title("📝 PCOS Prediction Form")

    st.markdown("Please fill in your information accurately:")

    with st.form("pcos_form"):
        age = st.number_input("Age (yrs)", min_value=10, max_value=60)
        weight = st.number_input("Weight (Kg)", min_value=30.0)
        height = st.number_input("Height (Cm)", min_value=100.0)
        blood_group = st.selectbox("Blood Group (code)", options=[11, 12, 13, 14, 15])
        pulse = st.number_input("Pulse rate (bpm)", min_value=30)
        rr = st.number_input("Respiratory Rate (breaths/min)", min_value=10)
        hb = st.number_input("Hemoglobin (g/dl)", min_value=5.0)
        cycle_type = st.selectbox("Cycle (R/I)", options=[1, 2])
        cycle_len = st.number_input("Cycle length (days)", min_value=1)
        marriage_years = st.number_input("Marriage Status (Years)", min_value=0)
        pregnant = st.selectbox("Pregnant (Y/N)", options=[0, 1])
        abortions = st.number_input("Number of Abortions", min_value=0)
        beta_hcg_1 = st.number_input("I beta-HCG (mIU/mL)")
        beta_hcg_2 = st.number_input("II beta-HCG (mIU/mL)")
        fsh = st.number_input("FSH (mIU/mL)")
        lh = st.number_input("LH (mIU/mL)")
        hip = st.number_input("Hip (inch)")
        waist = st.number_input("Waist (inch)")
        tsh = st.number_input("TSH (mIU/L)")
        amh = st.number_input("AMH (ng/mL)")
        prl = st.number_input("PRL (ng/mL)")
        vit_d3 = st.number_input("Vitamin D3 (ng/mL)")
        prg = st.number_input("PRG (ng/mL)")
