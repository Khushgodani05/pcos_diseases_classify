import streamlit as st
import numpy as np
import joblib
import google.generativeai as genai

# --- Load model ---
pipeline = joblib.load("PCOS_project.pkl")

# --- Gemini setup ---
GEMINI_API_KEY = "AIzaSyC5xZUT-JlaAcI2Ufg7ni0mewfqFgRNkGQ"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- Custom CSS ---
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    .section-header {
        background-color: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #667eea;
        margin: 1.5rem 0 1rem 0;
        border-radius: 0 8px 8px 0;
        color:black;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
    }
    
    .info-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #e9ecef;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-text {
        color: #856404;
        font-weight: 500;
        margin: 0;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #51cf66, #40c057);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
    
    .tips-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin-top: 1rem;
    }
    
    .feature-box {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        text-align: center;
        color:black;
    }
    
    .feature-icon {
        font-size: 2rem;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- Streamlit setup ---
st.set_page_config(
    page_title="PCOS Risk Assessment", 
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header ---
st.markdown("""
<div class="header-container">
    <h1 class="header-title">PCOS Risk Assessment</h1>
    <p class="header-subtitle">A comprehensive self-assessment tool for Polycystic Ovary Syndrome risk evaluation</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.markdown("### Navigation Menu")
page = st.sidebar.radio(
    "Select a section:", 
    ["Home & Information", "Risk Assessment", "Health Recommendations"],
    index=0
)

# --- Session init ---
if 'prediction' not in st.session_state:
    st.session_state.prediction = None

# --- Page 1: Home ---
if page == "Home & Information":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h2 style="color: #2c3e50; margin-bottom: 1rem;">Understanding PCOS</h2>
            <p style="font-size: 1.1rem; line-height: 1.6; color: #555;">
                Polycystic Ovary Syndrome (PCOS) is a hormonal disorder affecting reproductive-aged women. 
                It's characterized by irregular menstrual periods, excess hormone production, and enlarged 
                ovaries with small cysts.
            </p>
            <p style="font-size: 1.1rem; line-height: 1.6; color: #555;">
                Early detection and lifestyle modifications can significantly improve outcomes and quality of life 
                for women with PCOS.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
            <p class="warning-text">
                <strong>Medical Disclaimer:</strong> This tool is for educational purposes only and does not 
                replace professional medical advice. Please consult with a healthcare provider for proper 
                diagnosis and treatment.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("pcos_awareness.png", 
                caption="PCOS affects 1 in 10 women of reproductive age")
    
    st.markdown("### Why Use This Assessment Tool?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">⚡</div>
            <h4>Quick & Easy</h4>
            <p>Complete assessment in under 10 minutes with simple questions about your health.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🔒</div>
            <h4>Private & Secure</h4>
            <p>Your responses are processed locally and not stored or shared with third parties.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🎯</div>
            <h4>Personalized Results</h4>
            <p>Receive tailored recommendations based on your individual risk assessment.</p>
        </div>
        """, unsafe_allow_html=True)

# --- Page 2: Assessment Form ---
elif page == "Risk Assessment":
    st.markdown("## Complete Your Health Assessment")
    st.markdown("Please provide accurate information for the most reliable risk evaluation.")

    with st.form("pcos_assessment_form"):
        # Basic Information
        st.markdown("""
        <div class="section-header">
            <h3 class="section-title">Basic Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age (years)", min_value=10, max_value=60, value=25)
        with col2:
            weight = st.number_input("Weight (kg)", min_value=30.0, value=60.0, step=0.1)
        with col3:
            height = st.number_input("Height (cm)", min_value=100.0, value=160.0, step=0.1)

        # Vital Signs & Hormones
        st.markdown("""
        <div class="section-header">
            <h3 class="section-title">Vital Signs & Hormone Levels</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pulse = st.number_input("Pulse Rate (bpm)", value=72, min_value=40, max_value=200)
            fsh = st.number_input("FSH Level", value=0.0, step=0.1, help="Follicle Stimulating Hormone")
            amh = st.number_input("AMH Level", value=0.0, step=0.1, help="Anti-Müllerian Hormone")
            rbs = st.number_input("Blood Sugar (RBS)", value=0.0, step=0.1, help="Random Blood Sugar")
        
        with col2:
            rr = st.number_input("Respiratory Rate (per min)", value=16, min_value=8, max_value=40)
            lh = st.number_input("LH Level", value=0.0, step=0.1, help="Luteinizing Hormone")
            prl = st.number_input("Prolactin (PRL)", value=0.0, step=0.1)
            vit_d3 = st.number_input("Vitamin D3", value=0.0, step=0.1)
        
        with col3:
            hb = st.number_input("Hemoglobin (Hb)", value=12.0, step=0.1)
            tsh = st.number_input("TSH Level", value=0.0, step=0.1, help="Thyroid Stimulating Hormone")
            prg = st.number_input("Progesterone (PRG)", value=0.0, step=0.1)
            bhcg1 = st.number_input("β-HCG I", value=0.0, step=0.1)
        
        col1, col2 = st.columns(2)
        with col1:
            bhcg2 = st.number_input("β-HCG II", value=0.0, step=0.1)

        # Menstrual Health
        st.markdown("""
        <div class="section-header">
            <h3 class="section-title">Menstrual Health</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cycle = st.selectbox("Menstrual Cycle Regularity", 
                               options=[2, 1], 
                               format_func=lambda x: "Regular" if x == 2 else "Irregular",
                               index=0)
        with col2:
            cycle_len = st.number_input("Cycle Length (days)", value=28, min_value=15, max_value=60)
        with col3:
            marriage_yrs = st.number_input("Years of Marriage (if applicable)", value=0, min_value=0)
        
        col1, col2 = st.columns(2)
        with col1:
            pregnant = st.selectbox("Currently Pregnant", 
                                  options=[0, 1], 
                                  format_func=lambda x: "No" if x == 0 else "Yes")
        with col2:
            abortions = st.number_input("Number of Miscarriages", value=0, min_value=0)

        # Physical Characteristics
        st.markdown("""
        <div class="section-header">
            <h3 class="section-title">Physical Characteristics & Symptoms</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            hip = st.number_input("Hip Circumference (cm)", value=90.0, step=0.1)
            weight_gain = st.selectbox("Recent Weight Gain", 
                                     options=[0, 1], 
                                     format_func=lambda x: "No" if x == 0 else "Yes")
            skin_dark = st.selectbox("Dark Skin Patches", 
                                   options=[0, 1], 
                                   format_func=lambda x: "No" if x == 0 else "Yes")
        
        with col2:
            waist = st.number_input("Waist Circumference (cm)", value=75.0, step=0.1)
            hair_growth = st.selectbox("Excess Facial Hair", 
                                     options=[0, 1], 
                                     format_func=lambda x: "No" if x == 0 else "Yes")
            hair_loss = st.selectbox("Hair Thinning/Loss", 
                                   options=[0, 1], 
                                   format_func=lambda x: "No" if x == 0 else "Yes")
        
        with col3:
            pimples = st.selectbox("Frequent Acne", 
                                 options=[0, 1], 
                                 format_func=lambda x: "No" if x == 0 else "Yes")
            fast_food = st.selectbox("Regular Fast Food Consumption", 
                                   options=[0, 1], 
                                   format_func=lambda x: "No" if x == 0 else "Yes")
            exercise = st.selectbox("Regular Exercise", 
                                  options=[0, 1], 
                                  format_func=lambda x: "No" if x == 0 else "Yes")

        # Clinical Measurements
        st.markdown("""
        <div class="section-header">
            <h3 class="section-title">Clinical Measurements (if available)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            bp_sys = st.number_input("Systolic BP", value=120, min_value=80, max_value=200)
            foll_l = st.number_input("Left Ovary Follicle Count", value=0, min_value=0)
            fsize_l = st.number_input("Left Ovary Follicle Size", value=0.0, step=0.1)
        
        with col2:
            bp_dia = st.number_input("Diastolic BP", value=80, min_value=50, max_value=120)
            foll_r = st.number_input("Right Ovary Follicle Count", value=0, min_value=0)
            fsize_r = st.number_input("Right Ovary Follicle Size", value=0.0, step=0.1)
        
        with col3:
            blood_group = st.selectbox("Blood Group", 
                                     options=[11, 12, 13, 14, 15], 
                                     format_func=lambda x: {11: "A+", 12: "A-", 13: "B+", 14: "B-", 15: "O+"}[x])
            endo = st.number_input("Endometrium Thickness", value=0.0, step=0.1)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Analyze My Risk", use_container_width=True)

    if submitted:
        # Prepare data for prediction
        data = np.array([[age, weight, height, blood_group, pulse, rr, hb, cycle, cycle_len, marriage_yrs,
                          pregnant, abortions, bhcg1, bhcg2, fsh, lh, hip, waist, tsh, amh, prl, vit_d3, prg,
                          rbs, weight_gain, hair_growth, skin_dark, hair_loss, pimples, fast_food, exercise,
                          bp_sys, bp_dia, foll_l, foll_r, fsize_l, fsize_r, endo]])

        result = pipeline.predict(data)[0]
        st.session_state.prediction = result

        if result == 1:
            st.markdown("""
            <div class="risk-high">
                <h3>⚠️ Elevated Risk Detected</h3>
                <p style="font-size: 1.1rem; margin: 0;">
                    Based on your responses, you may have an increased risk for PCOS. 
                    We recommend consulting with a healthcare provider for comprehensive evaluation and testing.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="risk-low">
                <h3>✅ Low Risk Assessment</h3>
                <p style="font-size: 1.1rem; margin: 0;">
                    Your responses suggest a lower risk for PCOS. Continue maintaining your healthy lifestyle habits!
                </p>
            </div>
            """, unsafe_allow_html=True)

# --- Page 3: Recommendations ---
elif page == "Health Recommendations":
    st.markdown("## Personalized Health Recommendations")

    if st.session_state.prediction is None:
        st.markdown("""
        <div class="warning-box">
            <p class="warning-text">
                Please complete your risk assessment first to receive personalized recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Take Assessment Now"):
            st.session_state.page = "Risk Assessment"
            st.rerun()
    else:
        # Generate AI recommendations
        if st.session_state.prediction == 1:
            prompt = """Provide 5 evidence-based lifestyle and health recommendations for someone 
                       who may be at risk for PCOS. Focus on diet, exercise, stress management, 
                       and general wellness. Make the advice practical and actionable."""
        else:
            prompt = """Provide 5 preventive health recommendations to maintain hormonal balance 
                       and reduce the risk of developing PCOS. Focus on sustainable lifestyle 
                       habits for long-term health."""

        with st.spinner("Generating personalized recommendations..."):
            response = model.generate_content(prompt)

        st.markdown("""
        <div class="tips-container">
            <h3 style="color: #28a745; margin-bottom: 1rem;">Your Personalized Recommendations</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(response.text)

        st.markdown("""
        <div class="warning-box" style="margin-top: 2rem;">
            <p class="warning-text">
                <strong>Important:</strong> These recommendations are AI-generated suggestions for general wellness. 
                Always consult with your healthcare provider before making significant changes to your health regimen.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional resources
        st.markdown("### Additional Resources")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **When to See a Doctor:**
            - Irregular or missed periods
            - Difficulty conceiving
            - Unexplained weight gain
            - Excessive hair growth or loss
            - Persistent acne
            """)
        
        with col2:
            st.markdown("""
            **Emergency Signs:**
            - Severe pelvic pain
            - Heavy bleeding
            - Signs of diabetes
            - Severe mood changes
            - Difficulty breathing
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>PCOS Risk Assessment Tool</strong> | For educational purposes only | 
    Always consult healthcare professionals for medical advice</p>
</div>
""", unsafe_allow_html=True)