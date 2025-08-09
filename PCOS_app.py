import streamlit as st
import numpy as np
import joblib
import google.generativeai as genai

# --- Load model ---
pipeline = joblib.load("PCOS_project.pkl")

# --- Gemini setup ---
GEMINI_API_KEY = "AIzaSyAtZmc437LrsCmYq6djxBNl_ZMG80Txreo"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- Streamlit setup ---
st.set_page_config(page_title="PCOS Risk Checker", layout="wide")

# --- Branding ---
st.markdown("""
    <h1 style='text-align: center; color: #006666;'>🧬 PCOS Risk Self-Check</h1>
    <p style='text-align: center; font-size: 18px;'>Answer a few questions to see if you're at risk for Polycystic Ovary Syndrome</p>
    <hr>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("📂 Menu")
page = st.sidebar.radio("Choose a page", ["🏠 Welcome", "📝 Start Self-Check", "💬 Wellness Tips"])

# --- Page 1: Home ---
if page == "🏠 Welcome":
    st.image("https://www.cdc.gov/pcos/images/PCOS_infographic_social.jpg", use_container_width=True)
    st.markdown("""
        ## What is PCOS?
        Polycystic Ovary Syndrome (PCOS) is a health condition that affects hormone levels, periods, and fertility. 

        This tool helps you check your risk by answering some simple questions. Results are private and for your understanding.

        ⚠️ **This is not a diagnosis.** Please talk to a doctor for medical advice.

        ---
        ### Why use this tool?
        - Easy questions you can answer yourself
        - Instant results
        - AI tips for better health
    """)

# --- Session init ---
if 'prediction' not in st.session_state:
    st.session_state.prediction = None

# --- Page 2: Form ---
elif page == "📝 Start Self-Check":
    st.subheader("🩺 Tell us a bit about your health")

    with st.form("pcos_form"):
        st.markdown("### 🧍 Your Body")
        col1, col2, col3 = st.columns(3)
        age = col1.number_input("Age (years)", 10, 60)
        weight = col2.number_input("Weight (kg)", 30.0)
        height = col3.number_input("Height (cm)", 100.0)

        st.markdown("### 💓 Vitals & Hormones")
        col1, col2, col3 = st.columns(3)
        pulse = col1.number_input("Pulse rate (bpm)")
        rr = col2.number_input("Breathing rate (per min)")
        hb = col3.number_input("Hemoglobin (Hb)")
        fsh = col1.number_input("FSH level")
        lh = col2.number_input("LH level")
        tsh = col3.number_input("TSH level")
        amh = col1.number_input("AMH level")
        prl = col2.number_input("Prolactin (PRL)")
        prg = col3.number_input("Progesterone (PRG)")
        rbs = col1.number_input("Blood sugar (RBS)")
        vit_d3 = col2.number_input("Vitamin D3")
        bhcg1 = col3.number_input("β-HCG I")
        bhcg2 = col1.number_input("β-HCG II")

        st.markdown("### 🩸 Menstrual Info")
        col1, col2, col3 = st.columns(3)
        cycle = col1.selectbox("Are your periods regular?", [1, 2], format_func=lambda x: "No" if x == 1 else "Yes")
        cycle_len = col2.number_input("Cycle length (days)")
        marriage_yrs = col3.number_input("Years married (if applicable)")
        pregnant = col1.selectbox("Are you currently pregnant?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        abortions = col2.number_input("Number of miscarriages (if any)")

        st.markdown("### 🧘 Lifestyle & Physical Signs")
        col1, col2, col3 = st.columns(3)
        hip = col1.number_input("Hip size (cm)")
        waist = col2.number_input("Waist size (cm)")
        weight_gain = col3.selectbox("Gained weight recently?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        hair_growth = col1.selectbox("Do you have facial hair growth?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        skin_dark = col2.selectbox("Dark patches on skin?", [0, 1])
        hair_loss = col3.selectbox("Hair fall or thinning?", [0, 1])
        pimples = col1.selectbox("Frequent acne or pimples?", [0, 1])
        fast_food = col2.selectbox("Eat fast food often?", [0, 1])
        exercise = col3.selectbox("Do you exercise regularly?", [0, 1])

        st.markdown("### 🩻 Ultrasound & BP (if known)")
        col1, col2, col3 = st.columns(3)
        bp_sys = col1.number_input("Blood Pressure - Systolic")
        bp_dia = col2.number_input("Blood Pressure - Diastolic")
        foll_l = col3.number_input("Left Ovary Follicles Count")
        foll_r = col1.number_input("Right Ovary Follicles Count")
        fsize_l = col2.number_input("Left Ovary Follicle Size")
        fsize_r = col3.number_input("Right Ovary Follicle Size")
        endo = col1.number_input("Endometrium Thickness")

        blood_group = col2.selectbox("Blood Group", [11, 12, 13, 14, 15], format_func=lambda x: {11: "A+", 12: "A-", 13: "B+", 14: "B-", 15: "O+"}[x])

        submitted = st.form_submit_button("🔍 Check My Risk")

    if submitted:
        data = np.array([[age, weight, height, blood_group, pulse, rr, hb, cycle, cycle_len, marriage_yrs,
                          pregnant, abortions, bhcg1, bhcg2, fsh, lh, hip, waist, tsh, amh, prl, vit_d3, prg,
                          rbs, weight_gain, hair_growth, skin_dark, hair_loss, pimples, fast_food, exercise,
                          bp_sys, bp_dia, foll_l, foll_r, fsize_l, fsize_r, endo]])

        result = pipeline.predict(data)[0]
        st.session_state.prediction = result

        if result == 1:
            st.error("⚠️ Based on your answers, you may be at **risk for PCOS**. We recommend seeing a doctor for proper tests.")
        else:
            st.success("✅ You're likely at **low risk for PCOS**. Keep up your healthy habits!")

# --- Page 3: Tips ---
elif page == "💬 Wellness Tips":
    st.subheader("🌿 Health Tips Just for You")

    if st.session_state.prediction is None:
        st.warning("⚠️ Please complete your self-check first.")
    else:
        if st.session_state.prediction == 1:
            prompt = "I may have PCOS. Give me 5 gentle health and lifestyle tips I can follow at home."
        else:
            prompt = "Give me 5 healthy habits to keep hormones balanced and avoid PCOS."

        with st.spinner("Getting advice just for you..."):
            response = model.generate_content(prompt)

        st.markdown("### 💡 Your Tips:")
        st.markdown(response.text)

        st.caption("These are AI-generated suggestions. Please follow your doctor's advice for treatment.")
