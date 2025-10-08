"""
Results display logic for generated names.
"""

import streamlit as st
import orjson
import pandas as pd
import io
from core.fallback_generator import generate_fallback_names
from logo_generator import render_logo_section

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
