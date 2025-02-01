import streamlit as st
import openai
import os
import re
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Your Amazon Affiliate Store ID (Replace with yours)
AMAZON_AFFILIATE_TAG = "yourstoreid-20"  # Change this to your actual Store ID

# Function to format search queries & fetch Amazon links
def generate_amazon_search_link(product_name):
    query = product_name.replace(" ", "+")  # Format search query
    return f"https://www.amazon.com/s?k={query}&tag={AMAZON_AFFILIATE_TAG}"  # Amazon affiliate link

# Function to clean AI output and extract only gift names
def clean_gift_idea(raw_text):
    """
    Cleans the AI-generated text to extract only the product name,
    removing descriptions and extra words.
    """
    # Remove budget-related text (e.g., "all under $50 and easily orderable online")
    raw_text = re.sub(r'all under\s?\$?\d+\s?(and easily orderable online)?', '', raw_text, flags=re.IGNORECASE)
    
    # Extract just the product name by removing everything after ":" or "-"
    cleaned_text = re.split(r":|-", raw_text)[0].strip()

    return cleaned_text

# Function to generate gift ideas with clean Amazon affiliate links
def get_gift_ideas(occasion, budget, recipient):
    if not openai.api_key:
        return "❌ OpenAI API key is missing. Please check your .env file."

    prompt = f"Suggest three last-minute gift ideas for a {occasion} within a {budget} budget. The recipient is {recipient}. Keep them practical and easy to order online. Only provide the product names, no descriptions."

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI that suggests creative last-minute gifts."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Convert AI response into a clean list
        gift_ideas = response.choices[0].message.content.split("\n")  
        formatted_suggestions = []

        for idea in gift_ideas:
            if idea.strip():  # Ignore empty lines
                product_name = clean_gift_idea(idea.strip("🎁-"))  # Clean up AI response
                amazon_url = generate_amazon_search_link(product_name)
                formatted_suggestions.append(f"🎁 **{product_name}**\n🔗 [Find on Amazon]({amazon_url})\n")

        return "\n".join(formatted_suggestions)  # Return formatted gift list
    
    except Exception as e:
        return f"❌ Error: {e}"

# Streamlit UI
st.title("🎁 Last-Minute Gift AI")
st.write("Enter details below and get instant gift ideas with Amazon affiliate links!")

# User inputs
occasion = st.selectbox("Select an Occasion", ["Birthday", "Anniversary", "Christmas", "Graduation", "Valentine's Day"])
budget = st.selectbox("Select Budget", ["Under $50", "$50-$100", "$100-$200", "$200+"])
recipient = st.text_input("Describe the recipient (e.g., 'Dad who loves golf')")

# Generate gift ideas on button click
if st.button("Get Gift Ideas"):
    if recipient:
        gift_ideas = get_gift_ideas(occasion, budget, recipient)
        st.subheader("🎁 Gift Suggestions:")
        st.markdown(gift_ideas, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a recipient description.")
