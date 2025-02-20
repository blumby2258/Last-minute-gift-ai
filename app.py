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
    Always treat the user as ADVANCED in their interests.
    - Avoid generic or beginner gear.
    - Focus on pro-level, premium, or specialized items (4+ star reviews).
    - Provide exactly 3 unique items.
    Budget is just a guideline (Low < $50, Medium $50-$200, Big Spender > $200).
    We'll generate the final Amazon links ourselves.
    """

    prompt = f"""
You are an expert gift advisor. The user is advanced in their interests.
Recipient: {recipient}
Occasion: {occasion}
Budget: {budget} (Low < $50, Medium $50-$200, Big Spender > $200)

Return exactly 3 unique, advanced-level, and high-review (4+ stars) Amazon items 
that match the recipient's interests (no beginner or generic gear).

Format:
Gift Name: [Product name here]
(Exactly 3 items, no disclaimers.)
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
    Always treat the user as advanced. Suggest exactly 2 experiences.
    Must use only domain-level homepage links (no deeper paths).
    Format:
      Experience Suggestion: <short statement>
      Website: <domain homepage only>
    """

    prompt = f"""
You are an expert experience curator. The user is advanced in their interests.
Recipient: {recipient}
Occasion: {occasion}
Budget: {budget}

Return exactly 2 unique experiences, advanced-level or specialized.
Use only domain-level homepage links.
(no disclaimers, exactly 2 experiences)

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
            candidate_link = line.replace("Website:", "").strip()
            # If GPT tries "https://www.site.com/page", capture only "https://www.site.com"
            match = re.search(r"(https?://[^/]+)", candidate_link)
            site = match.group(1) if match else candidate_link

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

# NEW Dark Mode CSS
custom_css = """
<style>
/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

/* Global Styles - Dark Mode */
body {
    font-family: 'Poppins', sans-serif;
    background-color: #1B1B1B;
    color: #F2F2F2; /* Light text against dark background */
}

/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, #E74C3C, #F39C12);
    padding: 40px 20px;
    border-radius: 12px;
    text-align: center;
    color: #FFF;
}
.hero-section h1 {
    font-size: 3em;
    font-weight: bold;
    margin-bottom: 10px;
}
.hero-section p {
    font-size: 1.2em;
    opacity: 0.9;
}

/* Affiliate Disclosure */
.affiliate-disclosure {
    font-size: 0.9em;
    color: #BBBBBB;
    text-align: center;
    margin-top: 10px;
}

/* Inputs & Dropdowns */
.stTextInput, .stSelectbox {
    font-size: 1.1em;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #555555;
    background: #2A2A2A;
    color: #F2F2F2;
    transition: 0.2s ease-in-out;
}
.stTextInput:hover, .stSelectbox:hover {
    border-color: #E74C3C;
    transform: scale(1.02);
}

/* Button */
.stButton>button {
    background-color: #E74C3C !important;
    color: #FFF !important;
    font-weight: bold;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 1.2em;
    border: none;
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    background-color: #C0392B !important;
    transform: scale(1.05);
}

/* Result Cards */
.result-card {
    background: #2A2A2A;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 4px 12px rgba(255, 255, 255, 0.05);
    transition: transform 0.2s ease-in-out;
    display: block;
    margin-bottom: 15px;
}
.result-card:hover {
    transform: scale(1.02);
}
.result-card a {
    color: #F39C12;
    text-decoration: none;
    font-weight: 500;
}
.result-card a:hover {
    text-decoration: underline;
}

/* Streamlit Component Tweaks */
.reportview-container .main .block-container {
    color: #F2F2F2;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1>🎁 Impulse: Find the Perfect Gift in Seconds</h1>
    <p>AI-powered recommendations tailored to your needs – quick and easy!</p>
</div>
""", unsafe_allow_html=True)

# Affiliate Disclosure
st.markdown("""
<div class="affiliate-disclosure">
    <p><strong>Disclosure:</strong> As an Amazon Associate, we earn from qualifying purchases.
    This means we may receive a commission when you click our links and make a purchase.
    Thank you for supporting Impulse!</p>
</div>
""", unsafe_allow_html=True)

# --- User Inputs ---
st.subheader("🎯 Find the Perfect Gift in Seconds")

with st.container():
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        occasion = st.selectbox(
            "🎉 Select an Occasion", 
            ["Birthday", "Anniversary", "Holiday", "Wedding", "New Baby"]
        )
    
    with col2:
        budget = st.selectbox(
            "💰 Select Budget", 
            ["Low", "Medium", "Big Spender"]
        )
    
    with col3:
        recipient = st.text_input("👤 Describe the Recipient", 
            placeholder="e.g., 'My friend who is a passionate photographer'"
        )

# --- Generate Gift Ideas ---
if st.button("🔍 Find My Gift!"):
    if recipient.strip():
        with st.spinner("🎁 Finding the perfect gift..."):
            time.sleep(2)

            # 1) Amazon Gifts
            gift_ideas = get_gift_recommendations(occasion, budget, recipient)

            # 2) Experiences
            experiences = get_experiences(occasion, budget, recipient)

            st.subheader("✨ AI-Generated Gift Suggestions (Amazon):")
            if not gift_ideas:
                st.info("No items returned. Try adjusting your query.")
            else:
                for idea, link in gift_ideas:
                    st.markdown(f"""
                        <div class="result-card">
                            <strong>🎁 {idea}</strong><br>
                            <a href="{link}" target="_blank">🔗 Find on Amazon</a>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.subheader("🌟 Unique Experiences (Online or In-Person)")
            if not experiences:
                st.info("No experiences returned. Try adjusting your query.")
            else:
                for suggestion, site in experiences:
                    st.markdown(f"""
                        <div class="result-card">
                            <strong>{suggestion}</strong><br>
                            <a href="{site}" target="_blank">🔗 Visit Website</a>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a recipient description.")
