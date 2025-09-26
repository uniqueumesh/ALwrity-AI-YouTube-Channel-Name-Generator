from __future__ import annotations

from typing import List


def make_simple_text_svg(*, text: str, font_family: str, colors: List[str], width: int = 1024, height: int = 512) -> str:
    safe_text = (text or "").replace("<", "&lt;").replace(">", "&gt;")
    bg = colors[2] if len(colors) > 2 else "#FFFFFF"
    fg = colors[0] if colors else "#000000"
    accent = colors[1] if len(colors) > 1 else fg
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>"
        f"<rect width='100%' height='100%' fill='{bg}'/>"
        f"<text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle'"
        f" font-family='{font_family}' font-size='{int(min(width, height)*0.16)}' fill='{fg}'>"
        f"{safe_text}</text>"
        f"<rect x='{int(width*0.2)}' y='{int(height*0.78)}' width='{int(width*0.6)}' height='{int(height*0.02)}' fill='{accent}' rx='{int(height*0.01)}'/>"
        f"</svg>"
    )


