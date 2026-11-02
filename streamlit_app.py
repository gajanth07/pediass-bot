import streamlit as st
import random

# Page Configuration
st.set_page_config(page_title="NEET SS Pediatrics Master", page_icon="🩺", layout="centered")

# Custom CSS Styling for Elite Coaching Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #0f4c81; color: white; }
    .stButton>button:hover { background-color: #1a73e8; color: white; }
    .vignette-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #0f4c81; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .explanation-box { background-color: #e2e8f0; padding: 15px; border-radius: 8px; border-left: 5px solid #334155; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Score Tracking
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'questions_attempted' not in st.session_state:
    st.session_state.questions_attempted = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'current_q' not in st.session_state:
    st.session_state.current_q = None

# High-Yield Question Bank (Nelson 22nd / ISPN / NNF Aligned)
QUESTION_BANK = [
    {
        "id": "q1",
        "domain": "Neonatology (NNF / AIIMS Protocol)",
        "vignette": "A 28-week preterm neonate delivered following emergency LSCS for severe preeclampsia develops respiratory distress within 2 hours of life. Intubated and placed on mechanical ventilation. On day 3, the infant develops sudden right-sided desaturation, decreased breath sounds, and transillumination revealing a bright glow on the right hemithorax.",
        "options": {
            "A": "Immediate needle decompression / intercostal chest drain",
            "B": "Switch to High-Frequency Oscillatory Ventilation (HFOV)",
            "C": "Emergency echocardiogram for PPHN confirmation",
            "D": "Urgent contrast CT chest"
        },
        "answer": "A",
        "explanation": "✅ **CORRECT (+4 Marks)**\n\n**Protocol Verification:** Sudden clinical deterioration plus a bright transillumination glow in a ventilated preterm infant is pathognomonic for **tension pneumothorax**. This is a surgical/clinical emergency requiring immediate needle aspiration or chest tube insertion rather than waiting for X-ray confirmation."
    },
    {
        "id": "q2",
        "domain": "Pediatric Nephrology (ISPN Guidelines)",
        "vignette": "A 6-year-old boy presents with generalized anasarca, heavy proteinuria (5.2 g/24h), and serum albumin of 1.8 g/dL. He is started on standard prednisolone therapy (60 mg/m²/day). By week 4, his urine protein remains persistently 3+ to 4+, and he fails to enter remission.",
        "options": {
            "A": "Steroid-Dependent Nephrotic Syndrome; add Levamisole",
            "B": "Steroid-Resistant Nephrotic Syndrome; perform renal biopsy and genetic panel (NPHS1/NPHS2)",
            "C": "Frequently Relapsing Nephrotic Syndrome; give pulse methylprednisolone",
            "D": "Congenital Nephrotic Syndrome; start Cyclophosphamide"
        },
        "answer": "B",
        "explanation": "✅ **CORRECT (+4 Marks)**\n\n**ISPN Protocol Verification:** Failure to achieve remission after 4 weeks of daily high-dose steroids defines **Steroid-Resistant Nephrotic Syndrome (SRNS)**. Mandatory renal tissue evaluation (biopsy) and genetic testing for podocyte mutations are indicated before starting second-line calcineurin inhibitors."
    },
    {
        "id": "q3",
        "domain": "Inborn Errors of Metabolism (Nelson Metabolic)",
        "vignette": "A term neonate born to non-consanguineous parents develops lethargy and seizures on day 3 of life. Labs show severe high anion gap metabolic acidosis, hyperammonemia, and ketosis. Urine analysis reveals a distinct sweet, caramel-like / 'maple syrup' odor.",
        "options": {
            "A": "Ornithine transcarbamylase (OTC)",
            "B": "Branched-chain alpha-ketoacid dehydrogenase complex",
            "C": "Galactose-1-phosphate uridylyltransferase",
            "D": "Glucose-6-phosphatase"
        },
        "answer": "B",
        "explanation": "✅ **CORRECT (+4 Marks)**\n\n**Nelson Metabolic Verification:** This is classic **Maple Syrup Urine Disease (MSUD)** caused by deficiency of the mitochondrial branched-chain alpha-ketoacid dehydrogenase complex, leading to neurotoxic accumulation of Leucine, Isoleucine, and Valine."
    }
]

# App Header
st.title("🩺 NEET SS Pediatrics Master")
st.caption("AI-Powered Clinical Vignette Simulator | Nelson 22nd & Indian Protocols (ISPN/NNF/AIIMS)")

# Sidebar for Scoreboard & Navigation
with st.sidebar:
    st.header("📊 Score Dashboard")
    st.metric(label="Total Score", value=f"{st.session_state.score} Marks")
    st.metric(label="Questions Attempted", value=st.session_state.questions_attempted)
    
    if st.button("🔄 Reset Score"):
        st.session_state.score = 0
        st.session_state.questions_attempted = 0
        st.session_state.answered = False
        st.session_state.current_q = None
        st.rerun()

# Select or load a random question if none active
if st.session_state.current_q is None:
    st.session_state.current_q = random.choice(QUESTION_BANK)
    st.session_state.answered = False

q = st.session_state.current_q

# Display Domain & Vignette
st.markdown(f"### 🏷️ Domain: {q['domain']}")
st.markdown(f"""
<div class="vignette-box">
    <b>Clinical Scenario:</b><br><br>{q['vignette']}
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Form or radio options for answering
selected_option = st.radio(
    "Select your diagnostic management choice:",
    options=list(q['options'].keys()),
    format_func=lambda x: f"{x}) {q['options'][x]}",
    key=f"radio_{q['id']}"
)

col1, col2 = st.columns(2)

with col1:
    if not st.session_state.answered:
        if st.button("Submit Answer"):
            st.session_state.answered = True
            st.session_state.questions_attempted += 1
            if selected_option == q['answer']:
                st.session_state.score += 4
            else:
                st.session_state.score -= 1
            st.rerun()

with col2:
    if st.session_state.answered:
        if st.button("Next Question ➡️"):
            st.session_state.answered = False
            st.session_state.current_q = random.choice(QUESTION_BANK)
            st.rerun()

# Show feedback after submission
if st.session_state.answered:
    if selected_option == q['answer']:
        st.success(f"Selected Option: **{selected_option}** — Spot on, Doctor!")
    else:
        st.error(f"Selected Option: **{selected_option}** (-1 Mark). Correct Option was **{q['answer']}**.")
    
    st.markdown(f"""
    <div class="explanation-box">
        {q['explanation']}
    </div>
    """, unsafe_allow_html=True)
