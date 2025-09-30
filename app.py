# app.py

import os
import streamlit as st
import google.generativeai as genai
from typing import List

# --- Core Gemini Function ---

def get_gemini_variations(api_key: str, keyword: str) -> List[str]:
    """
    Uses the Gemini API to generate 5 conversational variations of a keyword.

    Args:
        api_key (str): The Google AI Studio API key.
        keyword (str): The keyword to get variations for.

    Returns:
        A list of 5 string variations, or a list with a single error message.
    """
    if not keyword:
        return ["Error: Keyword cannot be empty."]
    
    try:
        # Configure the generative AI library with the provided key
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Generate exactly 5 possible variations of how the following keyword could be used
        in a conversational query by a user asking a question to an LLM.

        - The variations should be natural-sounding questions or phrases.
        - Do not add any introduction, conclusion, or extra formatting.
        - Return only a numbered list of the 5 variations.

        KEYWORD: "{keyword}"
        """
        
        response = model.generate_content(prompt)
        
        # Clean up the response to get a simple list of strings
        variations = response.text.strip().split('\n')
        # Remove the numbering (e.g., "1. ", "2. ") from the start of each line
        cleaned_variations = [line.split('. ', 1)[-1] for line in variations if line]
        
        return cleaned_variations

    except Exception as e:
        st.error(f"An error occurred while communicating with the Gemini API: {e}")
        return [f"API Error for keyword: '{keyword}'"]


# --- Streamlit Application UI ---

st.set_page_config(page_title="Keyword Variation Generator", layout="wide")

st.title("Conversational Keyword Variation Generator")
st.markdown("Enter a list of keywords, and this app will use the Gemini API to generate 5 conversational-style queries for each one.")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # It's better to get the key from the user in the UI for interactive apps
    gemini_api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Get your key from Google AI Studio. Your key is not stored."
    )
    
    st.header("✍️ Your Keywords")
    keywords_input = st.text_area(
        "Enter keywords, one per line:",
        height=250,
        placeholder="Content marketing for startups\nHealthy breakfast ideas\nBeginner's guide to Python"
    )
    
    submit_button = st.button("🚀 Generate Variations")


# --- Main Content Area for Results ---
if submit_button:
    if not gemini_api_key:
        st.warning("Please enter your Gemini API Key in the sidebar.")
    elif not keywords_input:
        st.warning("Please enter at least one keyword.")
    else:
        # Process keywords from the text area
        keywords = [k.strip() for k in keywords_input.split('\n') if k.strip()]
        
        st.subheader(f"Generated Variations for {len(keywords)} Keywords")
        
        # Process each keyword and display the results
        for keyword in keywords:
            with st.spinner(f"Generating variations for '{keyword}'..."):
                variations = get_gemini_variations(gemini_api_key, keyword)
                
                with st.expander(f"▶️ Queries for: '{keyword}'"):
                    if "API Error" in variations[0]:
                        st.error(variations[0])
                    else:
                        for i, variation in enumerate(variations, 1):
                            st.markdown(f"{i}. {variation}")
