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
#   GPT-4 PROMPTS FOR GIFTS
# =========================
def get_gift_recommendations(occasion, budget, recipient):
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

    lines = response.choices[0].message.content.split("\n")
    gift_ideas = []
    for line in lines:
        if line.startswith("Gift Name:"):
            gift_name = line.replace("Gift Name:", "").strip()
            link = generate_amazon_search_link(gift_name)
            gift_ideas.append((gift_name, link))

    return gift_ideas[:3]

# =========================
#   GPT-4 PROMPTS FOR EXPERIENCES
# =========================
def get_experiences(occasion, budget, recipient):
    prompt = f"""
You are an expert experience curator. The user is advanced in their interests. 
Recipient: {recipient}
Occasion: {occasion}
Budget: {budget}
Return exactly 2 unique experiences, advanced-level or specialized. 
Use only domain-level homepage links. For instance, 'Website: https://www.stubhub.com' 
or 'Website: https://www.masterclass.com', no deeper paths.

Format exactly:
Experience Suggestion: [one line describing the idea]
Website: [domain homepage link only]

No disclaimers, exactly 2 experiences.
"""
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    lines = response.choices[0].message.content.split("\n")
    experiences = []
    suggestion, site = None, None

    for line in lines:
        if line.startswith("Experience Suggestion:"):
            suggestion = line.replace("Experience Suggestion:", "").strip()
        elif line.startswith("Website:"):
            candidate_link = line.replace("Website:", "").strip()
            pattern = r"(https?://[^/]+)"
            match = re.search(pattern, candidate_link)
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

/* Starry Background */
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

/* Input Fields */
.stTextInput, .stSelectbox {
    background: #000000;
    color: #000000;
    border-radius: 8px;
    padding: 12px;
    font-size: 1.1em;
    border: 1px solid #ffcc00;
}
.stTextInput::placeholder, .stSelectbox::placeholder {
    color: #777777;
}

/* Labels */
div[data-baseweb="select"] label, .stTextInput label {
    color: #ffffff !important;
}

/* Buttons */
.stButton>button {
    background-color: #ffcc00 !important;
    color: #000000 !important;
    font-weight: bold;
    border-radius: 12px;
    padding: 14px 30px;
    font-size: 1.2em;
    border: none;
}
.stButton>button:hover {
    background-color: #dddddd !important;
    transform: scale(1.05);
}

/* Result Cards */
.result-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(255, 255, 255, 0.2);
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
    <h1>Gift Finder AI</h1>
    <em>Thanks for testing this out </em>
    <p>Hint: Make sure to details for the gift recipient. For ex. My Dad < My Dad who loves golf </p>
</div>
""", unsafe_allow_html=True)

# User Inputs
st.subheader("")

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

            # Display Gifts
            st.subheader("✨ AI-Generated Gift Suggestions (Amazon):")
            for idea, link in gift_ideas:
                st.markdown(f"<div class='result-card'><strong>🎁 {idea}</strong><br><a href='{link}' target='_blank'>🔗 Find on Amazon</a></div>", unsafe_allow_html=True)

            # Display Experiences
            st.subheader("🌟 Unique Experiences (Online or In-Person)")
            for suggestion, site in experiences:
                st.markdown(f"<div class='result-card'><strong>{suggestion}</strong><br><a href='{site}' target='_blank'>🔗 Visit Website</a></div>", unsafe_allow_html=True)
# Affiliate Disclosure Section
st.markdown("""
<div class="affiliate-disclosure">
    <p><strong>Amazon Affiliate Disclosure:</strong> As an Amazon Associate, we earn from qualifying purchases. 
    This means we may receive a commission when you click our links and make a purchase. 
    Thank you for supporting Impulse!</p>
</div>
""", unsafe_allow_html=True)