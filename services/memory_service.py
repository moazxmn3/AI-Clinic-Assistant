from collections import defaultdict

# تخزين المحادثات في الذاكرة
_sessions = defaultdict(list)

# أقصى عدد رسائل يتم الاحتفاظ به لكل Session
MAX_HISTORY = 20


def add_message(session_id: str, role: str, message: str):
    """
    إضافة رسالة جديدة إلى سجل المحادثة.
    """

    _sessions[session_id].append({
        "role": role,
        "message": message
    })

    # الاحتفاظ بآخر MAX_HISTORY رسالة فقط
    if len(_sessions[session_id]) > MAX_HISTORY:
        _sessions[session_id] = _sessions[session_id][-MAX_HISTORY:]


def get_history(session_id: str) -> str:
    """
    تحويل سجل المحادثة إلى نص لإرساله إلى Gemini.
    """

    history = _sessions.get(session_id, [])

    if not history:
        return "لا يوجد سجل محادثة سابق."

    conversation = []

    for item in history:
        speaker = "المستخدم" if item["role"] == "user" else "المساعد"

        conversation.append(
            f"{speaker}: {item['message']}"
        )

    return "\n".join(conversation)


def clear_history(session_id: str):
    """
    حذف سجل جلسة معينة.
    """

    _sessions.pop(session_id, None)