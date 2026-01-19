import os
import google.generativeai as genai

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure Gemini
genai.configure(api_key=api_key)

# Use the model name exactly as listed
model = genai.GenerativeModel("models/gemini-flash-latest")

# Test prompt
response = model.generate_content("Say hello in one sentence")

print(response.text)
