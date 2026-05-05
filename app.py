import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

from model import load_model, analyze_multiple_reviews, generate_explanation
from preprocessing import clean_text
import ui   # 🔥 NEW

# Load model
model, tfidf = load_model()

# ---------------- SESSION STORAGE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "recent_links" not in st.session_state:
    st.session_state.recent_links = []

if "selected_link" not in st.session_state:
    st.session_state.selected_link = ""

# ---------------- APPLY UI ----------------
ui.apply_style()
ui.render_header()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Dashboard")

show_dashboard = st.sidebar.checkbox("Show Performance Analytics")

# -------- RECENT SEARCHES --------
st.sidebar.subheader("🔗 Recent Searches")

if st.session_state.recent_links:
    for link in st.session_state.recent_links:
        if st.sidebar.button(link):
            st.session_state.selected_link = link
else:
    st.sidebar.write("No recent links")

if show_dashboard:

    if st.session_state.history:

        st.sidebar.subheader("📋 Recent Results")
        for i, item in enumerate(st.session_state.history):
            st.sidebar.write(f"{i+1}. Trust: {item['trust']} | Fake: {item['fake']}%")

        st.sidebar.subheader("📈 Trust Score Trend")

        import matplotlib.pyplot as plt
        trust_values = [item["trust"] for item in st.session_state.history]

        fig, ax = plt.subplots()
        ax.plot(trust_values, marker='o')
        ax.set_ylim(0, 100)

        st.sidebar.pyplot(fig)

        st.sidebar.subheader("📊 Summary")

        avg_trust = sum(trust_values) / len(trust_values)
        st.sidebar.write(f"Average: {round(avg_trust, 2)}")
        st.sidebar.write(f"Highest: {max(trust_values)}")
        st.sidebar.write(f"Lowest: {min(trust_values)}")

        if st.sidebar.button("🗑 Clear History"):
            st.session_state.history = []
            st.sidebar.success("History cleared")

    else:
        st.sidebar.write("No data yet. Run analysis first.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("💡 Smart Tips")
    st.sidebar.write("✔ Avoid repeated phrases")
    st.sidebar.write("✔ Look for detailed reviews")
    st.sidebar.write("✔ Check both positive & negative feedback")

# ---------------- INPUT ----------------
product_link = st.text_input(
    "🔗 Enter Product Link (optional)",
    value=st.session_state.selected_link
)

reviews_input = st.text_area("📝 Paste Reviews (one per line)")

# ---------------- REVIEW EXTRACTION ----------------
def extract_reviews_from_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        reviews = []
        for p in soup.find_all("p"):
            text = p.get_text().strip()
            if len(text) > 50:
                reviews.append(text)

        return reviews[:10] if reviews else None

    except:
        return None

# ---------------- BUTTON ----------------
if st.button("🔍 Analyze Reviews"):

    reviews = []
    status = st.empty()

    # SAVE LINK
    if product_link.strip():
        if product_link not in st.session_state.recent_links:
            st.session_state.recent_links.insert(0, product_link)
            st.session_state.recent_links = st.session_state.recent_links[:5]

    # LINK LOGIC
    if product_link.strip():
        status.info("🔄 Extracting reviews from link...")
        time.sleep(1.2)

        extracted = extract_reviews_from_link(product_link)

        if extracted:
            status.success("✅ Reviews extracted successfully")
            time.sleep(1.2)
            reviews = extracted
        else:
            status.error("❌ Could not extract reviews. Please paste manually.")

    # FALLBACK
    if not reviews:
        if not reviews_input.strip():
            st.warning("⚠️ Please enter reviews manually.")
        else:
            reviews = [r.strip() for r in reviews_input.split("\n") if r.strip()]
            st.info(f"Using {len(reviews)} manually entered reviews")
            time.sleep(1)

    # ANALYSIS
    if reviews:
        status.info("📊 Analyzing reviews...")
        time.sleep(1.5)

        trust_score, fake_percent = analyze_multiple_reviews(
            model, tfidf, reviews, clean_text
        )

        # SAVE HISTORY
        st.session_state.history.insert(0, {
            "trust": round(trust_score, 2),
            "fake": round(fake_percent, 2)
        })

        st.session_state.history = st.session_state.history[:5]

        status.success("✅ Analysis completed")

        reasons = generate_explanation(fake_percent)

        # 🔥 UI FUNCTIONS USED
        ui.render_result(trust_score, fake_percent)
        ui.render_charts(trust_score, fake_percent)
        ui.render_explanation(reasons)
        ui.render_conclusion(trust_score)

# ---------------- FOOTER ----------------
st.markdown("---")
ui.render_tip()