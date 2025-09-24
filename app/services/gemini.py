from __future__ import annotations

import httpx
import orjson
from typing import Any, Dict


API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def _build_prompt_text(request: Dict[str, Any]) -> str:
    description = request["description"]
    language = request["language"]
    variants = int(request["variants"])
    tone = request["tone"]
    explain = bool(request["explain_meanings"])

    lines = [
        "You are a naming expert. Generate YouTube channel NAME IDEAS only.",
        f"Channel description: \"{description}\"",
        f"Target language: {language}",
        f"Tone/style: {tone}",
        "Constraints:",
        "- Names only. No sentences, slogans, or descriptions.",
        "- 1 to 3 words per name, concise, brandable.",
        "- Use only letters and spaces. No punctuation other than spaces. No emojis.",
        "- Avoid offensive content. Avoid numbers unless meaningful.",
        f"- Generate exactly {variants} names.",
        ("- Provide a concise explanation (<=20 words) for each name." if explain else "- Do NOT include explanations."),
        "Output format (STRICT): Return ONLY a JSON object with these fields:",
        ("{\n  \"ideas\": [string, ...],\n  \"explanations\": [string, ...]\n}" if explain else "{\n  \"ideas\": [string, ...]\n}"),
        "No extra text, no markdown, no comments.",
    ]
    return "\n".join(lines)


def generate_names(*, api_key: str, request: Dict[str, Any]) -> Dict[str, Any]:
    if not api_key:
        raise ValueError("Missing Gemini API key")

    prompt_text = _build_prompt_text(request)

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text},
                ]
            }
        ]
    }

    params = {"key": api_key}

    # Simple synchronous call; Streamlit will show a spinner.
    with httpx.Client(timeout=30.0) as client:
        resp = client.post(API_URL, params=params, json=payload)
        if resp.status_code != 200:
            raise RuntimeError(f"Gemini API error: {resp.status_code} {resp.text[:200]}")
        data = resp.json()

    # Attempt to extract JSON string from the model response and parse it.
    text_blocks = []
    for candidate in data.get("candidates", []) or []:
        for part in (candidate.get("content", {}).get("parts", []) or []):
            t = part.get("text")
            if t:
                text_blocks.append(t)

    raw_text = "\n".join(text_blocks).strip()
    if not raw_text:
        return {"ideas": [], "explanations": []}

    # Try to locate a JSON object within the text.
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start != -1 and end != -1 and end > start:
        json_str = raw_text[start : end + 1]
        try:
            parsed = orjson.loads(json_str)
            ideas = parsed.get("ideas") or []
            explanations = parsed.get("explanations") or []
            return {"ideas": ideas, "explanations": explanations}
        except Exception:
            pass

    # Fallback: split lines as names if strict JSON not returned.
    ideas = [line.strip("- •\n ") for line in raw_text.splitlines() if line.strip()]
    ideas = [i for i in ideas if i]
    return {"ideas": ideas[: int(request.get("variants", 10))], "explanations": []}


