import streamlit as st
import orjson
from typing import List, Dict, Optional


def generate_logos(names, style, font, colors, size, use_ai, api_key):
    """Generate logos for selected names"""
    logos = {}
    
    # Get color palette
    color_palette = get_color_palette(colors)
    
    for name in names:
        if use_ai and api_key:
            # Try AI generation first
            ai_logo = generate_ai_logo(name, style, api_key, size)
            if ai_logo:
                logos[name] = ai_logo
                continue
        
        # Fallback to template
        template_logo = create_template_logo(name, style, font, color_palette, size)
        logos[name] = template_logo
    
    return logos


def get_color_palette(palette_name):
    """Get color palette for logos"""
    palettes = {
        "Monochrome": ["#111111", "#444444", "#EEEEEE"],
        "Warm": ["#C0392B", "#E67E22", "#F1C40F"],
        "Cool": ["#2980B9", "#16A085", "#1ABC9C"],
        "Vibrant": ["#9B59B6", "#E74C3C", "#2ECC71"],
    }
    return palettes.get(palette_name, palettes["Monochrome"])


def create_template_logo(text, style, font, colors, size):
    """Create template-based SVG logo"""
    safe_text = (text or "").replace("<", "&lt;").replace(">", "&gt;")
    bg = colors[2] if len(colors) > 2 else "#FFFFFF"
    fg = colors[0] if colors else "#000000"
    accent = colors[1] if len(colors) > 1 else fg
    
    width = size
    height = int(size / 2)
    font_size = int(min(width, height) * 0.12)
    
    if style.lower() == "minimal":
        return create_minimal_logo(safe_text, font, fg, accent, bg, width, height, font_size)
    elif style.lower() == "bold":
        return create_bold_logo(safe_text, font, fg, accent, bg, width, height, font_size)
    elif style.lower() == "playful":
        return create_playful_logo(safe_text, font, fg, accent, bg, width, height, font_size)
    elif style.lower() == "professional":
        return create_professional_logo(safe_text, font, fg, accent, bg, width, height, font_size)
    elif style.lower() == "modern":
        return create_modern_logo(safe_text, font, fg, accent, bg, width, height, font_size)
    elif style.lower() == "retro":
        return create_retro_logo(safe_text, font, fg, accent, bg, width, height, font_size)
    elif style.lower() == "gradient":
        return create_gradient_logo(safe_text, font, fg, accent, bg, width, height, font_size)
    else:
        return create_minimal_logo(safe_text, font, fg, accent, bg, width, height, font_size)


def create_minimal_logo(text, font, fg, accent, bg, width, height, font_size):
    """Clean, simple design"""
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
        <rect width='100%' height='100%' fill='{bg}'/>
        <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='{font}, sans-serif' font-size='{font_size}' font-weight='300' fill='{fg}'>{text}</text>
        <rect x='{int(width*0.2)}' y='{int(height*0.75)}' width='{int(width*0.6)}' height='2' fill='{accent}'/>
    </svg>"""


def create_bold_logo(text, font, fg, accent, bg, width, height, font_size):
    """Strong typography with shadow effects"""
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
        <defs>
            <filter id='boldShadow' x='-50%' y='-50%' width='200%' height='200%'>
                <feDropShadow dx='3' dy='3' stdDeviation='4' flood-color='{fg}60'/>
            </filter>
        </defs>
        <rect width='100%' height='100%' fill='{bg}'/>
        <rect x='{int(width*0.1)}' y='{int(height*0.2)}' width='{int(width*0.8)}' height='{int(height*0.6)}' fill='{accent}10' rx='{int(height*0.05)}'/>
        <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='{font}, sans-serif' font-size='{font_size}' font-weight='900' fill='{fg}' filter='url(#boldShadow)'>{text}</text>
    </svg>"""


