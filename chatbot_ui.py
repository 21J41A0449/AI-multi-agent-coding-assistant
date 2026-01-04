"""
Multi-Agent Coding Assistant - Enhanced Streamlit Interface
A professional AI coding assistant with file management, code execution, and persistence.
"""

import asyncio
import os
import sys
import re
import streamlit as st
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo
from dotenv import load_dotenv

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

# Import our modules
from modules.file_manager import get_file_manager, FileManager
from modules.database import get_database, Database
from modules.code_executor import get_executor
from modules.git_manager import get_git_manager

# Syntax highlighting
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
    from pygments.formatters import HtmlFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="AI Coding Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        --primary-dark: #0F172A;
        --primary-navy: #1E293B;
        --primary-slate: #334155;
        --accent-blue: #3B82F6;
        --accent-cyan: #06B6D4;
        --accent-purple: #8B5CF6;
        --success-green: #10B981;
        --warning-orange: #F59E0B;
        --error-red: #EF4444;
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --text-muted: #94A3B8;
        --glass-bg: rgba(30, 41, 59, 0.8);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main .block-container {
        padding: 1.5rem 2rem;
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.98));
        border-radius: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin: 1rem;
        border: 1px solid var(--glass-border);
    }
    
    h1 {
        background: linear-gradient(135deg, #F8FAFC 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .stCaption {
        text-align: center;
        font-size: 1rem !important;
        color: var(--text-secondary) !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-right: 1px solid var(--glass-border);
    }
    
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    
    /* Chat styling */
    .stChatMessage, .stChatMessage > div, [data-testid="stChatMessageContent"] {
        background: var(--primary-navy) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
    }
    
    .stChatMessage * {
        color: var(--text-primary) !important;
        background: transparent !important;
    }
    
    /* Code blocks - VISIBLE */
    pre, code {
        display: block !important;
        background: #0F172A !important;
        color: #E2E8F0 !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    pre {
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        border: 1px solid var(--accent-blue) !important;
        overflow-x: auto !important;
    }
    
    .stMarkdown pre, .stMarkdown code {
        display: block !important;
    }
    
    /* Chat input */
    .stChatInputContainer, [data-testid="stChatInput"], [data-testid="stBottom"], 
    [data-testid="stBottom"] *, .stChatFloatingInputContainer, .stChatFloatingInputContainer * {
        background: var(--primary-dark) !important;
    }
    
    .stChatInputContainer textarea {
        background: var(--primary-slate) !important;
        border: 1px solid var(--glass-border) !important;
        color: var(--text-primary) !important;
    }
    
    /* Header */
    header, [data-testid="stHeader"] {
        background: var(--primary-dark) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    /* File tree styling */
    .file-tree {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    .file-tree-item {
        padding: 4px 8px;
        border-radius: 4px;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .file-tree-item:hover {
        background: rgba(59, 130, 246, 0.2);
    }
    
    .file-icon { margin-right: 6px; }
    .folder-icon { color: #F59E0B; }
    .file-icon-py { color: #3B82F6; }
    .file-icon-js { color: #F59E0B; }
    .file-icon-md { color: #10B981; }
    
    /* Agent badges */
    .agent-badge {
        display: inline-flex;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.8rem;
        margin-bottom: 8px;
    }
    .researcher-badge { background: linear-gradient(135deg, #3B82F6, #1D4ED8); color: white; }
    .coder-badge { background: linear-gradient(135deg, #8B5CF6, #7C3AED); color: white; }
    .tester-badge { background: linear-gradient(135deg, #10B981, #059669); color: white; }
    
    /* Copy button */
    .copy-btn {
        position: absolute;
        top: 8px;
        right: 8px;
        background: var(--accent-blue);
        color: white;
        border: none;
        padding: 4px 8px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.75rem;
    }
    
    /* Conversation selector */
    .conversation-item {
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 4px;
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid transparent;
        cursor: pointer;
    }
    .conversation-item:hover {
        border-color: var(--accent-blue);
    }
    .conversation-item.active {
        background: rgba(59, 130, 246, 0.2);
        border-color: var(--accent-blue);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--primary-dark); }
    ::-webkit-scrollbar-thumb { background: var(--primary-slate); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ===== Initialize Services =====
load_dotenv()

@st.cache_resource
def init_services():
    """Initialize all services (cached)."""
    workspace = os.path.dirname(__file__)
    return {
        'file_manager': get_file_manager(workspace),
        'database': get_database(),
        'executor': get_executor(workspace),
        'git': get_git_manager(workspace)
    }

services = init_services()
file_manager = services['file_manager']
database = services['database']
executor = services['executor']
git_manager = services['git']

# ===== Session State =====
def init_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("GOOGLE_API_KEY")
    
    if "conversation_id" not in st.session_state:
        conv = database.get_or_create_default_conversation()
        st.session_state.conversation_id = conv.id
        # Load existing messages
        messages = database.get_messages(conv.id)
        st.session_state.messages = [
            {"role": m.role, "content": m.content} for m in messages
        ]
    
    if "selected_file" not in st.session_state:
        st.session_state.selected_file = None
    
    if "show_file_content" not in st.session_state:
        st.session_state.show_file_content = False

init_session_state()

# ===== Helper Functions =====
def get_file_icon(filename: str) -> str:
    """Get icon for file type."""
    ext = os.path.splitext(filename)[1].lower()
    icons = {
        '.py': '🐍', '.js': '📜', '.ts': '📘', '.jsx': '⚛️', '.tsx': '⚛️',
        '.html': '🌐', '.css': '🎨', '.json': '📋', '.md': '📝',
        '.txt': '📄', '.yml': '⚙️', '.yaml': '⚙️', '.env': '🔐',
        '.git': '📦', '.sql': '🗃️', '.sh': '💻', '.bat': '💻',
    }
    return icons.get(ext, '📄')

def render_file_tree(tree: dict, level: int = 0):
    """Render file tree in sidebar."""
    if not tree:
        return
    
    indent = "  " * level
    name = tree.get('name', '')
    path = tree.get('path', '')
    is_dir = tree.get('is_dir', False)
    children = tree.get('children', [])
    
    if level > 0:  # Skip root
        if is_dir:
            st.markdown(f"{indent}📁 **{name}**")
        else:
            icon = get_file_icon(name)
            if st.button(f"{indent}{icon} {name}", key=f"file_{path}", use_container_width=True):
                st.session_state.selected_file = path
                st.session_state.show_file_content = True
    
    for child in children:
        render_file_tree(child, level + 1)

def highlight_code(code: str, language: str = None) -> str:
    """Apply syntax highlighting to code."""
    if not PYGMENTS_AVAILABLE:
        return f"<pre><code>{code}</code></pre>"
    
    try:
        if language:
            lexer = get_lexer_by_name(language)
        else:
            lexer = guess_lexer(code)
    except:
        lexer = TextLexer()
    
    formatter = HtmlFormatter(
        style='monokai',
        noclasses=True,
        nowrap=False
    )
    return highlight(code, lexer, formatter)

def save_message(role: str, content: str):
    """Save message to database and session."""
    st.session_state.messages.append({"role": role, "content": content})
    database.save_message(st.session_state.conversation_id, role, content)

# ===== Sidebar =====
with st.sidebar:
    # Header
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <div style='font-size: 2.5rem;'>🤖</div>
            <h2 style='margin: 0.5rem 0;'>AI Coding Assistant</h2>
            <p style='font-size: 0.85rem; color: #94A3B8;'>Multi-Agent System</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Tabs for sidebar sections (no Files tab)
    tab1, tab2 = st.tabs(["💬 History", "⚙️ Settings"])
    
    with tab1:
        # Conversation History
        st.markdown("#### Conversations")
        
        if st.button("➕ New Chat", use_container_width=True):
            conv = database.create_conversation()
            st.session_state.conversation_id = conv.id
            st.session_state.messages = []
            st.rerun()
        
        conversations = database.list_conversations(limit=10)
        for conv in conversations:
            is_active = conv.id == st.session_state.conversation_id
            status = "🔵" if is_active else "⚪"
            
            if st.button(f"{status} {conv.title[:25]}...", key=f"conv_{conv.id}", use_container_width=True):
                st.session_state.conversation_id = conv.id
                messages = database.get_messages(conv.id)
                st.session_state.messages = [
                    {"role": m.role, "content": m.content} for m in messages
                ]
                st.rerun()
    
    with tab2:
        # Settings
        st.markdown("#### Active Agents")
        st.markdown("🔍 **Researcher** - Analyzes & plans")
        st.markdown("💻 **Coder** - Writes code")
        st.markdown("✅ **Tester** - Reviews & validates")
        
        st.divider()
        
        st.markdown("#### Model")
        st.markdown("🧠 Gemini 2.5 Flash")
        
        st.divider()
        
        # Git status
        st.markdown("#### Git Status")
        git_status = git_manager.get_status()
        if git_status.is_repo:
            st.markdown(f"🌿 Branch: **{git_status.branch}**")
            if git_status.has_changes:
                st.markdown(f"📝 Modified: {len(git_status.modified_files)}")
        else:
            st.markdown("*Not a git repository*")
        
        st.divider()
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            database.delete_conversation(st.session_state.conversation_id)
            conv = database.create_conversation()
            st.session_state.conversation_id = conv.id
            st.rerun()

# ===== Main Content Area =====
# Two-column layout: Chat + File Viewer
if st.session_state.show_file_content and st.session_state.selected_file:
    col1, col2 = st.columns([2, 1])
else:
    col1 = st.container()
    col2 = None

with col1:
    st.title("🤖 AI Coding Assistant")
    st.caption("Describe what you want to build and watch your AI team collaborate!")
    
    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)
        elif role == "Researcher":
            with st.chat_message("assistant", avatar="🔍"):
                st.markdown('<div class="agent-badge researcher-badge">🔍 RESEARCHER</div>', unsafe_allow_html=True)
                st.markdown(content)
        elif role == "Coder":
            with st.chat_message("assistant", avatar="💻"):
                st.markdown('<div class="agent-badge coder-badge">💻 CODER</div>', unsafe_allow_html=True)
                st.markdown(content)
        elif role == "Tester":
            with st.chat_message("assistant", avatar="✅"):
                st.markdown('<div class="agent-badge tester-badge">✅ TESTER</div>', unsafe_allow_html=True)
                st.markdown(content)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(content)

# File Viewer Column
if col2:
    with col2:
        st.markdown("#### 📄 File Viewer")
        
        if st.button("✖️ Close", key="close_file"):
            st.session_state.show_file_content = False
            st.rerun()
        
        file_path = st.session_state.selected_file
        st.markdown(f"**{file_path}**")
        
        content = file_manager.read_file(file_path)
        if content:
            ext = os.path.splitext(file_path)[1].lower()
            lang_map = {'.py': 'python', '.js': 'javascript', '.json': 'json', '.md': 'markdown'}
            lang = lang_map.get(ext, 'text')
            st.code(content, language=lang)
        else:
            st.error("Could not read file")

# ===== Chat Input =====
user_input = st.chat_input("What would you like me to build?")

async def run_multi_agent_system(task: str, api_key: str):
    """Run the multi-agent system."""
    
    # Add project context to task
    project_summary = file_manager.get_project_summary()
    
    enhanced_task = f"""
Project Context:
{project_summary}

User Request:
{task}
"""
    
    gemini_model_info = ModelInfo(
        family="gemini-2.5-flash",
        vision=True,
        function_calling=True,
        json_output=True,
        structured_output=True
    )
    
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        model_info=gemini_model_info
    )
    
    researcher = AssistantAgent(
        name="Researcher",
        model_client=model_client,
        system_message="""You are a Researcher agent in an AI coding team. Your role is to:
1. Analyze the coding task thoroughly
2. Consider the existing project context
3. Break it down into clear, actionable steps
4. Identify key requirements and potential challenges
5. Create a detailed plan for the Coder to follow

Be concise but thorough. Focus on the technical approach."""
    )
    
    coder = AssistantAgent(
        name="Coder",
        model_client=model_client,
        system_message="""You are a Coder agent in an AI coding team. Your role is to:
1. Review the Researcher's plan
2. Write clean, efficient, and well-documented code
3. Follow best practices and coding standards
4. Include comments explaining key parts
5. Provide complete, working code that can be run immediately

Always include the full code, not snippets."""
    )
    
    tester = AssistantAgent(
        name="Tester",
        model_client=model_client,
        system_message="""You are a Tester agent in an AI coding team. Your role is to:
1. Review the code written by the Coder
2. Check for bugs, errors, and potential issues
3. Verify that it meets the original requirements
4. Suggest improvements if needed

If the code is good, respond with "TERMINATE" to end the conversation.
If there are issues, provide specific feedback."""
    )
    
    termination = TextMentionTermination("TERMINATE")
    
    team = RoundRobinGroupChat(
        participants=[researcher, coder, tester],
        termination_condition=termination,
        max_turns=15
    )
    
    stream = team.run_stream(task=enhanced_task)
    
    async for message in stream:
        yield message

def sync_run_agents(task: str, api_key: str):
    """Synchronous wrapper for running agents."""
    try:
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
    if not st.session_state.api_key:
        st.error("⚠️ Please set GOOGLE_API_KEY in your .env file!")
        st.stop()
    
    # Save user message
    save_message("user", user_input)
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Update conversation title from first message
    if len(st.session_state.messages) == 1:
        title = user_input[:50] + "..." if len(user_input) > 50 else user_input
        database.update_conversation_title(st.session_state.conversation_id, title)
    
    # Run agents
    with st.spinner("🤖 AI agents are collaborating..."):
        st.markdown("""
            <div style='text-align: center; padding: 2rem; background: rgba(59, 130, 246, 0.1); 
                        border-radius: 12px; margin: 1rem 0; border: 1px solid rgba(59, 130, 246, 0.2);'>
                <div style='font-size: 2rem;'>⚡</div>
                <div style='font-weight: 600; color: #F8FAFC;'>Your AI Team is Working...</div>
                <div style='color: #94A3B8; margin-top: 0.5rem;'>Researcher → Coder → Tester</div>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            messages = sync_run_agents(user_input, st.session_state.api_key)
            
            for msg in messages:
                if hasattr(msg, 'source') and hasattr(msg, 'content'):
                    agent_name = msg.source
                    content = msg.content
                    
                    if not content or not content.strip():
                        continue
                    
                    # Save to database
                    save_message(agent_name, content)
                    
                    # Display
                    if agent_name == "Researcher":
                        with st.chat_message("assistant", avatar="🔍"):
                            st.markdown('<div class="agent-badge researcher-badge">🔍 RESEARCHER</div>', unsafe_allow_html=True)
                            st.markdown(content)
                    elif agent_name == "Coder":
                        with st.chat_message("assistant", avatar="💻"):
                            st.markdown('<div class="agent-badge coder-badge">💻 CODER</div>', unsafe_allow_html=True)
                            st.markdown(content)
                    elif agent_name == "Tester":
                        with st.chat_message("assistant", avatar="✅"):
                            st.markdown('<div class="agent-badge tester-badge">✅ TESTER</div>', unsafe_allow_html=True)
                            st.markdown(content)
                elif "error" in msg:
                    st.error(f"❌ Error: {msg['error']}")
            
            st.balloons()
            st.success("✅ Task completed!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Welcome message
if len(st.session_state.messages) == 0:
    st.markdown("""<div style='background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95)); padding: 2rem; border-radius: 16px; text-align: center; border: 1px solid rgba(255,255,255,0.1);'>
<h2 style='color: #F8FAFC; margin-bottom: 1rem;'>👋 Welcome!</h2>
<p style='color: #94A3B8;'>Your AI coding team is ready to help.</p>
<div style='display: flex; justify-content: center; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap;'>
<div style='background: rgba(59, 130, 246, 0.15); padding: 1rem; border-radius: 10px; min-width: 120px;'>
<div style='font-size: 1.5rem;'>🔍</div>
<div style='color: #3B82F6; font-weight: 600;'>Researcher</div>
</div>
<div style='background: rgba(139, 92, 246, 0.15); padding: 1rem; border-radius: 10px; min-width: 120px;'>
<div style='font-size: 1.5rem;'>💻</div>
<div style='color: #8B5CF6; font-weight: 600;'>Coder</div>
</div>
<div style='background: rgba(16, 185, 129, 0.15); padding: 1rem; border-radius: 10px; min-width: 120px;'>
<div style='font-size: 1.5rem;'>✅</div>
<div style='color: #10B981; font-weight: 600;'>Tester</div>
</div>
</div>
<p style='color: #64748B; font-size: 0.9rem;'>💡 Try: "Create a calculator in Python" or "Build a Flask API"</p>
</div>""", unsafe_allow_html=True)