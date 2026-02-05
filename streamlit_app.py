import streamlit as st
import requests
import os
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Get backend URL from environment
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .chat-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'sessions' not in st.session_state:
    st.session_state.sessions = []

def load_sessions():
    """Load all chat sessions from backend"""
    try:
        response = requests.get(f"{API_BASE}/chat/sessions")
        if response.status_code == 200:
            st.session_state.sessions = response.json()
    except Exception as e:
        st.error(f"Error loading sessions: {str(e)}")

def load_messages(session_id):
    """Load messages for a specific session"""
    try:
        response = requests.get(f"{API_BASE}/chat/sessions/{session_id}/messages")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error loading messages: {str(e)}")
        return []

def create_new_session():
    """Create a new chat session"""
    try:
        response = requests.post(f"{API_BASE}/chat/sessions")
        if response.status_code == 200:
            session = response.json()
            st.session_state.current_session_id = session['session_id']
            st.session_state.messages = []
            load_sessions()
            return True
        return False
    except Exception as e:
        st.error(f"Error creating session: {str(e)}")
        return False

def send_message(message, session_id=None):
    """Send a message to the chatbot"""
    try:
        payload = {
            "message": message,
            "session_id": session_id
        }
        response = requests.post(f"{API_BASE}/chat", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")
        return None

def delete_session(session_id):
    """Delete a chat session"""
    try:
        response = requests.delete(f"{API_BASE}/chat/sessions/{session_id}")
        if response.status_code == 200:
            load_sessions()
            if st.session_state.current_session_id == session_id:
                st.session_state.current_session_id = None
                st.session_state.messages = []
            return True
        return False
    except Exception as e:
        st.error(f"Error deleting session: {str(e)}")
        return False

# Sidebar
with st.sidebar:
    st.markdown("### Chat Sessions")
    
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        if create_new_session():
            st.success("New chat created!")
            st.rerun()
    
    st.markdown("---")
    
    # Load sessions on first run
    if not st.session_state.sessions:
        load_sessions()
    
    # Display sessions
    for session in st.session_state.sessions:
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(
                f"💬 {session['title']}",
                key=f"session_{session['session_id']}",
                use_container_width=True
            ):
                st.session_state.current_session_id = session['session_id']
                st.session_state.messages = load_messages(session['session_id'])
                st.rerun()
        with col2:
            if st.button(
                "🗑️",
                key=f"delete_{session['session_id']}",
                help="Delete this chat"
            ):
                if delete_session(session['session_id']):
                    st.success("Deleted!")
                    st.rerun()

# Main content
st.markdown("""
<div class="chat-header">
    <h1>AI Chatbot</h1>
    <p>Powered by Claude Sonnet 4.5</p>
</div>
""", unsafe_allow_html=True)

# Check if session exists
if not st.session_state.current_session_id:
    st.info("👈 Click 'New Chat' in the sidebar to start a conversation!")
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])
            timestamp = datetime.fromisoformat(message['timestamp'].replace('Z', '+00:00'))
            st.caption(timestamp.strftime("%I:%M %p"))
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add to messages
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        # Get AI response
        with st.spinner("Thinking..."):
            response = send_message(prompt, st.session_state.current_session_id)
        
        if response:
            # Display assistant message
            with st.chat_message("assistant"):
                st.write(response['assistant_message'])
            
            # Add to messages
            st.session_state.messages.append({
                "role": "assistant",
                "content": response['assistant_message'],
                "timestamp": response['timestamp']
            })
            
            # Reload sessions to update timestamps
            load_sessions()
            
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Built with FastAPI, Streamlit, and Claude Sonnet 4.5</p>
</div>
""", unsafe_allow_html=True)