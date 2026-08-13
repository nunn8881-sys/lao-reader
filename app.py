import asyncio
import edge_tts
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Lao Text-to-Speech | Neural Reader",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Editorial CSS
st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Cinzel:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500&display=swap');

    /* Full-Screen Misty Luang Prabang Temple Background */
    .stApp {
        background: linear-gradient(
            to bottom,
            rgba(20, 15, 10, 0.40),
            rgba(10, 7, 4, 0.80)
        ),
        url('https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=2000&auto=format&fit=crop');
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

    /* Main Container Padding */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 6rem !important;
        max-width: 800px !important;
    }

    /* Animation */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(18px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .animated-content {
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Editorial Header Typography */
    .editorial-sub {
        font-family: 'Cinzel', serif;
        letter-spacing: 0.45em;
        text-transform: uppercase;
        font-size: 0.82rem;
        color: #e2c08d;
        text-align: center;
        margin-bottom: 0.6rem;
    }

    .editorial-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.8rem;
        font-weight: 300;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #ffffff;
        text-align: center;
        text-shadow: 0 4px 25px rgba(0, 0, 0, 0.7);
        margin-bottom: 0.3rem;
        line-height: 1.1;
    }

    .editorial-tagline {
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        font-size: 1.35rem;
        color: #d4c5b3;
        text-align: center;
        margin-bottom: 2.5rem;
    }

    /* REMOVE DEFAULT RED ACCENTS ON SLIDERS */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #e2c08d !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 10px rgba(226, 192, 141, 0.8) !important;
    }

    div[data-baseweb="slider"] div[data-testid="stSliderTickBar"] {
        background-color: rgba(226, 192, 141, 0.25) !important;
    }

    /* Active slider track gradient override */
    div[data-baseweb="slider"] > div > div > div {
        background: linear-gradient(90deg, #c99e66 0%, #e2c08d 100%) !important;
    }

    div[data-baseweb="slider"] div {
        color: #e2c08d !important;
    }

    /* Form Inputs Styling */
    div[data-baseweb="select"], div[data-baseweb="textarea"] {
        background-color: rgba(0, 0, 0, 0.35) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(226, 192, 141, 0.25) !important;
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
        border: 1px solid rgba(255, 215, 0, 0.35) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
        transition: all 0.35s ease !important;
        margin-top: 1.2rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 35px rgba(212, 167, 106, 0.5) !important;
        background: linear-gradient(135deg, #e2b67a 0%, #b5864a 100%) !important;
    }

    /* Minimal Divider */
    .gold-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(226, 192, 141, 0.35), transparent);
        margin: 3rem 0 2rem 0;
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

# Editorial Header
st.markdown("""
    <div class="animated-content">
        <div class="editorial-sub">Neural Voice Synthesis</div>
        <div class="editorial-title">LAO TEXT TO SPEECH</div>
        <div class="editorial-tagline">— Transform Lao script into natural, resonant voice —</div>
    </div>
""", unsafe_allow_html=True)

# Main Controls Layout (No extra wrap divs)
st.markdown('<div class="animated-content">', unsafe_allow_html=True)

# Voice Selection
voice = st.selectbox(
    "Select Voice Profile",
    ["lo-LA-KeomanyNeural (Female)", "lo-LA-ChanthavongNeural (Male)"]
)
voice_code = voice.split(" ")[0]

# Speed & Pitch Controls
col_speed, col_pitch = st.columns(2)

with col_speed:
    speed = st.slider("Speech Speed", min_value=0.6, max_value=1.4, value=1.0, step=0.05)
    rate_str = f"{int((speed - 1.0) * 100):+d}%"

with col_pitch:
    pitch = st.slider("Voice Tone / Pitch", min_value=-20, max_value=20, value=0, step=5)
    pitch_str = f"{pitch:+d}Hz"

# Text Passage Input
lao_text = st.text_area(
    "Lao Script Passage",
    height=210,
    placeholder="ວາງຂໍ້ຄວາມພາສາລາວຢູ່ທີ່ນີ້..."
)

# Async Audio Generation
async def generate_audio(text, voice_name, rate, pitch_val):
    communicate = edge_tts.Communicate(text, voice_name, rate=rate, pitch=pitch_val)
    await communicate.save("output.mp3")

# Action Button
if st.button("▶ Read Aloud"):
    if lao_text.strip():
        with st.spinner("Synthesizing natural Lao speech..."):
            asyncio.run(generate_audio(lao_text, voice_code, rate_str, pitch_str))
            st.audio("output.mp3", format="audio/mp3", autoplay=True)
            st.success("Playback Ready")
    else:
        st.warning("Please paste Lao script first.")

st.markdown('</div>', unsafe_allow_html=True)

# Minimal Footer
st.markdown("""
    <div class="gold-divider"></div>
    <div style="text-align: center; font-family: 'Cormorant Garamond', serif; font-style: italic; color: #d4c5b3; font-size: 1.1rem;">
        "Resonant Lao neural speech, crafted for long-form listening."
    </div>
""", unsafe_allow_html=True)
