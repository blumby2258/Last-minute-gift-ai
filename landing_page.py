import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Impulse: AI Gift Finder", page_icon="🎁", layout="centered")

# --- Custom CSS ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    background-color: #f8f9fa;
}

/* Hero Section */
.hero {
    text-align: center;
    padding: 60px 20px;
    background: linear-gradient(135deg, #e74c3c, #f39c12);
    border-radius: 12px;
    color: white;
}
.hero h1 {
    font-size: 3em;
    font-weight: 600;
}
.hero p {
    font-size: 1.2em;
    opacity: 0.9;
}
.hero button {
    margin-top: 15px;
}

/* Section Styling */
.section {
    text-align: center;
    margin: 50px 0;
}
.section h2 {
    color: #2c3e50;
    font-size: 2.2em;
}
.section p {
    font-size: 1.1em;
    color: #7f8c8d;
}

/* Steps */
.steps {
    display: flex;
    justify-content: center;
    gap: 30px;
}
.step-box {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    width: 250px;
    text-align: center;
}
.step-box h3 {
    font-size: 1.4em;
    color: #e74c3c;
}
.step-box p {
    font-size: 1em;
    color: #2c3e50;
}

/* Call to Action */
.cta {
    text-align: center;
    padding: 40px 0;
}
.cta button {
    background-color: #e74c3c;
    color: white;
    font-size: 1.3em;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: bold;
    transition: all 0.3s ease-in-out;
}
.cta button:hover {
    background-color: #c0392b;
    transform: scale(1.05);
}

/* Affiliate Disclosure */
.disclaimer {
    font-size: 0.9em;
    color: #7f8c8d;
    text-align: center;
    margin-top: 20px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero">
    <h1>🎁 Impulse: Find the Perfect Gift in Seconds</h1>
    <p>Let AI find the perfect last-minute gift – instantly!</p>
    <a href="/app">
        <button>🔍 Try It Now</button>
    </a>
</div>
""", unsafe_allow_html=True)

# --- How It Works Section ---
st.markdown("""
<div class="section">
    <h2>🎯 How It Works</h2>
    <div class="steps">
        <div class="step-box">
            <h3>1️⃣ Enter Details</h3>
            <p>Select an occasion, budget, and describe the recipient.</p>
        </div>
        <div class="step-box">
            <h3>2️⃣ Get AI Suggestions</h3>
            <p>Our AI finds the best last-minute gifts for you.</p>
        </div>
        <div class="step-box">
            <h3>3️⃣ Buy Instantly</h3>
            <p>Click & buy your gift directly on Amazon.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Benefits Section ---
st.markdown("""
<div class="section">
    <h2>🔥 Why Use Impulse?</h2>
    <p>✅ AI-powered, fast, and easy</p>
    <p>✅ Avoid last-minute stress</p>
    <p>✅ Personalized, high-quality gifts</p>
</div>
""", unsafe_allow_html=True)

# --- CTA Button ---
st.markdown("""
<div class="cta">
    <a href="/app">
        <button>🚀 Find Your Perfect Gift Now</button>
    </a>
</div>
""", unsafe_allow_html=True)

# --- Amazon Affiliate Disclosure ---
st.markdown("""
<div class="disclaimer">
    <p><strong>Disclaimer:</strong> As an Amazon Associate, we earn from qualifying purchases. Clicking on links may generate a commission for us at no extra cost to you.</p>
</div>
""", unsafe_allow_html=True)