def create_playful_logo(text, font, fg, accent, bg, width, height, font_size):
    """Colorful elements, circles, gradients"""
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
        <defs>
            <linearGradient id='playfulGrad' x1='0%' y1='0%' x2='100%' y2='100%'>
                <stop offset='0%' stop-color='{bg}'/>
                <stop offset='100%' stop-color='{accent}20'/>
            </linearGradient>
        </defs>
        <rect width='100%' height='100%' fill='url(#playfulGrad)'/>
        <circle cx='{int(width*0.15)}' cy='{int(height*0.25)}' r='{int(height*0.08)}' fill='{accent}'/>
        <circle cx='{int(width*0.85)}' cy='{int(height*0.75)}' r='{int(height*0.06)}' fill='{fg}30'/>
        <circle cx='{int(width*0.1)}' cy='{int(height*0.8)}' r='{int(height*0.04)}' fill='{accent}60'/>
        <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='{font}, sans-serif' font-size='{font_size}' font-weight='600' fill='{fg}'>{text}</text>
        <rect x='{int(width*0.2)}' y='{int(height*0.7)}' width='{int(width*0.6)}' height='{int(height*0.05)}' fill='{accent}' rx='{int(height*0.025)}'/>
    </svg>"""


def create_professional_logo(text, font, fg, accent, bg, width, height, font_size):
    """Structured layout with borders"""
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
        <rect width='100%' height='100%' fill='{bg}'/>
        <rect x='{int(width*0.05)}' y='{int(height*0.1)}' width='{int(width*0.9)}' height='{int(height*0.8)}' fill='none' stroke='{accent}' stroke-width='2' rx='{int(height*0.02)}'/>
        <rect x='{int(width*0.1)}' y='{int(height*0.15)}' width='{int(width*0.8)}' height='{int(height*0.7)}' fill='{accent}05' rx='{int(height*0.01)}'/>
        <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='{font}, sans-serif' font-size='{font_size}' font-weight='500' fill='{fg}'>{text}</text>
        <rect x='{int(width*0.2)}' y='{int(height*0.8)}' width='{int(width*0.6)}' height='1' fill='{accent}'/>
    </svg>"""


def create_modern_logo(text, font, fg, accent, bg, width, height, font_size):
    """Geometric shapes, linear gradients"""
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
        <defs>
            <linearGradient id='modernGrad' x1='0%' y1='0%' x2='100%' y2='0%'>
                <stop offset='0%' stop-color='{accent}'/>
                <stop offset='100%' stop-color='{fg}'/>
            </linearGradient>
        </defs>
        <rect width='100%' height='100%' fill='{bg}'/>
        <polygon points='{int(width*0.1)},{int(height*0.1)} {int(width*0.9)},{int(height*0.1)} {int(width*0.8)},{int(height*0.9)} {int(width*0.2)},{int(height*0.9)}' fill='url(#modernGrad)' opacity='0.1'/>
        <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='{font}, sans-serif' font-size='{font_size}' font-weight='400' fill='{fg}'>{text}</text>
        <rect x='{int(width*0.3)}' y='{int(height*0.7)}' width='{int(width*0.4)}' height='{int(height*0.02)}' fill='{accent}'/>
    </svg>"""


def create_retro_logo(text, font, fg, accent, bg, width, height, font_size):
    """Patterned backgrounds, vintage styling"""
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
        <defs>
            <pattern id='retroPattern' x='0' y='0' width='20' height='20' patternUnits='userSpaceOnUse'>
                <rect width='20' height='20' fill='{bg}'/>
                <circle cx='10' cy='10' r='1' fill='{accent}20'/>
            </pattern>
        </defs>
        <rect width='100%' height='100%' fill='url(#retroPattern)'/>
        <rect x='{int(width*0.1)}' y='{int(height*0.2)}' width='{int(width*0.8)}' height='{int(height*0.6)}' fill='{accent}15' stroke='{accent}' stroke-width='3' rx='{int(height*0.05)}'/>
        <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='{font}, serif' font-size='{font_size}' font-weight='700' fill='{fg}'>{text}</text>
        <rect x='{int(width*0.2)}' y='{int(height*0.8)}' width='{int(width*0.6)}' height='{int(height*0.03)}' fill='{accent}' rx='{int(height*0.015)}'/>
    </svg>"""


