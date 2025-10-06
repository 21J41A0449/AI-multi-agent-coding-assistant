"""
Quick test to verify ModelInfo configuration works
"""
from autogen_ext.models.openai._model_info import ModelInfo

# Test the ModelInfo with all required fields
try:
    gemini_model_info = ModelInfo(
        family="gemini-2.0-flash-exp",
        vision=True,
        function_calling=True,
        json_output=True,
        structured_output=True
    )
    print("✅ ModelInfo created successfully!")
    print(f"   Family: {gemini_model_info.get('family')}")
    print(f"   Vision: {gemini_model_info.get('vision')}")
    print(f"   Function Calling: {gemini_model_info.get('function_calling')}")
    print(f"   JSON Output: {gemini_model_info.get('json_output')}")
    print(f"   Structured Output: {gemini_model_info.get('structured_output')}")
    print("\n✅ All fields are properly set!")
except Exception as e:
    print(f"❌ Error creating ModelInfo: {e}")
    import traceback
    traceback.print_exc()