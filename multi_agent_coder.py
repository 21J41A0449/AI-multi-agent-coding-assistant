import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables with explicit path
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

# If not loaded from .env, try reading the file directly
if not api_key:
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('GOOGLE_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    break
    except Exception as e:
        print(f"Warning: Could not read .env file: {e}")

if not api_key:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

# Strip any quotes that might be in the .env file
api_key = api_key.strip('"').strip("'")

print(f"✓ API Key loaded (length: {len(api_key)})")

# --- 1. Configure Gemini Model Client ---
# Using Gemini through OpenAI-compatible endpoint with model_info to bypass validation
from autogen_ext.models.openai._model_info import ModelInfo

# Create custom model info for Gemini
gemini_model_info = ModelInfo(
    family="gemini",
    vision=True,
    function_calling=True,
    json_output=True,
    structured_output=True
)

model_client = OpenAIChatCompletionClient(
    model="gemini-2.5-flash",
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    model_info=gemini_model_info,
)

print("✓ Gemini model client configured (via OpenAI-compatible API)")

# --- 2. Define the Agents ---

# Agent 1: Researcher
researcher = AssistantAgent(
    name="Researcher",
    model_client=model_client,
    system_message="""You are a senior research analyst. Your role is to understand the user's request,
    identify the core problem, and break it down into a clear, step-by-step plan for the Coder.
    Do not write any code. Your final output should be a well-defined plan.""",
)

# Agent 2: Coder
coder = AssistantAgent(
    name="Coder",
    model_client=model_client,
    system_message="""You are a Python developer. You will receive a plan from the Researcher.
    Your job is to write clean, efficient, and correct Python code to implement that plan.
    Wrap your final Python code in a single ```python code block.
    Do not add any explanations outside the code block.""",
)

# Agent 3: Tester
tester = AssistantAgent(
    name="Tester",
    model_client=model_client,
    system_message="""You are a quality assurance engineer and Python expert.
    Your role is to review the code provided by the Coder.
    Check for correctness, bugs, and adherence to best practices.
    If the code is perfect, respond with "TERMINATE".
    If there are issues, provide clear, actionable feedback to the Coder.""",
)

print("✓ Three agents created: Researcher, Coder, Tester")

# --- 3. Set up the Round Robin Group Chat ---
termination = TextMentionTermination("TERMINATE")

team = RoundRobinGroupChat(
    participants=[researcher, coder, tester],
    termination_condition=termination,
    max_turns=10,
)

print("✓ Round-robin group chat configured")

# --- 4. Main Execution Block ---

async def main():
    """
    The main asynchronous function to run the agent chat.
    """
    print("\n" + "="*70)
    print("🤖 Welcome to the Multi-Agent Coding Assistant")
    print("   Powered by Google Gemini 1.5 Flash")
    print("="*70)
    
    # Get the task from the user
    task = input("\nPlease enter the coding task you want to solve: \n> ")
    
    print(f"\n🚀 Starting agent collaboration...")
    print(f"   Task: '{task}'")
    print("-"*70 + "\n")

    # Run the team chat and stream messages
    async for message in team.run_stream(task=task):
        if hasattr(message, 'source') and hasattr(message, 'content'):
            print(f"\n[{message.source}]:")
            print(f"{message.content}")
            print("-" * 70)
    
    print("\n" + "="*70)
    print("✅ Agent collaboration completed!")
    print("="*70)

if __name__ == "__main__":
    # Run the main asynchronous function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user. Exiting.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()