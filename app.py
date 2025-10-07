import streamlit as st
from transformers import pipeline
import time # To simulate a progress bar for better UX

# --- Page Configuration ---
# Sets the title of the browser tab and a fitting icon.
st.set_page_config(
    page_title="AI Sentiment Text Generator",
    page_icon="🤖",
    layout="centered" 
)

# --- Model Loading ---
# We keep the caching decorator to ensure models are loaded only once.
@st.cache_resource
def load_models():
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    text_generator = pipeline("text-generation", model="gpt2")
    return sentiment_analyzer, text_generator

# Load models and display a friendly message.
with st.spinner('Warming up the AI engines... Please wait.'):
    sentiment_analyzer, text_generator = load_models()

# --- Sidebar Content ---
# Adds a sidebar for extra information, keeping the main interface clean.
with st.sidebar:
    st.header("About This App")
    st.write("""
        This application is an AI-powered text generator. 
        It analyzes the sentiment of your input prompt and then 
        generates a new paragraph with a matching emotional tone.
    """)
    st.subheader("Technologies Used 🛠️:")
    st.write("- Streamlit for the User Interface")
    st.write("- Hugging Face Transformers for AI Models")
    st.divider() # Adds a visual separator

    st.header("Cantact Me")
    st.markdown("""
    **Komal Sharma**
    
    ---
    
    **Professional Profiles:**
    - **LinkedIn:** [k-sharma19](https://www.linkedin.com/in/k-sharma19/)
    - **GitHub:** [komal-sharma19](https://github.com/komal-sharma19)
    - **LeetCode:** [Komal Sharma](https://leetcode.com/u/KomalSharma19/)
    - **GeeksforGeeks:** [Komal Sharma](https://www.geeksforgeeks.org/user/2023asppwkz/)
    - **HackerRank:** [Komal Sharma](https://www.hackerrank.com/profile/2023aspire96)
    
    ---

    **Contact:**
    - ✉️ [1908.komalsharma@gmail.com](mailto:1908.komalsharma@gmail.com)
    - 📍 Kanpur,Uttar Pradesh
    """)


# --- Main Application UI ---
st.title("🤖 AI Text Generator with Sentiment")
st.markdown("Enter a prompt, and the AI will detect its sentiment and generate a new paragraph with the same feeling.")

# --- Example Prompts ---
# Use columns to lay out example buttons horizontally.
st.subheader("Try an Example")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("😊Positive Example"):
        st.session_state.prompt = "The sunny weather today makes me feel incredibly happy and optimistic."

with col2:
    if st.button("🌧️ Negative Example"):
        st.session_state.prompt = "The constant rain and canceled plans have left me feeling gloomy and disappointed."

with col3:
    if st.button("⚖️ Neutral Example"):
        st.session_state.prompt = "The new library downtown is scheduled to open next Tuesday."

# Initialize session_state for the text area if it doesn't exist.
if 'prompt' not in st.session_state:
    st.session_state.prompt = "I had an amazing vacation in the mountains!"

user_prompt = st.text_area("Enter your prompt here:", key="prompt", height=150)

# --- Generation Logic ---
if st.button("✨ Generate Text", type="primary"):
    if user_prompt:
        # Progress bar for a better visual cue during processing.
        progress_bar = st.progress(0, text="Thinking...")
        
        # 1. ANALYZE SENTIMENT
        sentiment_result = sentiment_analyzer(user_prompt)
        detected_sentiment = sentiment_result[0]['label']
        sentiment_for_prompt = detected_sentiment.lower()
        
        # Update progress bar
        for percent_complete in range(100):
            time.sleep(0.01) # Small delay to make the bar visible
            progress_bar.progress(percent_complete + 1, text=f"Sentiment Detected: {detected_sentiment}")

        # 2. GENERATE TEXT
        generation_prompt = f"Write a {sentiment_for_prompt} paragraph about the following topic: {user_prompt}"
        generated_text_result = text_generator(generation_prompt, max_length=150, num_return_sequences=1)
        full_text = generated_text_result[0]['generated_text']
        cleaned_text = full_text.replace(generation_prompt, "").strip()
        
        # Finish progress bar
        progress_bar.progress(100, text="Generation Complete!")
        time.sleep(1) # Pause briefly before hiding the bar
        progress_bar.empty()

        # 3. DISPLAY THE RESULTS
        st.divider()
        st.subheader("📜 Generated Result")

        # Use colored boxes (success, error, info) for sentiment for better UI.
        if detected_sentiment == 'POSITIVE':
            st.success(f"**Detected Sentiment: POSITIVE** 😊")
        elif detected_sentiment == 'NEGATIVE':
            st.error(f"**Detected Sentiment: NEGATIVE** 😠")
        else:
            st.info(f"**Detected Sentiment: NEUTRAL** 😐")

        # Display the generated text in a styled container.
        with st.container(border=True):
            st.write(cleaned_text)
            
    else:
        st.warning("Please enter a prompt first!")