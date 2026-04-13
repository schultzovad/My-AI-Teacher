import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. PAGE SETUP
st.set_page_config(page_title="AI Tutor", layout="centered")

# 2. API KEY SETUP
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")

# Initialize the model
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 3. APP INTERFACE
st.title("📚 AI Tutor")
st.subheader("Turn your notes into clear explanations!")

# File uploader
uploaded_file = st.file_uploader("Upload a photo of your notes (JPG, PNG, PDF)", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Notes uploaded successfully!', use_column_width=True)
    
    if st.button('✨ Explain these notes'):
        
        # Instruction for the AI
        prompt = """
        You are a friendly and expert teacher. 
        Analyze the provided image/document and follow these steps:
        1. Give a brief summary of the topic.
        2. Explain the main concepts or formulas in a simple way.
        3. Provide a real-world example to help me understand better.
        4. End with 3 quick review questions.
        
        IMPORTANT: Your response MUST be in the same language as the notes in the image.
        Use clean Markdown formatting, bullet points, and bold text for readability.
        """
        
        with st.spinner('Analyzing your notes... please wait.'):
            try:
                # Generate content
                response = model.generate_content([prompt, image])
                
                st.success("Analysis complete!")
                st.markdown("---")
                # Output the result
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.caption("Powered by Gemini AI | Designed for your success 🎓")
