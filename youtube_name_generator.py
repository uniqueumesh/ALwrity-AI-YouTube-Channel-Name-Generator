import streamlit as st
import httpx
import orjson
import base64
import io
import pandas as pd
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_random_exponential
from logo_generator import render_logo_section


def main():
    # Set page configuration
    st.set_page_config(
        page_title="ALwrity AI YouTube Channel Name Generator",
        page_icon="🎬",
        layout="wide",
    )
    
    # Custom styling
    st.markdown("""
        <style>
        ::-webkit-scrollbar-track {
            background: #e1ebf9;
        }
        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }
        ::-webkit-scrollbar {
            width: 16px;
        }
        div.stButton > button:first-child {
            background: #1565C0;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    st.title("🎬 ALwrity AI YouTube Channel Name Generator")
    st.caption("Free & Open Source • Powered by Gemini 2.5 Flash")

    # API Configuration Section
    with st.expander("API Configuration 🔑", expanded=False):
        st.markdown('''If the default Gemini API key is unavailable or exceeds its limits, you can provide your own API key below.<br>
        <a href="https://aistudio.google.com/app/apikey" target="_blank">Get Gemini API Key</a>
        ''', unsafe_allow_html=True)
        user_gemini_api_key = st.text_input("Gemini API Key", type="password", help="Paste your Gemini API Key here if you have one. Otherwise, the tool will use the default key if available.")

    
    # Main Input Section
    with st.expander("**PRO-TIP** - Follow the steps below for best results.", expanded=True):
        col1, col2 = st.columns([5, 5])

        with col1:
            input_description = st.text_area(
                '**📝 Enter your channel description!**',
                placeholder="e.g., Tutorials for beginners on Python and data science",
                help="Describe what your YouTube channel is about. Be specific for better results."
            )
            
            input_language = st.selectbox(
                '🌐 Select Language',
                options=["English", "Hindi", "French", "Spanish", "German", "Arabic", "Portuguese", "Bengali", "Japanese", "Korean", "Custom"],
                index=0,
                help="Choose the language for your channel names."
            )
            
            if input_language == "Custom":
                input_language = st.text_input(
                    'Specify Language',
                    placeholder="e.g., Italian, Dutch",
                    help="Specify your preferred language."
                )

        with col2:
            input_tone = st.selectbox(
                '🎭 Channel Tone',
                options=["Friendly", "Professional", "Casual", "Educational", "Playful", "Bold", "Custom"],
                index=0,
                help="Choose the tone that matches your brand."
            )
            
            if input_tone == "Custom":
                input_tone = st.text_input(
                    'Custom Tone',
                    placeholder="e.g., inspirational, minimalist",
                    help="Specify your preferred tone."
                )
            
            input_variants = st.selectbox(
                '📊 Number of Names',
                options=[5, 10, 15, 20],
                index=1,
                help="Choose how many channel names to generate."
            )
            

    # Generate Names Button
    if st.button('**Generate YouTube Channel Names**'):
        with st.spinner("Generating channel names..."):
            if not input_description.strip():
                st.error('**🫣 Please enter a channel description to generate names!**')
            else:
                
                channel_names = generate_youtube_names(
                    input_description, input_language, input_tone, input_variants, 
                    user_gemini_api_key
                )
                
                if channel_names:
                    st.session_state['generated_names'] = channel_names
                else:
                    st.error("💥 **Failed to generate channel names. Please try again!**")
                    st.info("💡 **Tips to fix this:**")
                    st.markdown("""
                    - Try rephrasing your channel description
                    - Use more general keywords
                    - Avoid potentially sensitive topics
                    - Try a different tone or language
                    - Check your API key if using a custom one
                    """)

    # Display Results
    if 'generated_names' in st.session_state and st.session_state['generated_names']:
        display_results(st.session_state['generated_names'])


def generate_youtube_names(description, language, tone, variants, api_key=None):
    """Generate YouTube channel names using improved prompts"""
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


def generate_fallback_names(description, variants):
    """Generate fallback names when API fails"""
    import random
    
    # Extract keywords from description
    words = description.lower().split()
    keywords = [w for w in words if len(w) > 3 and w not in ['the', 'and', 'for', 'with', 'from', 'this', 'that', 'about', 'your', 'channel', 'videos', 'content']]
    
    # Enhanced name templates based on common YouTube niches
    templates = [
        "{keyword} {suffix}",
        "{prefix} {keyword}",
        "{keyword} {keyword2}",
        "{prefix} {keyword} {suffix}",
        "{keyword} {suffix} {suffix2}",
        "{keyword}TV",
        "{keyword}Tube",
        "{keyword}Channel"
    ]
    
    # More relevant prefixes and suffixes
    prefixes = ["Pro", "Elite", "Master", "Prime", "Ultra", "Super", "Max", "Top", "Best", "Great"]
    suffixes = ["Hub", "Zone", "Lab", "Studio", "Academy", "Works", "Pro", "Elite", "TV", "Tube", "Channel", "Media", "Content"]
    
    # Niche-specific suggestions
    niche_suggestions = {
        'cook': ['Kitchen', 'Chef', 'Taste', 'Food', 'Recipe'],
        'tech': ['Tech', 'Code', 'Dev', 'Digital', 'Cyber'],
        'fitness': ['Fit', 'Strong', 'Health', 'Gym', 'Workout'],
        'education': ['Learn', 'Study', 'Academy', 'School', 'Edu'],
        'gaming': ['Game', 'Play', 'Gamer', 'Arcade', 'Quest'],
        'music': ['Music', 'Sound', 'Audio', 'Beat', 'Rhythm'],
        'art': ['Art', 'Creative', 'Design', 'Studio', 'Canvas'],
        'travel': ['Travel', 'Journey', 'Adventure', 'Explore', 'Wander']
    }
    
    # Add niche-specific keywords
    for word in keywords:
        for niche, suggestions in niche_suggestions.items():
            if niche in word.lower():
                keywords.extend(suggestions)
                break
    
    names = []
    used_names = set()
    
    for i in range(variants):
        attempts = 0
        while attempts < 15:
            template = random.choice(templates)
            
            if "{keyword}" in template:
                keyword = random.choice(keywords) if keywords else "Channel"
            else:
                keyword = random.choice(keywords) if keywords else "Channel"
                
            if "{keyword2}" in template:
                keyword2 = random.choice(keywords) if len(keywords) > 1 else "Hub"
            else:
                keyword2 = "Hub"
                
            if "{prefix}" in template:
                prefix = random.choice(prefixes)
            else:
                prefix = "Pro"
                
            if "{suffix}" in template:
                suffix = random.choice(suffixes)
            else:
                suffix = "Hub"
                
            if "{suffix2}" in template:
                suffix2 = random.choice(suffixes)
            else:
                suffix2 = "Pro"
            
            name = template.format(
                keyword=keyword.title(),
                keyword2=keyword2.title(),
                prefix=prefix,
                suffix=suffix,
                suffix2=suffix2
            )
            
            # Clean up the name
            name = name.replace("  ", " ").strip()
            if 8 <= len(name) <= 25 and name not in used_names:
                names.append(name)
                used_names.add(name)
                break
            attempts += 1
    
    # If we don't have enough names, add some generic but relevant ones
    while len(names) < variants:
        generic_names = [
            "Channel Pro", "Content Hub", "Video Zone", "Media Lab", "Creative Studio",
            "Digital Academy", "Video Works", "Content Pro", "Media Hub", "Video Lab",
            "Channel Elite", "Content Zone", "Video Hub", "Media Pro", "Creative Lab"
        ]
        for gen_name in generic_names:
            if gen_name not in used_names and len(names) < variants:
                names.append(gen_name)
                used_names.add(gen_name)
    
    return f'{{"names": {orjson.dumps(names).decode()}}}'


def build_youtube_prompt(description, language, tone, variants):
    """Build simple prompt to avoid safety filtering"""
    
    return f"""Create {variants} YouTube channel names for: {description}

Style: {tone}
Language: {language}

Rules:
- 2-4 words each
- 8-25 characters total
- No numbers or special characters
- Brandable and memorable

Return as JSON: {{"names": ["Name1", "Name2", "Name3"]}}"""


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


def display_results(names_text):
    """Display generated names with actions"""
    st.markdown('<h3 style="margin-top:2rem; color:#1976D2;">🎬 Generated YouTube Channel Names</h3>', unsafe_allow_html=True)
    
    # Parse the response
    try:
        # Try to extract JSON from response
        start = names_text.find('{')
        end = names_text.rfind('}')
        if start != -1 and end != -1:
            json_str = names_text[start:end+1]
            data = orjson.loads(json_str)
            names = data.get('names', [])
        else:
            # Fallback: split by lines and clean up
            lines = names_text.split('\n')
            names = []
            for line in lines:
                line = line.strip('- •\n "')
                # Remove numbering (1., 2., etc.)
                if line and not line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                    # Clean up common prefixes
                    line = line.replace('Name:', '').replace('Channel:', '').strip()
                    if line and len(line) > 2 and len(line) < 50:
                        names.append(line)
    except Exception as e:
        st.warning(f"Failed to parse response: {e}")
        # Final fallback - try to extract any text that looks like a name
        names = []
        lines = names_text.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 2 and len(line) < 50:
                names.append(line)
    
    # Ensure we have valid names
    if not names:
        st.warning("No valid names found. Using fallback names.")
        fallback_response = generate_fallback_names("YouTube channel", 5)
        # Parse fallback response
        start = fallback_response.find('{')
        end = fallback_response.rfind('}')
        if start != -1 and end != -1:
            json_str = fallback_response[start:end+1]
            data = orjson.loads(json_str)
            names = data.get('names', [])
    
    if not names:
        st.warning("No names were returned. Try adjusting your inputs and generate again.")
        return
    
    # Display names
    for idx, name in enumerate(names):
        with st.container(border=True):
            st.markdown(f"**{name}**")
            
            cols = st.columns(2)
            with cols[0]:
                st.button("Copy", key=f"copy_{idx}", on_click=lambda n=name: st.session_state.update({"clipboard": n}))
            with cols[1]:
                st.button("Generate Logo", key=f"logo_{idx}")
    
    # Logo Generation Section
    if names:
        render_logo_section(names)
    
    # Export functionality
    st.markdown('<h4 style="margin-top:2rem;">📤 Export Options</h4>', unsafe_allow_html=True)
    
    # CSV Export
    df = pd.DataFrame({'Channel Name': names})
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    st.download_button(
        label="Download as CSV",
        data=csv_data,
        file_name="youtube_channel_names.csv",
        mime="text/csv"
    )
    
    # Excel Export
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    
    st.download_button(
        label="Download as Excel",
        data=excel_buffer,
        file_name="youtube_channel_names.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )




if __name__ == "__main__":
    main()
