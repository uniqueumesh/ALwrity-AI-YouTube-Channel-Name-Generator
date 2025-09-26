from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LogoRequest:
    names: List[str]
    style: str
    font_family: str
    palette_name: str
    custom_colors: Optional[List[str]]
    size_px: int
    want_svg: bool
    want_png: bool
    icon_keyword: Optional[str]
    use_ai: bool = False
    style_prompt: Optional[str] = None


def validate_logo_request(req: LogoRequest) -> LogoRequest:
    names = [n.strip() for n in req.names if isinstance(n, str) and n.strip()]
    if not names:
        raise ValueError("At least one name must be selected for logo generation")
    size_px = req.size_px if req.size_px in (1024, 2048) else 1024
    return LogoRequest(
        names=names,
        style=req.style or "Minimal",
        font_family=req.font_family or "Inter",
        palette_name=req.palette_name or "Monochrome",
        custom_colors=req.custom_colors or None,
        size_px=size_px,
        want_svg=bool(req.want_svg),
        want_png=bool(req.want_png),
        icon_keyword=(req.icon_keyword or None),
        use_ai=bool(getattr(req, "use_ai", False)),
        style_prompt=(getattr(req, "style_prompt", None) or None),
    )


