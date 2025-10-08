"""
Gemini API integration for name generation.
"""

from tenacity import retry, stop_after_attempt, wait_random_exponential
import streamlit as st

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_text_response(prompt, user_gemini_api_key=None):
    """Call Gemini API with retry logic"""
    import google.generativeai as genai
    import os
    
    try:
        api_key = user_gemini_api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            st.error("GEMINI_API_KEY is missing. Please provide it in the API Configuration section or set it in the environment.")
            return None
        genai.configure(api_key=api_key)
    except Exception as err:
        st.error(f"Failed to configure Gemini: {err}")
        return None
    
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 512
    }
    
    model = genai.GenerativeModel(model_name="gemini-2.5-flash", generation_config=generation_config)
    
    try:
        response = model.generate_content(prompt)
        
        # Check for rate limits
        if hasattr(response, 'code') and response.code == 429:
            return 'RATE_LIMIT'
        
        # Check for safety filtering (finish_reason = 2)
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'finish_reason') and candidate.finish_reason == 2:
                return None
        
        # Check for quota issues
        if hasattr(response, 'text') and response.text:
            if 'rate limit' in response.text.lower() or 'quota' in response.text.lower():
                return 'RATE_LIMIT'
            return response.text
        else:
            return None
            
    except Exception as err:
        if 'quota' in str(err).lower() or 'rate limit' in str(err).lower():
            return 'RATE_LIMIT'
        if 'finish_reason' in str(err).lower() or 'filtered' in str(err).lower():
            return None
        return None
