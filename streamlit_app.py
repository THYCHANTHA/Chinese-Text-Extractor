import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import io
from PIL import Image
import base64
from datetime import datetime
import json
from streamlit_option_menu import option_menu

# Try to import pyzbar, but make it optional
try:
    from pyzbar.pyzbar import decode
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False
    st.warning("⚠️ QR code scanning is not available. Please install system dependencies (libzbar0) to enable this feature.")

# Page configuration
st.set_page_config(
    page_title="CNVid2Text - Chinese Text Extractor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #1d4ed8;
        --success-color: #10b981;
        --danger-color: #ef4444;
        --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    /* Card styling */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.15);
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Success message */
    .success-box {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Error message */
    .error-box {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        font-family: 'Courier New', monospace;
    }
    
    /* Sidebar styling - much more stable selector */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Ensure the navigation container is also transparent */
    [data-testid="stSidebarNav"] {
        background-color: transparent !important;
    }

    /* Ensure all text in sidebar is readable */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {
        color: white !important;
    }

    /* Fix for the option menu background */
    .nav-link {
        background-color: transparent !important;
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .nav-link:hover {
        color: white !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }

    .nav-link.active {
        color: white !important;
        background-color: rgba(255, 255, 255, 0.2) !important;
        font-weight: bold !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated {
        animation: fadeIn 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'extraction_history' not in st.session_state:
    st.session_state.extraction_history = []
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'current_url' not in st.session_state:
    st.session_state.current_url = ""

# Functions
def extract_text_from_url(url):
    """Extract Chinese text from a given URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract text from common content tags
        all_text = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'div', 'span', 'li']):
            text = tag.get_text(strip=True)
            if text and re.search(r'[\u4e00-\u9fff]', text):  # Contains Chinese characters
                all_text.append(text)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_text = []
        for line in all_text:
            if line not in seen and len(line) > 5:  # Filter out very short lines
                seen.add(line)
                unique_text.append(line)
        
        extracted_text = '\n\n'.join(unique_text)
        
        if not extracted_text:
            return None, "No Chinese text found on this page."
        
        return extracted_text, None
        
    except requests.exceptions.RequestException as e:
        return None, f"Error fetching the page: {str(e)}"
    except Exception as e:
        return None, f"Error processing the page: {str(e)}"

def decode_qr_code(image):
    """Decode QR code from image"""
    if not PYZBAR_AVAILABLE:
        return None, "QR code scanning is not available on this server. Please provide a URL directly."
    try:
        decoded_objects = decode(image)
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8'), None
        else:
            return None, "No QR code detected in the image."
    except Exception as e:
        return None, f"Error decoding QR code: {str(e)}"

def analyze_text(text):
    """Analyze extracted text and return statistics"""
    if not text:
        return {}
    
    lines = text.split('\n')
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    words = text.split()
    
    return {
        'total_characters': len(text),
        'chinese_characters': len(chinese_chars),
        'total_lines': len([line for line in lines if line.strip()]),
        'total_words': len(words),
        'paragraphs': len([p for p in text.split('\n\n') if p.strip()])
    }

def create_download_link(text, filename):
    """Create a download link for text"""
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="download-link">📥 Download as TXT</a>'

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h1 style='color: white; font-size: 2rem;'>🎬 CNVid2Text</h1>
        <p style='color: rgba(255,255,255,0.8);'>Professional Text Extractor</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Extract", "History", "About"],
        icons=["search", "clock-history", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "white",
                "--hover-color": "rgba(255,255,255,0.1)"
            },
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        }
    )
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    auto_analyze = st.checkbox("Auto-analyze text", value=True)
    show_stats = st.checkbox("Show statistics", value=True)
    
    st.markdown("---")
    
    # Quick stats
    if st.session_state.extraction_history:
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Extractions", len(st.session_state.extraction_history))
        st.metric("Last Extraction", 
                 st.session_state.extraction_history[-1]['timestamp'].strftime("%H:%M"))

# Main content
if selected == "Extract":
    # Header
    st.markdown("""
    <div class='main-header animated'>
        <h1>🎬 Chinese Text Extractor</h1>
        <p>Extract Chinese text from video pages via URL or QR code - Fast, Accurate, Professional</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input methods
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔗 Method 1: URL Input")
        url_input = st.text_input(
            "Enter video page URL",
            placeholder="https://tv.cctv.com/...",
            help="Paste the URL of a Chinese video page (e.g., CCTV, news sites)"
        )
        
        if st.button("🚀 Extract from URL", use_container_width=True):
            if url_input:
                with st.spinner("🔍 Extracting text from URL..."):
                    text, error = extract_text_from_url(url_input)
                    
                    if error:
                        st.markdown(f"""
                        <div class='error-box'>
                            <strong>❌ Error:</strong> {error}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.session_state.extracted_text = text
                        st.session_state.current_url = url_input
                        
                        # Add to history
                        st.session_state.extraction_history.append({
                            'timestamp': datetime.now(),
                            'url': url_input,
                            'method': 'URL',
                            'text_length': len(text)
                        })
                        
                        st.markdown("""
                        <div class='success-box'>
                            <strong>✅ Success!</strong> Text extracted successfully!
                        </div>
                        """, unsafe_allow_html=True)
                        st.rerun()
            else:
                st.warning("⚠️ Please enter a URL")
    
    with col2:
        st.markdown("### 📸 Method 2: QR Code Upload")
        uploaded_file = st.file_uploader(
            "Upload QR code image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload an image containing a QR code with the video URL"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded QR Code", use_container_width=True)
            
            if st.button("🔓 Decode & Extract", use_container_width=True, disabled=not PYZBAR_AVAILABLE):
                if not PYZBAR_AVAILABLE:
                    st.error("QR code scanning is not supported in this environment.")
                else:
                    with st.spinner("🔍 Decoding QR code and extracting text..."):
                        # Decode QR
                        url, qr_error = decode_qr_code(image)
                        
                        if qr_error:
                            st.markdown(f"""
                            <div class='error-box'>
                                <strong>❌ Error:</strong> {qr_error}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.info(f"🔗 Decoded URL: {url}")
                            
                            # Extract text
                            text, extract_error = extract_text_from_url(url)
                            
                            if extract_error:
                                st.markdown(f"""
                                <div class='error-box'>
                                    <strong>❌ Error:</strong> {extract_error}
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.session_state.extracted_text = text
                                st.session_state.current_url = url
                                
                                # Add to history
                                st.session_state.extraction_history.append({
                                    'timestamp': datetime.now(),
                                    'url': url,
                                    'method': 'QR Code',
                                    'text_length': len(text)
                                })
                                
                                st.markdown("""
                                <div class='success-box'>
                                    <strong>✅ Success!</strong> QR code decoded and text extracted!
                                </div>
                                """, unsafe_allow_html=True)
                                st.rerun()
    
    # Display extracted text
    if st.session_state.extracted_text:
        st.markdown("---")
        st.markdown("## 📄 Extracted Text")
        
        # Statistics
        if show_stats:
            stats = analyze_text(st.session_state.extracted_text)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown(f"""
                <div class='stats-card'>
                    <p class='stats-number'>{stats['total_characters']}</p>
                    <p class='stats-label'>Characters</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='stats-card'>
                    <p class='stats-number'>{stats['chinese_characters']}</p>
                    <p class='stats-label'>Chinese Chars</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='stats-card'>
                    <p class='stats-number'>{stats['total_lines']}</p>
                    <p class='stats-label'>Lines</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class='stats-card'>
                    <p class='stats-number'>{stats['total_words']}</p>
                    <p class='stats-label'>Words</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                st.markdown(f"""
                <div class='stats-card'>
                    <p class='stats-number'>{stats['paragraphs']}</p>
                    <p class='stats-label'>Paragraphs</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Text display and actions
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown(f"**Source:** {st.session_state.current_url[:50]}...")
        
        with col2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.code(st.session_state.extracted_text, language=None)
                st.success("✅ Text ready to copy!")
        
        with col3:
            # Download button
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chinese_text_{timestamp}.txt"
            st.download_button(
                label="📥 Download TXT",
                data=st.session_state.extracted_text,
                file_name=filename,
                mime="text/plain",
                use_container_width=True
            )
        
        with col4:
            # Download as JSON
            json_data = {
                'url': st.session_state.current_url,
                'extracted_at': datetime.now().isoformat(),
                'text': st.session_state.extracted_text,
                'statistics': analyze_text(st.session_state.extracted_text) if auto_analyze else {}
            }
            st.download_button(
                label="📥 Download JSON",
                data=json.dumps(json_data, ensure_ascii=False, indent=2),
                file_name=f"chinese_text_{timestamp}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Text area
        st.text_area(
            "Extracted Chinese Text",
            value=st.session_state.extracted_text,
            height=400,
            help="The extracted Chinese text from the video page"
        )
        
        # Clear button
        if st.button("🗑️ Clear Results", use_container_width=False):
            st.session_state.extracted_text = ""
            st.session_state.current_url = ""
            st.rerun()

elif selected == "History":
    st.markdown("""
    <div class='main-header animated'>
        <h1>📜 Extraction History</h1>
        <p>View your previous text extractions</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.extraction_history:
        st.markdown(f"### Total Extractions: {len(st.session_state.extraction_history)}")
        
        # Display history in reverse order (newest first)
        for idx, item in enumerate(reversed(st.session_state.extraction_history)):
            with st.expander(f"🕐 {item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {item['method']}"):
                st.markdown(f"**URL:** {item['url']}")
                st.markdown(f"**Method:** {item['method']}")
                st.markdown(f"**Text Length:** {item['text_length']} characters")
                st.markdown(f"**Time:** {item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.extraction_history = []
            st.rerun()
    else:
        st.info("📭 No extraction history yet. Start extracting text to see your history here!")

elif selected == "About":
    st.markdown("""
    <div class='main-header animated'>
        <h1>ℹ️ About CNVid2Text</h1>
        <p>Professional Chinese Text Extraction Tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>🎯 Features</h3>
            <ul>
                <li>✅ Extract Chinese text from video pages</li>
                <li>✅ Support URL and QR code input</li>
                <li>✅ Real-time text analysis</li>
                <li>✅ Multiple export formats (TXT, JSON)</li>
                <li>✅ Extraction history tracking</li>
                <li>✅ Professional, modern UI</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3>🚀 How to Use</h3>
            <ol>
                <li><strong>URL Method:</strong> Paste a video page URL and click "Extract from URL"</li>
                <li><strong>QR Code Method:</strong> Upload a QR code image and click "Decode & Extract"</li>
                <li>View extracted text with statistics</li>
                <li>Download as TXT or JSON format</li>
                <li>Check your extraction history</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>💡 Supported Sources</h3>
            <ul>
                <li>🎬 CCTV Video Pages</li>
                <li>📰 Chinese News Websites</li>
                <li>🎥 Video Summary Pages</li>
                <li>📺 Broadcasting Platforms</li>
                <li>🔗 Any page with Chinese text</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3>🛠️ Technology Stack</h3>
            <ul>
                <li>🐍 Python 3.12</li>
                <li>🎈 Streamlit</li>
                <li>🌐 BeautifulSoup4</li>
                <li>📸 Pillow & pyzbar</li>
                <li>🎨 Custom CSS Styling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h3>🏆 Powered by InsightCode Academy</h3>
        <p style='color: #666; margin-top: 1rem;'>
            Professional text extraction tool for Chinese video content<br>
            Version 2.0 - Streamlit Edition
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Made with ❤️ by InsightCode Academy | © 2026 CNVid2Text</p>
</div>
""", unsafe_allow_html=True)
