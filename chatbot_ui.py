"""
Multi-Agent Coding Assistant - Streamlit Chatbot Interface
A web-based chat interface for the multi-agent coding system using Google Gemini
"""

import asyncio
import os
import streamlit as st
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="AI Coding Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 25px;
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.4);
        margin: 1.5rem;
        border: 3px solid rgba(30, 60, 114, 0.3);
    }
    
    /* Title styling - BOLD AND VISIBLE WITH WHITE COLOR */
    h1 {
        color: white !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease-out;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    /* Subtitle/Caption - VISIBLE WITH WHITE COLOR */
    .stCaption {
        text-align: center;
        font-size: 1.2rem !important;
        color: white !important;
        font-weight: 600 !important;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling - THICK BLUE GRADIENT */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
        padding: 2rem 1rem;
        border-right: 5px solid #7e22ce;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 500 !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        animation: slideInUp 0.4s ease-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* User message */
    [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* HIDE CODE BLOCKS - Make them invisible */
    code {
        display: none !important;
    }
    
    pre {
        display: none !important;
    }
    
    /* Hide code blocks in markdown */
    .stMarkdown pre {
        display: none !important;
    }
    
    .stMarkdown code {
        display: none !important;
    }
    
    /* Chat input */
    .stChatInputContainer {
        border-top: 2px solid #e0e0e0;
        padding-top: 1rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 -4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.8rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(30, 60, 114, 0.5);
        font-size: 1rem;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(30, 60, 114, 0.7);
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
    }
    
    /* Text input - HIDE PASSWORD */
    .stTextInput input[type="password"] {
        border-radius: 10px;
        border: 2px solid #2a5298;
        padding: 0.7rem;
        transition: border-color 0.3s ease;
        font-weight: 600;
    }
    
    .stTextInput input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.7rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: #1e3c72;
        box-shadow: 0 0 0 3px rgba(30, 60, 114, 0.2);
    }
    
    /* Info box */
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #dbeafe 100%);
        border-left: 5px solid #1e3c72;
        border-radius: 10px;
        padding: 1rem;
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 5px solid #4caf50;
        border-radius: 10px;
        animation: fadeIn 0.6s ease-out;
        font-weight: 600;
    }
    
    /* Error message */
    .stError {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 5px solid #f44336;
        border-radius: 10px;
        animation: shake 0.5s ease-out;
        font-weight: 600;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #1e3c72 !important;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #1e3c72, #2a5298, #1e3c72, transparent);
    }
    
    /* Agent badges - PROFESSIONAL BLUE THEME */
    .agent-badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.8rem;
        letter-spacing: 0.5px;
    }
    
    .researcher-badge {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        box-shadow: 0 3px 15px rgba(30, 60, 114, 0.4);
    }
    
    .coder-badge {
        background: linear-gradient(135deg, #2a5298 0%, #7e22ce 100%);
        color: white;
        box-shadow: 0 3px 15px rgba(42, 82, 152, 0.4);
    }
    
    .tester-badge {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        box-shadow: 0 3px 15px rgba(5, 150, 105, 0.4);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    /* Pulse animation for loading */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Scrollbar styling - THICK BLUE */
    ::-webkit-scrollbar {
        width: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: #e5e7eb;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 10px;
        border: 2px solid #e5e7eb;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2a5298 0%, #7e22ce 100%);
    }
    
    /* Make all headings BOLD and VISIBLE WITH WHITE COLOR */
    h2, h3, h4, h5, h6 {
        color: white !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.3);
    }
    
    /* Example prompts heading */
    .main h3 {
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    }
    
    /* Make sure icons in titles are visible */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Load environment variables
def load_api_key():
    """Load API key from .env file"""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Fallback: read .env file directly if load_dotenv() didn't work
    if not api_key:
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("GOOGLE_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        break
        except FileNotFoundError:
            pass
    
    return api_key

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = load_api_key()

# Sidebar
with st.sidebar:
    # Header with icon
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='font-size: 3rem; margin: 0;'>🤖</h1>
            <h2 style='color: white; margin: 0.5rem 0;'>AI Assistant</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # API Key input - HIDDEN AND SECURE
    st.markdown("### 🔑 API Configuration")
    
    # Check if API key exists
    if st.session_state.api_key:
        st.success("✅ API Key Configured")
        st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 0.8rem; border-radius: 10px; text-align: center;'>
                <div style='color: white; font-size: 0.9rem;'>🔒 Secure Connection Active</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Option to change API key
        if st.button("🔄 Change API Key", use_container_width=True):
            st.session_state.show_api_input = True
    else:
        st.session_state.show_api_input = True
    
    # Show API key input only when needed
    if st.session_state.get('show_api_input', False) or not st.session_state.api_key:
        api_key_input = st.text_input(
            "Enter API Key",
            value="",
            type="password",
            help="Your Google Gemini API key (hidden for security)",
            placeholder="Paste your API key here...",
            label_visibility="collapsed"
        )
        
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.session_state.show_api_input = False
            st.rerun()
    
    st.divider()
    
    # Agent information with badges
    st.markdown("### 🤖 Active Agents")
    
    st.markdown("""
        <div style='margin: 1rem 0;'>
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem;'>
                <div style='font-size: 1.5rem;'>🔍</div>
                <div style='font-weight: 600; color: white;'>Researcher</div>
                <div style='font-size: 0.85rem; color: rgba(255,255,255,0.8);'>Analyzes & plans</div>
            </div>
            
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem;'>
                <div style='font-size: 1.5rem;'>💻</div>
                <div style='font-weight: 600; color: white;'>Coder</div>
                <div style='font-size: 0.85rem; color: rgba(255,255,255,0.8);'>Writes the code</div>
            </div>
            
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;'>
                <div style='font-size: 1.5rem;'>✅</div>
                <div style='font-weight: 600; color: white;'>Tester</div>
                <div style='font-size: 0.85rem; color: rgba(255,255,255,0.8);'>Reviews & validates</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Statistics
    if len(st.session_state.messages) > 0:
        st.markdown("### 📊 Session Stats")
        user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
        agent_msgs = len([m for m in st.session_state.messages if m["role"] != "user"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Messages", user_msgs)
        with col2:
            st.metric("Agent Replies", agent_msgs)
        
        st.divider()
    
    # Clear chat button with better styling
    if st.button("🗑️ Clear Chat History", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Footer
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0; color: rgba(255,255,255,0.7);'>
            <div style='font-size: 0.9rem; margin-bottom: 0.5rem;'>⚡ Powered by</div>
            <div style='font-weight: 600; color: white;'>Google Gemini 2.5 Flash</div>
            <div style='font-size: 0.8rem; margin-top: 1rem;'>Made with ❤️ using AutoGen</div>
        </div>
    """, unsafe_allow_html=True)

# Main chat interface
st.title("🤖 AI Multi-Agent Coding Assistant")
st.caption("Ask me to create any code, and watch my team of AI agents collaborate!")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        # Determine avatar and styling based on role
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)
        elif role == "Researcher":
            with st.chat_message("assistant", avatar="🔍"):
                st.markdown("""
                    <div class='agent-badge researcher-badge'>🔍 RESEARCHER</div>
                """, unsafe_allow_html=True)
                st.markdown(content)
        elif role == "Coder":
            with st.chat_message("assistant", avatar="💻"):
                st.markdown("""
                    <div class='agent-badge coder-badge'>💻 CODER</div>
                """, unsafe_allow_html=True)
                st.markdown(content)
        elif role == "Tester":
            with st.chat_message("assistant", avatar="✅"):
                st.markdown("""
                    <div class='agent-badge tester-badge'>✅ TESTER</div>
                """, unsafe_allow_html=True)
                st.markdown(content)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(content)

# Chat input
user_input = st.chat_input("Describe the code you want to create...")

async def run_multi_agent_system(task: str, api_key: str):
    """Run the multi-agent system and yield messages"""
    
    # Create custom ModelInfo to bypass OpenAI model validation
    gemini_model_info = ModelInfo(
        family="gemini-2.0-flash-exp",
        vision=True,
        function_calling=True,
        json_output=True,
        structured_output=True
    )
    
    # Configure Gemini through OpenAI-compatible API
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.0-flash-exp",
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        model_info=gemini_model_info
    )
    
    # Define agents
    researcher = AssistantAgent(
        name="Researcher",
        model_client=model_client,
        system_message="""You are a Researcher agent. Your role is to:
1. Analyze the coding task thoroughly
2. Break it down into clear, actionable steps
3. Identify key requirements and potential challenges
4. Create a detailed plan for the Coder to follow

Be concise but thorough. Focus on the technical approach."""
    )
    
    coder = AssistantAgent(
        name="Coder",
        model_client=model_client,
        system_message="""You are a Coder agent. Your role is to:
1. Review the Researcher's plan
2. Write clean, efficient, and well-documented code
3. Follow best practices and coding standards
4. Include comments explaining key parts of the code

Provide complete, working code that can be run immediately."""
    )
    
    tester = AssistantAgent(
        name="Tester",
        model_client=model_client,
        system_message="""You are a Tester agent. Your role is to:
1. Review the code written by the Coder
2. Check for bugs, errors, and potential issues
3. Verify that it meets the original requirements
4. Suggest improvements if needed

If the code is good, respond with "TERMINATE" to end the conversation.
If there are issues, provide specific feedback."""
    )
    
    # Create termination condition
    termination = TextMentionTermination("TERMINATE")
    
    # Create team
    team = RoundRobinGroupChat(
        participants=[researcher, coder, tester],
        termination_condition=termination,
        max_turns=15
    )
    
    # Run the team and stream results
    stream = team.run_stream(task=task)
    
    async for message in stream:
        yield message

