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

# Custom Luxury Editorial CSS with Parallax & Gold Overrides
st.markdown("""
    <style>
    /* Google Serif & Display Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Cinzel:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500&display=swap');

    /* Global Full-Screen Parallax Background */
    .stApp {
        background: linear-gradient(
            to bottom,
            rgba(15, 11, 7, 0.45),
            rgba(10, 7, 4, 0.85)
        ),
        url('https://images.unsplash.com/photo-1558862107-d49ef2a04d72?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        color: #f7f4ef;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Hide standard Streamlit header & footer */
    header, footer, #MainMenu {
        visibility: hidden;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 6rem !important;
        max-width: 820px !important;
    }

    /* Scroll Motion Animations */
    @keyframes heroFadeIn {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .hero-container {
        animation: heroFadeIn 1.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Editorial Typography */
    .editorial-sub {
        font-family: 'Cinzel', serif;
        letter-spacing: 0.45em;
        text-transform: uppercase;
        font-size: 0.8rem;
        color: #e2c08d;
        text-align: center;
        margin-bottom: 0.6rem;
    }

    .editorial-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 4.5rem;
        font-weight: 300;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #ffffff;
        text-align: center;
        text-shadow: 0 6px 30px rgba(0, 0, 0, 0.7);
        margin-bottom: 0.2rem;
        line-height: 1.1;
    }

    .editorial-tagline {
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        font-size: 1.4rem;
        color: #d4c5b3;
        text-align: center;
        margin-bottom: 3rem;
    }

    /* Frosted Glass Control Panel Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(226, 192, 141, 0.25);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        transition: transform 0.4s ease, border-color 0.4s ease;
    }

    .glass-card:hover {
        border-color: rgba(226, 192, 141, 0.45);
        transform: translateY(-2px);
    }

    /* Override ALL Red Accents in Streamlit Sliders & Inputs */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #e2c08d !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 12px rgba(226, 192, 141, 0.8) !important;
    }

    div[data-baseweb="slider"] div[data-testid="stSliderTickBar"] {
        background-color: rgba(226, 192, 141, 0.3) !important;
    }

    div[data-baseweb="slider"] div {
        color: #e2c08d !important;
    }

    /* Input & Select Box Customization */
    div[data-baseweb="select"], div[data-baseweb="textarea"] {
        background-color: rgba(0, 0, 0, 0.25) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(226, 192, 141, 0.2) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }

    textarea {
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
    }

    textarea::placeholder {
        color: rgba(255, 255, 255, 0.35) !important;
    }

    label p {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
        font-size: 0.78rem !important;
        color: #e2c08d !important;
    }

    /* Gold Action Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #d4a76a 0%, #a3773f 100%) !important;
        color: #ffffff !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.25em !important;
        text-transform: uppercase !important;
        font-size: 0.95rem !important;
        padding: 0.95rem 2rem !important;
        border-radius: 35px !important;
        border: 1px solid rgba(255, 215, 0, 0.4) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
        transition: all 0.35s ease !important;
        margin-top: 1.2rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 35px rgba(212, 167, 106, 0.5) !important;
        background: linear-gradient(135deg, #e2b67a 0%, #b5864a 100%) !important;
    }

    /* Divider Lines */
    .gold-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(226, 192, 141, 0.4), transparent);
        margin: 3.5rem 0 2rem 0;
    }

    /* Audio Player Custom Styling */
    audio {
        width: 100% !important;
        margin-top: 1.5rem !important;
        border-radius: 30px !important;
        filter: invert(0.9) sepia(0.3) saturate(1.8) hue-rotate(340deg);
    }
    </style>
""", unsafe_allow_html=True)

# Editorial Header Component
st.markdown("""
    <div class="hero-container">
        <div class="editorial-sub">Neural Voice Synthesis</div>
        <div class="editorial-title">LUANG PRABANG</div>
        <div class="editorial-tagline">— Experience natural, resonant Lao speech —</div>
    </div>
""", unsafe_allow_html=True)

# Speech Controls Box
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# Voice Selection
voice = st.selectbox(
    "Select Voice Profile",
    ["lo-LA-KeomanyNeural (Female)", "lo-LA-ChanthavongNeural (Male)"]
)
voice_code = voice.split(" ")[0]

# Speed & Pitch Controls placed side-by-side cleanly
ctrl_col1, ctrl_col2 = st.columns(2)

with ctrl_col1:
    speed = st.slider("Playback Speed", min_value=0.6, max_value=1.4, value=1.0, step=0.05)
    rate_str = f"{int((speed - 1.0) * 100):+d}%"

with ctrl_col2:
    pitch = st.slider("Tone / Pitch", min_value=-20, max_value=20, value=0, step=5)
    pitch_str = f"{pitch:+d}Hz"

# Passage Input
lao_text = st.text_area(
    "Lao Script Passage",
    height=210,
    placeholder="ວາງຂໍ້ຄວາມພາສາລາວຢູ່ທີ່ນີ້..."
)

# Async Speech Generator
async def generate_audio(text, voice_name, rate, pitch_val):
    communicate = edge_tts.Communicate(text, voice_name, rate=rate, pitch=pitch_val)
    await communicate.save("output.mp3")

# Trigger Button
if st.button("▶ Synthesize Speech"):
    if lao_text.strip():
        with st.spinner("Synthesizing neural speech..."):
            asyncio.run(generate_audio(lao_text, voice_code, rate_str, pitch_str))
            st.audio("output.mp3", format="audio/mp3", autoplay=True)
            st.success("Playback Ready")
    else:
        st.warning("Please enter or paste Lao text first.")

st.markdown('</div>', unsafe_allow_html=True)

# Minimal Editorial Footer Divider
st.markdown("""
    <div class="gold-divider"></div>
    <div style="text-align: center; font-family: 'Cormorant Garamond', serif; font-style: italic; color: #d4c5b3; font-size: 1.1rem;">
        "The quiet beauty of the ancient sanctuary, echoing through modern neural voice."
    </div>
""", unsafe_allow_html=True)
