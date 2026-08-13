cat << 'EOF' > app.py
import asyncio
import edge_tts
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="LUANG PRABANG | Lao Voice Reader",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Full-Screen Luxury Custom CSS
st.markdown("""
    <style>
    /* Import Google Serif & Display Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Cinzel:wght@400;600&family=Plus+Jakarta+Sans:wght@300;400;500&display=swap');

    /* Global Page Styling with Full-Screen Background Image */
    .stApp {
        background: linear-gradient(
            to bottom,
            rgba(20, 15, 10, 0.45),
            rgba(15, 10, 5, 0.75)
        ),
        url('https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        color: #f7f4ef;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Hide standard Streamlit header & footer elements */
    header, footer, #MainMenu {
        visibility: hidden;
    }

    /* Main Container Padding & Centering */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 5rem !important;
        max-width: 850px !important;
    }

    /* Editorial Title Typography */
    .editorial-sub {
        font-family: 'Cinzel', serif;
        letter-spacing: 0.35em;
        text-transform: uppercase;
        font-size: 0.85rem;
        color: #e2c08d;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .editorial-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.8rem;
        font-weight: 400;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #ffffff;
        text-align: center;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        margin-bottom: 0.2rem;
    }

    .editorial-tagline {
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        font-size: 1.3rem;
        color: #d4c5b3;
        text-align: center;
        margin-bottom: 2.5rem;
    }

    /* Glassmorphism Card Wrapper around Input Controls */
    div[data-baseweb="select"], div[data-baseweb="textarea"] {
        background-color: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }

    /* Text Area Styling */
    textarea {
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }

    textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }

    /* Dropdown Text Styling */
    div[data-baseweb="select"] * {
        color: #ffffff !important;
    }

    /* Label Styling */
    label p {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        font-size: 0.8rem !important;
        color: #e2c08d !important;
    }

    /* Primary Action Button (Gold / Bronze Accent) */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #c99e66 0%, #9e733b 100%) !important;
        color: #ffffff !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.2em !important;
        text-transform: uppercase !important;
        font-size: 0.95rem !important;
        padding: 0.85rem 2rem !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
        margin-top: 1rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(201, 158, 102, 0.5) !important;
        background: linear-gradient(135deg, #d8ac74 0%, #b08247 100%) !important;
    }

    /* Audio Player Styling */
    audio {
        width: 100% !important;
        margin-top: 1.5rem !important;
        border-radius: 30px !important;
        filter: invert(0.9) sepia(0.2) saturate(1.5) hue-rotate(350deg);
    }
    </style>
""", unsafe_allow_html=True)

# Editorial Header HTML
st.markdown("""
    <div class="editorial-sub">Lao Neural Reader</div>
    <div class="editorial-title">LUANG PRABANG</div>
    <div class="editorial-tagline">— Transform Lao script into natural, resonant voice —</div>
""", unsafe_allow_html=True)

# Dropdown Voice Selection
voice = st.selectbox(
    "Select Voice Profile",
    ["lo-LA-KeomanyNeural (Female)", "lo-LA-ChanthavongNeural (Male)"]
)
voice_code = voice.split(" ")[0]

# Text Input Area
lao_text = st.text_area(
    "Lao Passage",
    height=220,
    placeholder="ວາງຂໍ້ຄວາມພາສາລາວຢູ່ທີ່ນີ້..."
)

# Async TTS Generation Function
async def generate_audio(text, voice_name):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save("output.mp3")

# Read Aloud Trigger
if st.button("▶ Listen in Lao"):
    if lao_text.strip():
        with st.spinner("Synthesizing neural speech..."):
            asyncio.run(generate_audio(lao_text, voice_code))
            st.audio("output.mp3", format="audio/mp3", autoplay=True)
            st.success("Playback Ready")
    else:
        st.warning("Please enter or paste Lao text first.")
EOF
