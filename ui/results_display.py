"""
Results display logic for generated names.
"""

import streamlit as st
import streamlit.components.v1 as components
import orjson
import pandas as pd
import io
import html as html_lib
from core.fallback_generator import generate_fallback_names
from logo_generator import render_logo_section


def display_results(names_text):
    """Display generated names with actions"""
    st.markdown('<h3 style="margin-top:2rem; color:#1976D2;">🎬 Generated YouTube Channel Names</h3>', unsafe_allow_html=True)
    
    # Add responsive grid styling
    st.markdown("""
    <style>
    .name-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .name-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .name-title {
        font-size: 1.2em;
        font-weight: 600;
        color: #1976D2;
        text-align: center;
        margin-bottom: 0.75rem;
        word-break: break-word;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
    
    # Display names in optimized multi-column grid
    st.markdown(f'<div style="margin-bottom: 1rem; padding: 0.5rem; background: #e3f2fd; border-radius: 8px; text-align: center;"><strong>📊 Generated {len(names)} unique channel names</strong></div>', unsafe_allow_html=True)
    
    # Calculate number of columns based on screen size (3-4 columns)
    num_columns = min(4, len(names)) if len(names) >= 3 else len(names)
    
    # Create grid layout
    for i in range(0, len(names), num_columns):
        cols = st.columns(num_columns)
        
        for j, col in enumerate(cols):
            if i + j < len(names):
                name = names[i + j]
                idx = i + j
                
                with col:
                    # Enhanced card styling with hover effects (escape name for safety)
                    safe_name = html_lib.escape(name)
                    st.markdown(f'''
                    <div class="name-card">
                        <div class="name-title">{safe_name}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Action buttons in a more compact layout
                    btn_cols = st.columns(2)
                    with btn_cols[0]:
                        # Client-side copy button (no rerun; reliable clipboard)
                        safe_text = orjson.dumps(name).decode()
                        html_tmpl = """
                        <style>
                          #copy-IDX{display:inline-flex;align-items:center;justify-content:center;width:100%;height:40px;background:#1565C0;color:#fff;border:none;border-radius:8px;font-weight:600;cursor:pointer;white-space:nowrap}
                          #copy-IDX.copied{background:#2E7D32}
                        </style>
                        <button id='copy-IDX'>📋 Copy Name</button>
                        <script>
                          (function(){
                            const btn = document.getElementById('copy-IDX');
                            if(!btn) return;
                            btn.addEventListener('click', async () => {
                              try {
                                await navigator.clipboard.writeText(TEXT_PLACE);
                                btn.textContent = '✅ Copied';
                                btn.classList.add('copied');
                              } catch(e){ console.error(e); }
                            });
                          })();
                        </script>
                        """
                        components.html(
                            html_tmpl.replace("IDX", str(idx)).replace("TEXT_PLACE", safe_text),
                            height=46,
                        )
                    
                    with btn_cols[1]:
                        st.button("🎨 Logo", key=f"logo_{idx}", use_container_width=True)
    
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
