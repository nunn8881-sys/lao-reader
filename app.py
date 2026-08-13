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

# Full-Screen Luxury Custom CSS with Scroll Animations & Styling
st.markdown("""
    <style>
    /* Import Google Serif & Display Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Cinzel:wght@400;600&family=Plus+Jakarta+Sans:wght@300;400;500&display=swap');

    /* Global Page Background */
    .stApp {
        background: linear-gradient(
            to bottom,
            rgba(18, 14, 10, 0.55),
            rgba(12, 9, 6, 0.85)
        ),
        url('https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        color: #f7f4ef;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Hide standard Streamlit elements */
    header, footer, #MainMenu {
        visibility: hidden;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 900px !important;
    }

    /* Scroll Animation Effects */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(25px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animated-section {
        animation: fadeInUp 0.8s ease-out forwards;
    }

    /* Typography */
    .editorial-sub {
        font-family: 'Cinzel', serif;
        letter-spacing: 0.4em;
        text-transform: uppercase;
        font-size: 0.85rem;
        color: #e2c08d;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .editorial-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 4.2rem;
        font-weight: 400;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #ffffff;
        text-align: center;
        text-shadow: 0 4px 25px rgba(0, 0, 0, 0.6);
        margin-bottom: 0.2rem;
    }

    .editorial-tagline {
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        font-size: 1.35rem;
        color: #d4c5b3;
        text-align: center;
        margin-bottom: 2.5rem;
    }

    /* Glassmorphism Input Styling */
    div[data-baseweb="select"], div[data-baseweb="textarea"], div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
    }

    textarea {
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }

    textarea::placeholder {
        color: rgba(255, 255, 255, 0.45) !important;
    }

    label p {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        font-size: 0.82rem !important;
        color: #e2c08d !important;
    }

    /* Slider Customization */
    div[data-baseweb="slider"] * {
        color: #e2c08d !important;
    }

    /* Golden Action Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #c99e66 0%, #9e733b 100%) !important;
        color: #ffffff !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.22em !important;
        text-transform: uppercase !important;
        font-size: 0.95rem !important;
        padding: 0.9rem 2rem !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255, 215, 0, 0.35) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.3s ease !important;
        margin-top: 1rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(201, 158, 102, 0.55) !important;
        background: linear-gradient(135deg, #d8ac74 0%, #b08247 100%) !important;
    }

    /* Editorial Image Cards Gallery */
    .gallery-card {
        background-size: cover;
        background-position: center;
        height: 260px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
        display: flex;
        align-items: flex-end;
        padding: 1.2rem;
        margin-top: 1.5rem;
    }

    .gallery-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 15px 35px rgba(226, 192, 141, 0.25);
    }

    .card-caption {
        font-family: 'Cinzel', serif;
        font-size: 0.85rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #ffffff;
        background: rgba(0, 0, 0, 0.45);
        backdrop-filter: blur(8px);
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
    }

    /* Audio Bar */
    audio {
        width: 100% !important;
        margin-top: 1.5rem !important;
        border-radius: 30px !important;
        filter: invert(0.9) sepia(0.2) saturate(1.5) hue-rotate(350deg);
    }
    </style>
""", unsafe_allow_html=True)

# Editorial Header Component
st.markdown("""
    <div class="animated-section">
        <div class="editorial-sub">Lao Neural Reader</div>
        <div class="editorial-title">LUANG PRABANG</div>
        <div class="editorial-tagline">— Transform Lao script into natural, resonant voice —</div>
    </div>
""", unsafe_allow_html=True)

# Main Form Controls inside animated container
st.markdown('<div class="animated-section">', unsafe_allow_html=True)

# Voice Selection & Speech Settings Controls
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    voice = st.selectbox(
        "Select Voice Profile",
        ["lo-LA-KeomanyNeural (Female)", "lo-LA-ChanthavongNeural (Male)"]
    )
    voice_code = voice.split(" ")[0]

with col2:
    # Speed Adjuster
    speed = st.slider("Speech Speed", min_value=0.5, max_value=1.5, value=1.0, step=0.1)
    # Convert slider value to edge-tts rate parameter (e.g., '+0%', '-20%', '+30%')
    rate_str = f"{int((speed - 1.0) * 100):+d}%"

with col3:
    # Pitch Adjuster
    pitch = st.slider("Voice Pitch", min_value=-20, max_value=20, value=0, step=5)
    pitch_str = f"{pitch:+d}Hz"

# Text Area
lao_text = st.text_area(
    "Lao Passage",
    height=200,
    placeholder="ວາງຂໍ້ຄວາມພາສາລາວຢູ່ທີ່ນີ້..."
)

# Async TTS Generation with Speed & Pitch Parameters
async def generate_audio(text, voice_name, rate, pitch_val):
    communicate = edge_tts.Communicate(text, voice_name, rate=rate, pitch=pitch_val)
    await communicate.save("output.mp3")

# Action Trigger
if st.button("▶ Listen in Lao"):
    if lao_text.strip():
        with st.spinner("Synthesizing neural speech..."):
            asyncio.run(generate_audio(lao_text, voice_code, rate_str, pitch_str))
            st.audio("output.mp3", format="audio/mp3", autoplay=True)
            st.success("Playback Ready")
    else:
        st.warning("Please enter or paste Lao text first.")

st.markdown('</div>', unsafe_allow_html=True)

# Visual Gallery Cards Section (Featured Temple & Cultural Images)
st.markdown("""
    <div class="animated-section" style="margin-top: 3.5rem;">
        <div class="editorial-sub" style="font-size: 0.75rem;">Heritage & Atmosphere</div>
        <div style="font-family: 'Cormorant Garamond', serif; font-size: 2rem; text-align: center; margin-bottom: 1rem;">
            THE SPIRIT OF LAOS
        </div>
    </div>
""", unsafe_allow_html=True)

img_col1, img_col2, img_col3 = st.columns(3)

with img_col1:
    st.markdown("""
        <div class="gallery-card" style="background-image: url('https://images.unsplash.com/photo-1528181304800-259b08848526?q=80&w=800&auto=format&fit=crop');">
            <span class="card-caption">Morning Alms · Luang Prabang</span>
        </div>
    """, unsafe_allow_html=True)

with img_col2:
    st.markdown("""
        <div class="gallery-card" style="background-image: url('https://images.unsplash.com/photo-1583417319070-4a69db38a482?q=80&w=800&auto=format&fit=crop');">
            <span class="card-caption">Wat Xieng Thong</span>
        </div>
    """, unsafe_allow_html=True)

with img_col3:
    st.markdown("""
        <div class="gallery-card" style="background-image: url('https://images.unsplash.com/photo-1508009603885-50cf7c579365?q=80&w=800&auto=format&fit=crop');">
            <span class="card-caption">Mekong River Sanctuary</span>
        </div>
    """, unsafe_allow_html=True)
