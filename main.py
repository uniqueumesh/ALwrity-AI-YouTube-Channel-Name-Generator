"""
Main Streamlit application for YouTube Channel Name Generator.
Clean modular architecture following best programming practices.
"""

import streamlit as st
from core.name_generator import generate_youtube_names
from ui.results_display import display_results

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


if __name__ == "__main__":
    main()
