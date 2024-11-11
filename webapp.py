import streamlit as st
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv
from main import relevant_documents

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Design Bot",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.8);
    }
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.8);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: rgba(255, 255, 255, 0.9);
    }
    .bot-message {
        background-color: rgba(144, 238, 144, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

def initialize_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OPENAI_API_KEY not found in .env file. Please check your .env file configuration.")
        st.stop()
    return OpenAI(api_key=api_key)

def get_assistant_response(client, prompt, conversation_history):
    try:
        messages = [
            {"role": "system", "content": "You are a creative and knowledgeable design assistant, skilled in providing design advice, suggestions, and creative solutions. You communicate in a friendly, professional manner and provide detailed, actionable feedback."}
        ]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": "user" if msg["is_user"] else "assistant",
                "content": relevant_documents(msg["content"])
            })
            
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.3,
            max_tokens=2024
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Main app title
st.title("🎨 Design Assistant")
st.markdown("---")

# Initialize OpenAI client
client = initialize_openai_client()

# Sidebar with additional options
with st.sidebar:
    st.header("Settings")
    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.markdown("### Chat with your Design Assistant")
st.markdown("Ask me anything about design, and I'll help you create something amazing!")

# Display chat history
for message in st.session_state.messages:
    with st.container():
        st.markdown(f"""
            <div class="chat-message {'user-message' if message['is_user'] else 'bot-message'}">
                <b>{'You' if message['is_user'] else '🎨 Design Bot'}:</b><br>{message['content']}
            </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.text_area("Your message:", height=100)
if st.button("Send", key="send"):
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"content": user_input, "is_user": True})
        
        # Get bot response
        response = get_assistant_response(client, user_input, st.session_state.messages)
        
        # Add bot response to history
        st.session_state.messages.append({"content": response, "is_user": False})
        
        # Clear input
        st.rerun()
