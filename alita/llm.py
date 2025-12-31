
import os, json, requests, re

LANG_RULE = (
    "IMPORTANT LANGUAGE RULE:\n"
    "- You MUST reply in Simplified Chinese only.\n"
    "- Do NOT use English unless it appears in command output.\n"
)

BASE_RULES = (
    "No markdown. No code fences. Output plain text only. "
    "Total output under 300 tokens."
)

def _call_llm(system, messages):
    base  = os.getenv("ANTHROPIC_BASE_URL")
    key   = os.getenv("ANTHROPIC_API_KEY")
    model = os.getenv("ANTHROPIC_MODEL")
    if not all([base, key, model]):
        raise RuntimeError("Missing LLM env vars")

    payload = {
        "model": model,
        "max_tokens": 300,
        "temperature": 0,
        "system": system,
        "messages": messages,
    }

    r = requests.post(
        base.rstrip("/") + "/v1/messages",
        headers={
            "content-type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01"
        },
        data=json.dumps(payload),
        timeout=30
    )
    if r.status_code != 200:
        raise RuntimeError(r.text)

    text = ""
    for b in r.json().get("content", []):
        if b.get("type") == "text":
            text += b.get("text","")
    return text.strip()

def _extract_command(text):
    matches = re.findall(r"\{[^{}]*\"command\"[^{}]*\}", text, re.S)
    for m in reversed(matches):
        try:
            obj = json.loads(m)
            if isinstance(obj, dict) and "command" in obj:
                cleaned = text.replace(m, "").strip()
                return cleaned, obj["command"]
        except Exception:
            continue
    return text, None

def think_cmd(user, context):
    system = (
        LANG_RULE +
        "Phase: THINK.\n"
        "Your task: propose ONE best diagnostic command.\n"
        "Output explanation + JSON {\"command\":\"<cmd>\"}.\n"
        + BASE_RULES
    )
    text = _call_llm(system, [
        {"role": "user", "content": user if not context else f"{user}\nContext:\n{context}"}
    ])
    return _extract_command(text)

def analyze_output(output):
    system = (
        LANG_RULE +
        "Phase: ANALYZE.\n"
        "Explain the meaning of the output.\n"
        "Do NOT suggest commands.\n"
        + BASE_RULES
    )
    return _call_llm(system, [
        {"role": "user", "content": output}
    ])

def recommend_next(context):
    system = (
        LANG_RULE +
        "Phase: RECOMMEND.\n"
        "Recommend ONE next diagnostic command.\n"
        "Output ONLY the command.\n"
        + BASE_RULES
    )
    return _call_llm(system, [
        {"role": "user", "content": context}
    ])
