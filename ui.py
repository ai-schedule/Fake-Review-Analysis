import streamlit as st
import matplotlib.pyplot as plt

# ---------------- STYLE ----------------
def apply_style():
    st.markdown("""
    <style>

    /* MAIN BACKGROUND (UNCHANGED) */
    .stApp {
        background-color: #8FC7A6;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #9FB3A6 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #1B4332 !important;
    }

    /* CONTAINER */
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
    }

    /* TITLE */
    h1 {
        text-align: left;
        font-family: 'Poppins', sans-serif;
        font-style: italic;
        font-weight: 500;
        color: #1B4332;
    }

    /* SLOGAN */
    .slogan {
        text-align: center;
        font-size: 22px;
        font-weight: 600;
        letter-spacing: 2px;
        color: #1B4332;
    }

    /* ---------- GLASS EFFECT ---------- */
    .stTextInput, .stTextArea, .stButton {
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(6px);
        border-radius: 12px;
        padding: 6px;
    }

    /* INPUT BOX */
    input, textarea {
        background: rgba(255,255,255,0.35) !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px !important;
    }

    /* BUTTON */
    button {
        background-color: rgba(255,255,255,0.4) !important;
        color: #1B4332 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    button:hover {
        background-color: rgba(255,255,255,0.6) !important;
    }

    /* TITLES */
    .custom-title {
        font-family: 'Poppins', sans-serif;
        font-style: italic;
        font-weight: 600;
        font-size: 24px;
        color: #1B4332;
        margin-top: 10px;
    }

    /* TEXT */
    .custom-text {
        font-family: 'Times New Roman', serif;
        font-style: italic;
        font-size: 17px;
        color: #2F4F4F;
    }

    /* TIP */
    .tip {
        text-align: left;
        font-size: 16px;
        color: #1B4332;
        margin-top: 20px;
    }

    </style>
    """, unsafe_allow_html=True)


# ---------------- HEADER ----------------
def render_header():
    st.markdown(
        "<h1>🛍️ Fake Review Detection System</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="slogan">DETECT THE FAKE</div>',
        unsafe_allow_html=True
    )


# ---------------- RESULT ----------------
def render_result(trust_score, fake_percent):
    st.subheader("🔍 Analysis Result")
    st.write(f"Fake Reviews: {round(fake_percent, 2)} %")
    st.write(f"Trust Score: {round(trust_score, 2)} / 100")


# ---------------- CHARTS ----------------
def render_charts(trust_score, fake_percent):
    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        ax1.pie(
            [fake_percent, 100 - fake_percent],
            labels=["Fake", "Genuine"],
            autopct='%1.1f%%'
        )
        fig1.set_size_inches(3.5, 3.5)
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        ax2.bar(["Trust", "Fake"], [trust_score, fake_percent])
        ax2.set_ylim(0, 100)
        fig2.set_size_inches(3.5, 3.5)
        st.pyplot(fig2)


# ---------------- EXPLANATION ----------------
def render_explanation(reasons):
    st.markdown('<div class="custom-title">📌 Explanation</div>', unsafe_allow_html=True)

    for r in reasons:
        st.markdown(f'<div class="custom-text">• {r}</div>', unsafe_allow_html=True)


# ---------------- CONCLUSION ----------------
def render_conclusion(trust_score):
    st.markdown('<div class="custom-title">🧠 Conclusion</div>', unsafe_allow_html=True)

    if trust_score >= 75:
        st.markdown('<div class="custom-text">✔ Product looks trustworthy</div>', unsafe_allow_html=True)
    elif trust_score >= 60:
        st.markdown('<div class="custom-text">⚠ Moderate trust. Check carefully</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="custom-text">❌ High risk product. Many fake reviews detected</div>', unsafe_allow_html=True)


# ---------------- TIP ----------------
def render_tip():
    st.markdown("""
    <div class="tip">
    💡 Tip: Avoid repetitive or overly emotional reviews.
    </div>
    """, unsafe_allow_html=True)