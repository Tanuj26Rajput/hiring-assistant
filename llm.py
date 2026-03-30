from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def gemi_invoke(prompt: str) -> str:
    try:
        response = client_gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            return "fallback"   # ✅ safety

        return response.text.strip()

    except Exception as e:
        print("Gemini API Error:", e)
        return "fallback"   # ✅ NEVER ""

