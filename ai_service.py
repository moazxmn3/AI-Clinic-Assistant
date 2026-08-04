from google import genai
from config import GEMINI_API_KEY
from prompts import SYSTEM_PROMPT
import json

client = genai.Client(api_key=GEMINI_API_KEY)


def ask_ai(message, clinic_data):

    prompt = f"""
{SYSTEM_PROMPT}

بيانات العيادة:

{json.dumps(clinic_data, ensure_ascii=False, indent=2)}

رسالة العميل:

{message}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text