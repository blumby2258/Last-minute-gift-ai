import streamlit as st
import openai
import os
import re
import time
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
#   AMAZON LINK GENERATION
# =========================
AMAZON_AFFILIATE_TAG = "blumby20-20"

def generate_amazon_search_link(product_name):
    """Generate a basic Amazon search URL from the gift name, with affiliate tag."""
    query = re.sub(r'[^a-zA-Z0-9 ]', '', product_name).replace(" ", "+")
    return f"https://www.amazon.com/s?k={query}&tag={AMAZON_AFFILIATE_TAG}"

# =========================
#         UI
# =========================

st.set_page_config(
    page_title="Impulse: Find the Perfect Gift",
    page_icon="🎁",
    layout="wide"
)

custom_css = """
<style>
/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');

/* Background */
body {
    background-color: #000000;
    color: #ffffff;
    font-family: 'Poppins', sans-serif;
}

/* Starry background */
.stApp {
    background: url('https://source.unsplash.com/1600x900/?stars,space') no-repeat center center fixed;
    background-size: cover;
}

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 80px 20px;
    color: white;
}
.hero-section h1 {
    font-size: 3.5em;
    font-weight: 600;
}
.hero-section em {
    font-style: italic;
    font-size: 1.2em;
    opacity: 0.8;
}
.hero-section p {
    margin-top: 10px;
    font-size: 1em;
    opacity: 0.7;
}

/* Input Field Styling */
.stTextInput, .stSelectbox {
    background: #000000;  /* White background */
    color: #000000;  /* Black text */
    border-radius: 8px;
    padding: 12px;
    font-size: 1.1em;
    border: 1px solid #ffcc00;
}
.stTextInput::placeholder, .stSelectbox::placeholder {
    color: #777777;
}
.stTextInput:hover, .stSelectbox:hover {
    border-color:#000000;
    box-shadow: 0px 0px 8px rgba(255, 255, 255, 0.2);
}

/* Labels for Inputs */
div[data-baseweb="select"] label, .stTextInput label {
    color: #ffffff !important;  /* black label text */
}

/* Primary Button */
.stButton>button {
    background-color: #ffcc00 !important;
    color: #000000 !important;
    font-weight: bold;
    border-radius: 12px;
    padding: 14px 30px;
    font-size: 1.2em;
    border: none;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
}
.stButton>button:hover {
    background-color: #dddddd !important;
    transform: scale(1.05);
}

/* Result Cards */
.result-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 18px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(255, 255, 255, 0.1);
    margin-bottom: 15px;
}
.result-card a {
    color: #ffffff;
    text-decoration: none;
    font-weight: 500;
}
.result-card a:hover {
    text-decoration: underline;
}

/* Affiliate Disclosure */
.affiliate-disclosure {
    font-size: 0.9em;
    color: #bbbbbb;
    text-align: center;
    margin-top: 30px;
    padding: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1>The Gift Finder</h1>
    <em></em>
    <p>Your personalized AI Gift Agent</p>
</div>
""", unsafe_allow_html=True)

# User Inputs
st.subheader("🎯 Find the Perfect Gift in Seconds")

with st.container():
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        occasion = st.selectbox("🎉 Select an Occasion", ["Birthday", "Anniversary", "Holiday", "Wedding", "New Baby"])
    
    with col2:
        budget = st.selectbox("💰 Select Budget", ["Low", "Medium", "Big Spender"])
    
    with col3:
        recipient = st.text_input("👤 Describe the Recipient", placeholder="e.g., 'My friend who is a passionate photographer'")

# Generate Gift Ideas
if st.button("🔍 Find My Gift!"):
    if recipient.strip():
        with st.spinner("🎁 Finding the perfect gift..."):
            time.sleep(2)

            # Placeholder for results
            st.subheader("✨ AI-Generated Gift Suggestions (Amazon):")
            st.markdown("""
                <div class="result-card">
                    <strong>🎁 Example Gift 1</strong><br>
                    <a href="#">🔗 Find on Amazon</a>
                </div>
                <div class="result-card">
                    <strong>🎁 Example Gift 2</strong><br>
                    <a href="#">🔗 Find on Amazon</a>
                </div>
                <div class="result-card">
                    <strong>🎁 Example Gift 3</strong><br>
                    <a href="#">🔗 Find on Amazon</a>
                </div>
            """, unsafe_allow_html=True)
            
            st.subheader("🌟 Unique Experiences (Online or In-Person)")
            st.markdown("""
                <div class="result-card">
                    <strong>Experience 1</strong><br>
                    <a href="#">🔗 Visit Website</a>
                </div>
                <div class="result-card">
                    <strong>Experience 2</strong><br>
                    <a href="#">🔗 Visit Website</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a recipient description.")

# Amazon Affiliate Disclosure
st.markdown("""
<div class="affiliate-disclosure">
    <p><strong>Disclosure:</strong> As an Amazon Associate, we earn from qualifying purchases. Clicking our links 
    may result in a commission, helping us continue providing this service. Thank you!</p>
</div>
""", unsafe_allow_html=True)
