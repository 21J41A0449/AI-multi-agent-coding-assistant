import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY").strip('"').strip("'")

# Initialize the client
client = genai.Client(api_key=api_key)

# List available models
print("Available Gemini models:")
print("="*60)
for model in client.models.list():
    print(f"- {model.name}")
    if hasattr(model, 'supported_generation_methods'):
        print(f"  Methods: {model.supported_generation_methods}")