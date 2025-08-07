from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Set Streamlit page config (must be at top)
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction by Gemini Pro")

# Load environment variables and Gemini API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Apply custom CSS styling
st.markdown("""
    <style>
    /* Push header & text up */
    .block-container {
        padding-top: 3rem;
    }

    h1, .stMarkdown {
        margin-bottom: 1rem;
    }

    /* Style file uploader text */
    .stFileUploader label {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
    }

    /* Style button */
    .stButton>button {
        color: white;
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        border: none;
        padding: 0.7rem 2rem;
        border-radius: 999px;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease-in-out;
        display: block;
        margin: 0.2rem auto auto 10rem;  /* Centered */
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #ff4b2b, #ff416c);
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Header and description
st.header("GeminiDecode: Multilanguage Document Extraction by Gemini Pro")
text = (
    "Utilizing Gemini Pro AI, this project effortlessly extracts vital information "
    "from diverse multilingual documents, transcending language barriers with "
    "precision and efficiency for enhanced productivity and decision-making."
)
styled_text = f"<span style='font-family:serif;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

# Gemini Vision function
def get_gimini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([input, image, prompt])
    return response.text

# Upload image
st.divider()

upload_files = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])
image = None

# Load image
def input_image_details(upload_files):
    if upload_files is not None:
        image = Image.open(upload_files)
        st.image(image, caption="Uploaded Document", use_container_width=True)
        return image
    return None

# Show image if uploaded
image = input_image_details(upload_files)

# User query
user_question = st.text_input("What do you want to know?'", placeholder='e.g., Explain the complete document in brief')

# Submit
submit = st.button("Submit")

if submit:
    if upload_files is None:
        st.warning("Please upload an image first.")
    elif not user_question.strip():
        st.warning("Please enter a question about the document.")
    else:
        response = get_gimini_response("Answer the user's question based on this document image:", image, user_question)
        st.subheader("The response is:")
        st.write(response)
