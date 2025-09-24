from typing import Any, Dict
import re


def build_generation_request(
    *,
    description: str,
    language: str,
    variants: int,
    tone: str,
    explain_meanings: bool,
) -> Dict[str, Any]:
    if variants not in {5, 10, 15, 20}:
        raise ValueError("variants must be one of 5, 10, 15, 20")

    return {
        "description": description,
        "language": language,
        "variants": variants,
        "tone": tone,
        "explain_meanings": explain_meanings,
    }


def sanitize_ideas(ideas: list[str]) -> list[str]:
    """Filter out items that look like sentences or are too long.

    Keep short, name-like phrases (1-3 words, letters/spaces only).
    """
    cleaned: list[str] = []
    pattern = re.compile(r"^[A-Za-z][A-Za-z ]{0,29}$")
    for item in ideas:
        candidate = (item or "").strip()
        if not candidate:
            continue
        if len(candidate.split()) > 3:
            continue
        if not pattern.match(candidate):
            continue
        cleaned.append(candidate)
    return cleaned


