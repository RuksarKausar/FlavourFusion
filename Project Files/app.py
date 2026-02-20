import streamlit as st
import google.generativeai as genai
import random
import os
from dotenv import load_dotenv

# -------------------------------
# LOAD ENVIRONMENT VARIABLES
# -------------------------------

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ API key not found. Please add GOOGLE_API_KEY in .env file")
    st.stop()

genai.configure(api_key=API_KEY)

# -------------------------------
# MODEL CONFIGURATION
# -------------------------------

generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash",
    generation_config=generation_config
)

# -------------------------------
# JOKE GENERATOR
# -------------------------------

def get_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why do Java developers wear glasses? Because they don't C#!",
        "Why did the programmer quit his job? Because he didn’t get arrays.",
        "Why do Python programmers wear glasses? Because they can't C.",
        "Why was the computer cold? Because it forgot to close Windows."
    ]
    return random.choice(jokes)

# -------------------------------
# RECIPE GENERATOR FUNCTION
# -------------------------------

def recipe_generation(user_input, word_count):

    st.info("⏳ Generating your recipe...")
    st.write("😂 **Joke while waiting:**", get_joke())

    try:
        chat = model.start_chat()

        prompt = f"""
        Generate a detailed and engaging recipe blog on the topic:
        "{user_input}"
        The blog should be around {word_count} words.
        Include:
        - Introduction
        - Ingredients list
        - Step-by-step cooking instructions
        - Cooking tips
        - Variations
        - Conclusion
        """

        response = chat.send_message(prompt)

        return response.text

    except Exception as e:
        return f"❌ Error: {e}"

# -------------------------------
# STREAMLIT UI (FRONTEND)
# -------------------------------

st.set_page_config(page_title="Flavour Fusion", page_icon="🍲", layout="centered")

st.title("🍽️ Flavour Fusion: AI-Driven Recipe Blogging")
st.subheader("Create amazing AI-powered recipe blogs instantly ✨")

topic = st.text_input("Enter Recipe Topic", placeholder="Example: Vegan Chocolate Cake")

word_count = st.number_input(
    "Number of Words",
    min_value=200,
    max_value=2000,
    value=600,
    step=100
)

if st.button("Generate Recipe"):
    if topic.strip() == "":
        st.warning("⚠️ Please enter a recipe topic")
    else:
        recipe = recipe_generation(topic, word_count)
        st.success("✅ Your recipe is ready!")
        st.write(recipe)