def sync_run_agents(task: str, api_key: str):
    """Synchronous wrapper for running agents"""
    try:
        # Create new event loop for this run
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def collect_messages():
            messages = []
            async for message in run_multi_agent_system(task, api_key):
                messages.append(message)
            return messages
        
        messages = loop.run_until_complete(collect_messages())
        loop.close()
        
        return messages
    except Exception as e:
        return [{"error": str(e)}]

# Handle user input
if user_input:
    # Check if API key is available
    if not st.session_state.api_key:
        st.error("⚠️ Please enter your Google API Key in the sidebar!")
        st.stop()
    
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Show loading spinner with animated message
    loading_messages = [
        "🔍 Researcher is analyzing your request...",
        "💻 Coder is writing the solution...",
        "✅ Tester is reviewing the code...",
        "🤖 AI agents are collaborating..."
    ]
    
    with st.spinner(loading_messages[len(st.session_state.messages) % len(loading_messages)]):
        # Show a nice loading animation - BLUE THEME
        st.markdown("""
            <div style='text-align: center; padding: 2.5rem; background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%); 
                        border-radius: 18px; margin: 1rem 0; animation: pulse 1.5s ease-in-out infinite; border: 3px solid #1e3c72; box-shadow: 0 8px 25px rgba(30, 60, 114, 0.3);'>
                <div style='font-size: 2.5rem; margin-bottom: 1rem;'>⚡</div>
                <div style='font-weight: 700; color: #1e3c72; font-size: 1.3rem;'>
                    Your AI Team is Working on It...
                </div>
                <div style='color: #374151; margin-top: 0.8rem; font-size: 1rem; font-weight: 600;'>
                    This may take a few moments
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            # Run the multi-agent system
            messages = sync_run_agents(user_input, st.session_state.api_key)
            
            # Process and display messages
            for msg in messages:
                if hasattr(msg, 'source') and hasattr(msg, 'content'):
                    agent_name = msg.source
                    content = msg.content
                    
                    # Skip if content is empty or just whitespace
                    if not content or not content.strip():
                        continue
                    
                    # Add to session state
                    st.session_state.messages.append({
                        "role": agent_name,
                        "content": content
                    })
                    
                    # Display message with badges
                    if agent_name == "Researcher":
                        with st.chat_message("assistant", avatar="🔍"):
                            st.markdown("""
                                <div class='agent-badge researcher-badge'>🔍 RESEARCHER</div>
                            """, unsafe_allow_html=True)
                            st.markdown(content)
                    elif agent_name == "Coder":
                        with st.chat_message("assistant", avatar="💻"):
                            st.markdown("""
                                <div class='agent-badge coder-badge'>💻 CODER</div>
                            """, unsafe_allow_html=True)
                            st.markdown(content)
                    elif agent_name == "Tester":
                        with st.chat_message("assistant", avatar="✅"):
                            st.markdown("""
                                <div class='agent-badge tester-badge'>✅ TESTER</div>
                            """, unsafe_allow_html=True)
                            st.markdown(content)
                elif "error" in msg:
                    st.error(f"❌ Error: {msg['error']}")
            
            # Success message with celebration - BLUE/GREEN THEME
            st.balloons()
            st.markdown("""
                <div style='background: linear-gradient(135deg, #059669 0%, #10b981 100%); 
                            padding: 2rem; 
                            border-radius: 18px; 
                            color: white; 
                            text-align: center;
                            box-shadow: 0 12px 35px rgba(5, 150, 105, 0.4);
                            animation: fadeIn 0.6s ease-out;
                            border: 3px solid rgba(255,255,255,0.3);'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.8rem;'>🎉</div>
                    <div style='font-weight: 800; font-size: 1.4rem;'>Task Completed Successfully!</div>
                    <div style='font-size: 1rem; margin-top: 0.8rem; opacity: 0.95; font-weight: 600;'>
                        Your AI team has finished collaborating
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)

