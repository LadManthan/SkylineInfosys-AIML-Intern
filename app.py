import streamlit as st
from chatbot_core import RAGChatbot
from supabase_db import ChatDatabase
import uuid
from datetime import datetime

# Page config
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = RAGChatbot()

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("💬 Chat Sessions")
    
    # New Chat button
    if st.button("➕ New Chat", use_container_width=True):
        session = ChatDatabase.create_chat_session(
            user_id=st.session_state.user_id,
            title=f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        if session:
            st.session_state.current_session_id = session['id']
            st.session_state.messages = []
            st.rerun()
    
    st.divider()
    
    # Load previous sessions
    sessions = ChatDatabase.get_user_sessions(st.session_state.user_id)
    
    if sessions:
        st.subheader("Previous Chats")
        for session in sessions:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if st.button(
                    session['title'],
                    key=f"session_{session['id']}",
                    use_container_width=True
                ):
                    st.session_state.current_session_id = session['id']
                    # Load messages
                    messages = ChatDatabase.get_session_messages(session['id'])
                    st.session_state.messages = [
                        {"role": "user", "content": msg['user_message'], "timestamp": msg['created_at']}
                        for msg in messages
                    ] + [
                        {"role": "assistant", "content": msg['bot_response'], "timestamp": msg['created_at']}
                        for msg in messages
                    ]
                    st.session_state.messages.sort(key=lambda x: x['timestamp'])
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{session['id']}"):
                    ChatDatabase.delete_session(session['id'])
                    if st.session_state.current_session_id == session['id']:
                        st.session_state.current_session_id = None
                        st.session_state.messages = []
                    st.rerun()
    else:
        st.info("No previous chats")

# Main chat interface
st.title("🤖 RAG Chatbot")
st.caption("Ask questions about your document")

# Create session if none exists
if st.session_state.current_session_id is None:
    session = ChatDatabase.create_chat_session(
        user_id=st.session_state.user_id,
        title=f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    if session:
        st.session_state.current_session_id = session['id']

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chatbot.chat(prompt)
            st.write(response)
    
    # Add assistant message to chat
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Store in database
    if st.session_state.current_session_id:
        ChatDatabase.store_message(
            session_id=st.session_state.current_session_id,
            user_message=prompt,
            bot_response=response
        )
        
        # Update title with first message
        if len(st.session_state.messages) == 2:
            title = prompt[:50] + "..." if len(prompt) > 50 else prompt
            ChatDatabase.update_session_title(
                st.session_state.current_session_id,
                title
            )

# Footer
st.divider()
st.caption("Powered by LangGraph, Groq, and Supabase")