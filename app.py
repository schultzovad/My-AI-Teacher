import streamlit as st
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="AI Tutor", layout="centered", page_icon="🎓")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key in Secrets!")

# Stable model names
AVAILABLE_MODELS = ['gemini-flash-latest', 'gemini-2.0-flash', 'gemini-pro-latest']

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. HEADER AND CHAT HISTORY
st.title("🎓 Your Personal AI Tutor")
st.caption("Upload your notes and ask anything. I'm here to help you understand! 😊")

# Displaying chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.write("---")

# 3. FILE UPLOADER (Positioned at the bottom, above chat input)
with st.container():
    uploaded_files = st.file_uploader(
        "Attach notes or photos", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="file_uploader_fixed"
    )
    
    # "Explain" button - only appears if files are uploaded
    analyze_clicked = False
    if uploaded_files:
        if st.button("✨ Explain my uploaded files"):
            analyze_clicked = True

# 4. CHAT INPUT (At the very bottom)
input_text = st.chat_input("Ask a question...")

# 5. PROCESSING LOGIC
if input_text or analyze_clicked:
    # Set the prompt text
    prompt = input_text if input_text else "Please explain these files like a teacher and solve any problems you see."
    
    # Add to history and rerun to move the UI elements
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# This part runs after rerun if the last message is from the user
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        container = st.empty()
        payload = []
        
        # SYSTEM INSTRUCTION (The "Personality")
        teacher_prompt = """
        You are an experienced, kind, and patient teacher. 
        Your task is to explain study materials clearly and humanly.
        
        CRITICAL RULES:
        1. If there are math problems or exercises in the images, solve them step-by-step first.
        2. Be encouraging and helpful.
        3. 100% factual accuracy is required.
        4. IMPORTANT: Always respond in the SAME LANGUAGE as the user's question or the language of the uploaded notes. 
           If the notes are in Slovak, explain them in Slovak. If the notes are in English, explain in English.
        """
        payload.append(teacher_prompt)
        
        # Add context (last 6 messages)
        for m in st.session_state.messages[-6:]:
            payload.append(f"{m['role']}: {m['content']}")

        # Add files from the uploader
        if uploaded_files:
            for f in uploaded_files:
                payload.append({'mime_type': f.type, 'data': f.getvalue()})

        success = False
        full_response = ""
        for model_name in AVAILABLE_MODELS:
            if success: break
            try:
                with st.spinner('Teacher is thinking...'):
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(payload)
                    full_response = response.text
                    success = True
            except Exception as e:
                if "429" in str(e): continue
                else: break
        
        if not success:
            full_response = "I'm sorry, I need a 30-second coffee break. Please try again in a moment! ☕😊"

        container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        # Rerun again to place the uploader and input field below the new response
        st.rerun()

# Sidebar for settings
with st.sidebar:
    st.title("Settings")
    if st.button("🗑️ Clear Chat / New Topic"):
        st.session_state.messages = []
        st.rerun()