# Welcome message - PROFESSIONAL BLUE THEME
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%); 
                    padding: 3rem; 
                    border-radius: 20px; 
                    color: white; 
                    text-align: center;
                    box-shadow: 0 15px 40px rgba(30, 60, 114, 0.5);
                    animation: fadeIn 0.8s ease-out;
                    border: 3px solid rgba(255,255,255,0.2);'>
            <h2 style='color: white !important; margin-bottom: 1rem; font-weight: 800; font-size: 2.2rem;'>👋 Welcome to Your AI Coding Team!</h2>
            <p style='font-size: 1.2rem; margin-bottom: 2rem; font-weight: 500;'>
                Three specialized AI agents are ready to collaborate and build code for you
            </p>
            
            <div style='display: flex; justify-content: space-around; margin: 2rem 0; flex-wrap: wrap;'>
                <div style='background: rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 15px; margin: 0.5rem; min-width: 160px; border: 2px solid rgba(255,255,255,0.2);'>
                    <div style='font-size: 2.5rem;'>🔍</div>
                    <div style='font-weight: 700; margin-top: 0.8rem; font-size: 1.1rem;'>Researcher</div>
                    <div style='font-size: 0.95rem; opacity: 0.95; margin-top: 0.3rem;'>Plans the solution</div>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 15px; margin: 0.5rem; min-width: 160px; border: 2px solid rgba(255,255,255,0.2);'>
                    <div style='font-size: 2.5rem;'>💻</div>
                    <div style='font-weight: 700; margin-top: 0.8rem; font-size: 1.1rem;'>Coder</div>
                    <div style='font-size: 0.95rem; opacity: 0.95; margin-top: 0.3rem;'>Writes the code</div>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 15px; margin: 0.5rem; min-width: 160px; border: 2px solid rgba(255,255,255,0.2);'>
                    <div style='font-size: 2.5rem;'>✅</div>
                    <div style='font-weight: 700; margin-top: 0.8rem; font-size: 1.1rem;'>Tester</div>
                    <div style='font-size: 0.95rem; opacity: 0.95; margin-top: 0.3rem;'>Validates quality</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Example prompts in a nice grid - BLUE THEME
    st.markdown("### 💡 Try These Examples:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #e3f2fd 0%, #dbeafe 100%); padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; border-left: 5px solid #1e3c72; box-shadow: 0 3px 10px rgba(0,0,0,0.1);'>
                <div style='font-weight: 700; color: #1e3c72; margin-bottom: 0.5rem; font-size: 1.05rem;'>🧮 Calculator App</div>
                <div style='font-size: 0.95rem; color: #374151; font-weight: 500;'>"Create a calculator app in Python"</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; border-left: 5px solid #7e22ce; box-shadow: 0 3px 10px rgba(0,0,0,0.1);'>
                <div style='font-weight: 700; color: #7e22ce; margin-bottom: 0.5rem; font-size: 1.05rem;'>📝 Todo List</div>
                <div style='font-size: 0.95rem; color: #374151; font-weight: 500;'>"Build a todo list with Flask"</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; border-left: 5px solid #059669; box-shadow: 0 3px 10px rgba(0,0,0,0.1);'>
                <div style='font-weight: 700; color: #059669; margin-bottom: 0.5rem; font-size: 1.05rem;'>🎮 Simple Game</div>
                <div style='font-size: 0.95rem; color: #374151; font-weight: 500;'>"Make a Rock Paper Scissors game"</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%); padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; border-left: 5px solid #ea580c; box-shadow: 0 3px 10px rgba(0,0,0,0.1);'>
                <div style='font-weight: 700; color: #ea580c; margin-bottom: 0.5rem; font-size: 1.05rem;'>🔐 Password Generator</div>
                <div style='font-size: 0.95rem; color: #374151; font-weight: 500;'>"Write a password generator"</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%); border-radius: 15px; border: 2px solid #1e3c72;'>
            <p style='margin: 0; color: #1e3c72; font-weight: 700; font-size: 1.1rem;'>
                ✨ Type your request below and watch the magic happen! ✨
            </p>
        </div>
    """, unsafe_allow_html=True)