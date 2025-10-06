import asyncio
import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage

# Load environment variables
load_dotenv()

async def test_gemini():
    """Test Gemini connection"""
    print("🧪 Testing Gemini API connection...")
    
    # Get API key and remove quotes if present
    api_key = os.environ.get("GOOGLE_API_KEY", "").strip('"').strip("'")
    
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables")
        return
    
    print(f"✓ API Key found (length: {len(api_key)})")
    
    # Create Gemini model client
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash",
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    
    try:
        # Test with a simple message
        result = await model_client.create([
            UserMessage(content="Say 'Hello, I am Gemini!' in one sentence.", source="user")
        ])
        
        print(f"✅ Success! Gemini responded:")
        print(f"   {result.content}")
        print(f"\n📊 Usage: {result.usage}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await model_client.close()

if __name__ == "__main__":
    asyncio.run(test_gemini())