def create_gradient_logo(text, font, fg, accent, bg, width, height, font_size):
    """Beautiful color transitions"""
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
        <defs>
            <linearGradient id='textGrad' x1='0%' y1='0%' x2='100%' y2='0%'>
                <stop offset='0%' stop-color='{fg}'/>
                <stop offset='100%' stop-color='{accent}'/>
            </linearGradient>
            <radialGradient id='bgGrad' cx='50%' cy='50%' r='50%'>
                <stop offset='0%' stop-color='{bg}'/>
                <stop offset='100%' stop-color='{accent}10'/>
            </radialGradient>
        </defs>
        <rect width='100%' height='100%' fill='url(#bgGrad)'/>
        <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='{font}, sans-serif' font-size='{font_size}' font-weight='600' fill='url(#textGrad)'>{text}</text>
        <ellipse cx='50%' cy='{int(height*0.75)}' rx='{int(width*0.3)}' ry='{int(height*0.02)}' fill='{accent}' opacity='0.6'/>
    </svg>"""


def generate_ai_logo(name, style, api_key, size):
    """Generate AI-assisted logo using Gemini"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        prompt = f"""Create a simple, clean, brandable logo as pure SVG markup (vector).
        Channel name: '{name}'. Desired style: {style}.
        Constraints:
        - Flat design, high legibility, no photorealism.
        - Typography-centric logo with optional minimal geometric shape.
        - No external images, no scripts, no external references.
        - Viewbox 0 0 {size} {int(size/2)}, responsive width/height.
        Output strictly as JSON with one field: svg (a single string containing the full <svg>...</svg>). No extra text."""
        
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        response = model.generate_content(prompt)
        
        if response and response.text:
            # Try to extract SVG from response
            start = response.text.find('{')
            end = response.text.rfind('}')
            if start != -1 and end != -1:
                json_str = response.text[start:end+1]
                data = orjson.loads(json_str)
                svg = data.get('svg', '').strip()
                if svg and svg.lower().startswith('<svg') and svg.lower().endswith('</svg>'):
                    return svg
    except:
        pass
    return None


def render_logo_section(names):
    """Render the logo generation section in Streamlit"""
    if not names:
        return
    
    with st.expander("🎨 Logo Generation (Optional)", expanded=False):
        st.caption("Generate quick logo previews for your channel names.")
        
        selected_names = st.multiselect("Select names for logos", options=names, default=names[:1])
        
        if selected_names:
            col1, col2 = st.columns(2)
            
            with col1:
                logo_style = st.selectbox("Logo Style", ["Minimal", "Bold", "Playful", "Professional", "Modern", "Retro", "Gradient"], index=0)
                logo_font = st.selectbox("Font Family", ["Inter", "Poppins", "Montserrat", "Roboto Slab", "Abril Fatface"], index=0)
                logo_colors = st.selectbox("Color Palette", ["Monochrome", "Warm", "Cool", "Vibrant", "Custom"], index=0)
            
            with col2:
                logo_size = st.selectbox("Size (px)", [1024, 2048], index=0)
                use_ai = st.checkbox("Use AI-assisted logos (Gemini)", value=False)
                ai_api_key = None
                if use_ai:
                    ai_api_key = st.text_input("Gemini API Key (for logos)", type="password", placeholder="Paste your Gemini API key")
            
            if st.button("Generate Logos"):
                with st.spinner("Generating logos..."):
                    logos = generate_logos(selected_names, logo_style, logo_font, logo_colors, logo_size, use_ai, ai_api_key)
                    
                    if logos:
                        st.markdown('<h4 style="margin-top:1rem;">🎨 Generated Logos</h4>', unsafe_allow_html=True)
                        for name, logo_svg in logos.items():
                            with st.container(border=True):
                                st.markdown(f"**{name}**")
                                st.markdown(logo_svg, unsafe_allow_html=True)
                                
                                st.download_button(
                                    label="Download SVG",
                                    data=logo_svg.encode("utf-8"),
                                    file_name=f"{name.replace(' ', '_')}_{logo_style.lower()}_{logo_size}.svg",
                                    mime="image/svg+xml",
                                    key=f"dl_svg_{name}"
                                )
