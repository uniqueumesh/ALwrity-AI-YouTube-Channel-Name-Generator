from __future__ import annotations

import streamlit as st

from app.core.logo import LogoRequest, validate_logo_request
from app.services.logo.template import generate_template_svgs
from app.services.logo.ai import generate_ai_logos
from app.utils.colors import DEFAULT_PALETTES


def render_logo_section(available_names: list[str]) -> None:
    if not available_names:
        return

    with st.expander("Logo previews (optional)", expanded=False):
        st.caption("Generate quick logo previews for one or more names.")

        selected = st.multiselect("Select names", options=available_names, default=available_names[:1])
        style = st.selectbox("Style preset", ["Minimal", "Bold", "Playful", "Professional", "Retro", "Modern", "Gradient"], index=0)
        font = st.selectbox("Font family", ["Inter", "Poppins", "Montserrat", "Roboto Slab", "Abril Fatface", "Custom"], index=0)
        custom_font = ""
        if font == "Custom":
            custom_font = st.text_input("Custom font family", placeholder="e.g., Lato")

        palette_name = st.selectbox("Color palette", list(DEFAULT_PALETTES.keys()) + ["Custom"], index=0)
        custom_colors: list[str] | None = None
        if palette_name == "Custom":
            col1, col2, col3 = st.columns(3)
            with col1:
                c1 = st.color_picker("Primary", value="#111111")
            with col2:
                c2 = st.color_picker("Accent", value="#E91E63")
            with col3:
                c3 = st.color_picker("Background", value="#FAFAFA")
            custom_colors = [c1, c2, c3]

        size_px = st.selectbox("Size (px)", options=[1024, 2048], index=0)
        want_png = st.checkbox("Export PNG", value=True)
        want_svg = st.checkbox("Export SVG", value=True)

        st.markdown("---")
        use_ai = st.checkbox("Use AI-assisted logos (Gemini)", value=False)
        style_prompt = None
        api_key = None
        if use_ai:
            style_prompt = st.text_input("Style prompt (optional)", placeholder="e.g., minimalist, geometric accent")
            api_key = st.text_input("Gemini API Key (for logos)", type="password", placeholder="Paste your Gemini API key")

        if st.button("Generate Logos"):
            try:
                req = validate_logo_request(
                    LogoRequest(
                        names=selected,
                        style=style,
                        font_family=(custom_font or font),
                        palette_name=palette_name,
                        custom_colors=custom_colors,
                        size_px=int(size_px),
                        want_svg=bool(want_svg),
                        want_png=bool(want_png),
                        icon_keyword=None,
                        use_ai=bool(use_ai),
                        style_prompt=style_prompt,
                    )
                )
            except Exception as exc:
                st.error(str(exc))
                return

            with st.spinner("Generating logos..."):
                svgs = generate_template_svgs(
                    names=req.names,
                    palette_name=req.palette_name,
                    custom_colors=req.custom_colors,
                    font_family=req.font_family,
                    size_px=req.size_px,
                )

                ai_images = {}
                if req.use_ai and api_key:
                    try:
                        ai_images = generate_ai_logos(
                            api_key=api_key,
                            names=req.names,
                            style=req.style,
                            style_prompt=req.style_prompt,
                            size_px=req.size_px,
                        )
                    except Exception as e:
                        st.warning(f"AI-assisted logo generation failed. Falling back to template only. ({e})")

            st.subheader("Logo previews")
            for name in req.names:
                with st.container(border=True):
                    st.markdown(f"**{name}**")
                    if name in ai_images:
                        st.markdown(ai_images[name], unsafe_allow_html=True)
                        st.caption(f"{name} — AI (Gemini) {req.style} (SVG)")
                    if name in svgs:
                        # Streamlit doesn't reliably render raw SVG via st.image; embed as HTML instead
                        st.markdown(svgs[name], unsafe_allow_html=True)
                        st.caption(f"{name} — Template {req.style} (SVG preview)")
                        st.download_button(
                            label="Download SVG",
                            data=svgs[name].encode("utf-8"),
                            file_name=f"{name.replace(' ', '_')}_{req.style.lower()}_{req.size_px}.svg",
                            mime="image/svg+xml",
                            key=f"dl_svg_{name}",
                        )


