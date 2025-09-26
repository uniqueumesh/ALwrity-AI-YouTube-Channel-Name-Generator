from __future__ import annotations

from typing import List


DEFAULT_PALETTES: dict[str, list[str]] = {
    "Monochrome": ["#111111", "#444444", "#EEEEEE"],
    "Warm": ["#C0392B", "#E67E22", "#F1C40F"],
    "Cool": ["#2980B9", "#16A085", "#1ABC9C"],
    "Vibrant": ["#9B59B6", "#E74C3C", "#2ECC71"],
}


def sanitize_hex(color: str) -> str:
    value = (color or "").strip()
    if not value:
        return "#000000"
    if value.startswith("#"):
        value = value[1:]
    value = value[:6]
    for ch in value:
        if ch.lower() not in "0123456789abcdef":
            return "#000000"
    return f"#{value.upper():0<6}"


def get_palette(name: str, custom: list[str] | None = None) -> List[str]:
    if name == "Custom" and custom:
        return [sanitize_hex(c) for c in custom if c]
    return DEFAULT_PALETTES.get(name, DEFAULT_PALETTES["Monochrome"])  # type: ignore[return-value]


