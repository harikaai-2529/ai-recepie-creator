import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("Gemini API key is not configured.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)


# -------------------------------
# Streamlit UI
# -------------------------------

st.set_page_config(
    page_title="AI Recipe Creator",
    page_icon="🍳"
)

st.title("🍳 AI Recipe Creator")

st.write(
    "Enter any ingredients you have at home, "
    "and AI will create a suitable recipe for you."
)


# Ingredient input
ingredients = st.text_input(
    "🥕 Available Ingredients",
    placeholder="Example: potato, onion, tomato"
)


# Generate button
if st.button("🍽️ Generate Recipe"):

    # Check whether user entered ingredients
    if not ingredients.strip():

        st.warning("Please enter at least one ingredient.")

    else:

        # Prompt for Gemini
        prompt = f"""
You are an expert AI recipe creator.

The user will provide ANY ingredients that they currently
have available at home.

User's available ingredients:
{ingredients}

Your job is to create ONE practical and realistic recipe
using the ingredients provided.

IMPORTANT RULES:

1. Analyze the actual ingredients provided by the user.
2. Do NOT assume that the user has egg, onion, tomato, rice,
   chicken, potato, or any other ingredient unless they
   explicitly provide it.
3. The example ingredients are only examples.
4. You may recommend a few common additional ingredients
   if they are necessary to make the recipe practical.
5. Clearly separate the ingredients the user already has
   from additional ingredients you recommend.
6. Keep the recipe simple and suitable for home cooking.
7. Do not create an unrealistic combination of ingredients.
8. Provide clear step-by-step cooking instructions.
9. Give a realistic estimated cooking time.
10. Mention servings and difficulty level.

Return the answer using exactly this structure:

RECIPE NAME:
<recipe name>

COOKING TIME:
<time in minutes>

SERVINGS:
<number>

DIFFICULTY:
<Easy / Medium / Hard>

AVAILABLE INGREDIENTS:
- <ingredient>
- <ingredient>

ADDITIONAL INGREDIENTS:
- <ingredient>
- <ingredient>

STEPS:
1. <step>
2. <step>
3. <step>
4. <step>

COOKING TIP:
<one useful cooking tip>
"""

        # Show loading message
        with st.spinner("🤖 Creating your recipe..."):

            try:

                # Send request to Gemini
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                # Display result
                st.subheader("🍽️ Your AI-Generated Recipe")

                st.write(response.text)

            except Exception as e:

                st.error(
                    "Something went wrong while generating "
                    "the recipe."
                )

                st.write(e)
