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
#       GPT-4 PROMPTS
# =========================

def get_gift_recommendations(occasion, budget, recipient):
    """
    - Assumes the user is ADVANCED in their interests.
    - Avoids generic or beginner-level gear.
    - Focuses on pro-level, premium, or specialized items (4+ star reviews).
    - Provides exactly 3 unique items.
    - Budget is a guideline (Low < $50, Medium $50-$200, Big Spender > $200).
    """

    prompt = f"""
You are an expert gift advisor. The user is advanced in their interests.
Recipient: {recipient}
Occasion: {occasion}
Budget: {budget} (Low < $50, Medium $50-$200, Big Spender > $200)

Return exactly 3 unique, high-quality, and high-review (4+ stars) Amazon items 
that match the recipient's interests (no beginner or generic gear).

Format:
Gift Name: [Product name here]
"""

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    gift_ideas = []
    for line in response.choices[0].message.content.split("\n"):
        if line.startswith("Gift Name:"):
            gift_name = line.replace("Gift Name:", "").strip()
            gift_ideas.append((gift_name, generate_amazon_search_link(gift_name)))

    return gift_ideas[:3]

def get_experiences(occasion, budget, recipient):
    """
    - Assumes the user is advanced in their interests.
    - Suggests exactly 2 experiences with only domain-level homepage links.
    """

    prompt = f"""
You are an expert experience curator. The user is advanced in their interests.
Recipient: {recipient}
Occasion: {occasion}
Budget: {budget}

Return exactly 2 unique experiences, advanced-level or specialized.
Use only domain-level homepage links (e.g., 'Website: https://www.stubhub.com').

Format:
Experience Suggestion: [one line describing the idea]
Website: [domain homepage link only]
"""

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    experiences = []
    suggestion, site = None, None

    lines = response.choices[0].message.content.split("\n")
    for line in lines:
        if line.startswith("Experience Suggestion:"):
            suggestion = line.replace("Experience Suggestion:", "").strip()
        elif line.startswith("Website:"):
            match = re.search(r"(https?://[^/]+)", line.replace("Website:", "").strip())
            site = match.group(1) if match else None

        if suggestion and site:
            experiences.append((suggestion, site))
            suggestion, site = None, None

    return experiences[:2]

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

/* Inputs & Dropdowns */
.stTextInput, .stSelectbox {
    background: #222222;
    color: white;
    border-radius: 8px;
    padding: 10px;
    font-size: 1.1em;
}
.stTextInput:hover, .stSelectbox:hover {
    border-color: #ffffff;
}

/* Button */
.stButton>button {
    background-color: white !important;
    color: black !important;
    font-weight: bold;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 1.2em;
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    background-color: #dddddd !important;
}

/* Result Cards */
.result-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1>Find the perfect gift</h1>
    <em>In seconds.</em>
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

            gift_ideas = get_gift_recommendations(occasion, budget, recipient)
            experiences = get_experiences(occasion, budget, recipient)

            st.subheader("✨ AI-Generated Gift Suggestions (Amazon):")
            for idea, link in gift_ideas:
                st.markdown(f"<div class='result-card'><strong>🎁 {idea}</strong><br><a href='{link}'>🔗 Find on Amazon</a></div>", unsafe_allow_html=True)

            st.subheader("🌟 Unique Experiences")
            for suggestion, site in experiences:
                st.markdown(f"<div class='result-card'><strong>{suggestion}</strong><br><a href='{site}'>🔗 Visit Website</a></div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a recipient description.")
