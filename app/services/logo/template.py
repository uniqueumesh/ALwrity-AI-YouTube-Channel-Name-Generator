from __future__ import annotations

from typing import Dict, List

from app.utils.colors import get_palette
from app.utils.svg import make_simple_text_svg


def generate_template_svgs(*, names: List[str], palette_name: str, custom_colors: List[str] | None, font_family: str, size_px: int) -> Dict[str, str]:
    palette = get_palette(palette_name, custom_colors)
    outputs: Dict[str, str] = {}
    for n in names:
        svg = make_simple_text_svg(text=n, font_family=font_family, colors=palette, width=size_px, height=int(size_px/2))
        outputs[n] = svg
    return outputs


