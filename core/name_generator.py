"""
Core name generation logic for YouTube channel names.
"""

def generate_youtube_names(description, language, tone, variants, api_key=None):
    """Generate YouTube channel names using improved prompts"""
    from services.gemini_api import gemini_text_response
    from core.prompt_builder import build_youtube_prompt
    from core.fallback_generator import generate_fallback_names
    import streamlit as st
    
    prompt = build_youtube_prompt(description, language, tone, variants)
    
    try:
        response = gemini_text_response(prompt, api_key)
        if response == 'RATE_LIMIT':
            st.info('ℹ️ Using our smart fallback name generator for better results.')
            return generate_fallback_names(description, variants)
        if response is None:
            st.info('ℹ️ Using our smart fallback name generator for better results.')
            return generate_fallback_names(description, variants)
        return response
    except Exception as e:
        st.info('ℹ️ Using our smart fallback name generator for better results.')
        return generate_fallback_names(description, variants)
