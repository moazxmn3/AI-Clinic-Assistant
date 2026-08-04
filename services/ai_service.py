from google import genai

from config import GEMINI_API_KEY
from services.memory_service import add_message, get_history
from services.guardrails import is_allowed
from services.prompt_builder import build_prompt


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


client = genai.Client(api_key=GEMINI_API_KEY)


def ask_ai(
    session_id: str,
    message: str,
    clinic_data: dict,
) -> str:
    """
    Main AI Service
    """

    # حفظ رسالة المستخدم
    add_message(
        session_id=session_id,
        role="user",
        message=message,
    )

    # Guardrails
    if not is_allowed(message):

        reply = (
            "أنا مساعد خاص بالعيادة، "
            "وأقدر أساعد فقط في الأسئلة المتعلقة "
            "بالأطباء والخدمات والأسعار والمواعيد."
        )

        add_message(
            session_id=session_id,
            role="assistant",
            message=reply,
        )

        return reply

    # قراءة سجل المحادثة
    history = get_history(session_id)

    # بناء الـ Prompt
    prompt = build_prompt(
        clinic_data=clinic_data,
        history=history,
        user_message=message,
    )

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        reply = (
            response.text.strip()
            if response.text
            else "عذرًا، لم أتمكن من إنشاء رد."
        )

    except Exception as e:

        print(e)

        reply = (
            "حدث خطأ أثناء الاتصال بخدمة الذكاء الاصطناعي."
        )

    # حفظ رد المساعد
    add_message(
        session_id=session_id,
        role="assistant",
        message=reply,
    )

    return reply