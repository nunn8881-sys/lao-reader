import asyncio
import edge_tts
import streamlit as st

st.set_page_config(page_title="Lao Reader", page_icon="🔊", layout="centered")

# ----------------------------------------------------------------------
# Custom CSS + decorative SVG artwork + scroll animations
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background: #FBF4E8;
        }

        #MainMenu, footer, header {visibility: hidden;}

        .block-container {
            max-width: 560px;
            padding-top: 0 !important;
            padding-bottom: 3rem;
        }

        /* ---- Hero: layered gradient sky + parallax silhouettes ---- */
        .hero {
            position: relative;
            overflow: hidden;
            margin: 0 -1rem 2rem -1rem;
            padding: 3.4rem 1.5rem 2.6rem 1.5rem;
            background: linear-gradient(180deg, #F8E0AE 0%, #F0C48A 45%, #E3A868 100%);
            border-radius: 0 0 26px 26px;
            text-align: center;
        }
        .hero-mist {
            position: absolute;
            left: -10%;
            width: 120%;
            height: 60px;
            background: linear-gradient(180deg, rgba(255,255,255,0.55), rgba(255,255,255,0));
            filter: blur(6px);
            animation: driftMist 14s ease-in-out infinite alternate;
            pointer-events: none;
        }
        .hero-mist.m1 { top: 10px; opacity: 0.7; }
        .hero-mist.m2 { top: 55px; opacity: 0.45; animation-duration: 18s; }
        @keyframes driftMist {
            0%   { transform: translateX(-4%); }
            100% { transform: translateX(4%); }
        }
        .hero-mountains {
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 100%;
            display: block;
            opacity: 0.9;
        }
        .hero-palm {
            position: absolute;
            width: 90px;
            opacity: 0.85;
        }
        .hero-palm.left  { top: 8px; left: -6px; transform: scaleX(-1); }
        .hero-palm.right { top: 4px; right: -10px; }

        .hero-content { position: relative; z-index: 2; }
        .hero-eyebrow {
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #6B4423;
            margin-bottom: 0.6rem;
        }
        .hero-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 600;
            color: #3B2A18;
            margin: 0;
            line-height: 1.15;
        }
        .hero-sub {
            font-size: 0.85rem;
            font-weight: 500;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #8A5A2E;
            margin-top: 0.5rem;
        }
        .hero-sub::before, .hero-sub::after { content: "—"; margin: 0 10px; opacity: 0.6; }

        /* ---- Scroll-reveal ---- */
        .reveal {
            opacity: 0;
            transform: translateY(24px);
            transition: opacity 0.7s ease, transform 0.7s ease;
        }
        .reveal.visible {
            opacity: 1;
            transform: translateY(0);
        }

        /* ---- Section labels ---- */
        .section-label {
            font-size: 0.72rem;
            font-weight: 600;
            color: #8A6D4A;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-top: 1.3rem;
            margin-bottom: 0.4rem;
        }

        /* ---- Card wrapper ---- */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #FFFDF8;
            border-radius: 16px;
            border: 1px solid #EAD9B8;
            padding: 4px;
        }

        .stTextArea textarea {
            border-radius: 12px !important;
            border: 1px solid #E3D2AC !important;
            background: #FFFCF5 !important;
            font-size: 1rem !important;
            color: #3B2A18 !important;
        }
        .stTextArea textarea:focus {
            border-color: #C9862B !important;
            box-shadow: 0 0 0 3px rgba(201,134,43,0.15) !important;
        }
        .stTextArea textarea::placeholder { color: #B79A6E !important; }

        div[data-baseweb="select"] > div {
            border-radius: 10px !important;
            border: 1px solid #E3D2AC !important;
            background: #FFFCF5 !important;
        }

        .stSlider [data-baseweb="slider"] div[role="slider"] {
            background-color: #C9862B !important;
            box-shadow: 0 2px 6px rgba(201,134,43,0.4) !important;
        }
        .stSlider [data-baseweb="slider"] > div > div { background: #C9862B !important; }

        .counter-pill {
            display: inline-block;
            background: #F3E4C4;
            color: #7A5A2E;
            font-size: 0.8rem;
            font-weight: 500;
            padding: 4px 13px;
            border-radius: 999px;
            margin-top: -4px;
            margin-bottom: 8px;
        }

        .stButton > button[kind="primary"] {
            background: #24422E;
            border: none;
            border-radius: 12px;
            padding: 0.7rem 1rem;
            font-weight: 600;
            font-size: 1.02rem;
            width: 100%;
            letter-spacing: 0.02em;
        }
        .stButton > button[kind="primary"]:hover { background: #1B3322; }
        .stButton > button[kind="primary"]:active { transform: scale(0.98); }

        .stDownloadButton > button {
            border-radius: 12px;
            border: 1px solid #C9862B;
            color: #8A5A1E;
            background: #FFFCF5;
            font-weight: 600;
            width: 100%;
        }
        .stDownloadButton > button:hover { background: #FBF0DC; }

        audio { width: 100%; border-radius: 10px; margin-top: 0.8rem; }

        /* Small decorative divider between sections */
        .leaf-divider {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 1.6rem 0 0.4rem 0;
            opacity: 0.6;
        }
    </style>

    <div class="hero">
        <div class="hero-mist m1"></div>
        <div class="hero-mist m2"></div>

        <svg class="hero-palm left" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <g fill="#4A6B3E">
                <path d="M50 90 C 48 60, 45 40, 30 15 C 42 25, 48 40, 50 55 C 52 40, 58 25, 70 15 C 55 40, 52 60, 50 90 Z"/>
                <path d="M50 55 C 40 45, 20 40, 5 45 C 22 48, 38 55, 50 62 Z"/>
                <path d="M50 55 C 60 45, 80 40, 95 45 C 78 48, 62 55, 50 62 Z"/>
                <path d="M50 40 C 42 28, 25 20, 8 20 C 25 26, 40 34, 50 45 Z"/>
                <path d="M50 40 C 58 28, 75 20, 92 20 C 75 26, 60 34, 50 45 Z"/>
            </g>
        </svg>
        <svg class="hero-palm right" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <g fill="#3E5C33">
                <path d="M50 90 C 48 60, 45 40, 30 15 C 42 25, 48 40, 50 55 C 52 40, 58 25, 70 15 C 55 40, 52 60, 50 90 Z"/>
                <path d="M50 55 C 40 45, 20 40, 5 45 C 22 48, 38 55, 50 62 Z"/>
                <path d="M50 55 C 60 45, 80 40, 95 45 C 78 48, 62 55, 50 62 Z"/>
                <path d="M50 40 C 42 28, 25 20, 8 20 C 25 26, 40 34, 50 45 Z"/>
                <path d="M50 40 C 58 28, 75 20, 92 20 C 75 26, 60 34, 50 45 Z"/>
            </g>
        </svg>

        <div class="hero-content">
            <div class="hero-eyebrow">Jet Set Journal · Text to Speech</div>
            <div class="hero-title">Lao Reader</div>
            <div class="hero-sub">Laos</div>
        </div>

        <svg class="hero-mountains" viewBox="0 0 500 90" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0,90 L0,55 Q60,20 120,45 T240,35 Q300,15 360,40 T500,30 L500,90 Z" fill="#7A8B6A" opacity="0.55"/>
            <path d="M0,90 L0,68 Q80,42 160,60 T320,55 Q400,38 500,58 L500,90 Z" fill="#4E5F42" opacity="0.75"/>
            <path d="M235,42 L245,20 L255,42 Z" fill="#D9A736"/>
        </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Paste Lao script below to listen to natural neural speech.")

# ----------------------------------------------------------------------
# Voice selection
# ----------------------------------------------------------------------
st.markdown('<div class="section-label reveal">Voice</div>', unsafe_allow_html=True)
voice = st.selectbox(
    "Choose Voice:",
    ["lo-LA-KeomanyNeural (Female)", "lo-LA-ChanthavongNeural (Male)"],
    label_visibility="collapsed",
)
voice_code = voice.split(" ")[0]

# ----------------------------------------------------------------------
# Text input + live word/character counter
# ----------------------------------------------------------------------
st.markdown('<div class="section-label reveal">Text</div>', unsafe_allow_html=True)
lao_text = st.text_area(
    "Lao Text:",
    height=220,
    placeholder="ວາງຂໍ້ຄວາມພາສາລາວທີ່ນີ້...",
    label_visibility="collapsed",
)

char_count = len(lao_text)
word_count = len(lao_text.split()) if lao_text.strip() else 0
st.markdown(
    f'<span class="counter-pill">✏ {word_count} words · {char_count} characters</span>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Speed / Pitch / Volume controls
# ----------------------------------------------------------------------
st.markdown('<div class="section-label reveal">Playback settings</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    rate_pct = st.slider("Speed", min_value=-50, max_value=50, value=0, step=5, format="%d%%")
with col2:
    volume_pct = st.slider("Volume", min_value=-50, max_value=50, value=0, step=5, format="%d%%")

pitch_hz = st.slider("Pitch", min_value=-20, max_value=20, value=0, step=2, format="%dHz")

rate_str = f"{'+' if rate_pct >= 0 else ''}{rate_pct}%"
volume_str = f"{'+' if volume_pct >= 0 else ''}{volume_pct}%"
pitch_str = f"{'+' if pitch_hz >= 0 else ''}{pitch_hz}Hz"

# ----------------------------------------------------------------------
# Generate audio
# ----------------------------------------------------------------------
async def generate_audio(text, voice_name, rate, volume, pitch, out_path):
    communicate = edge_tts.Communicate(
        text,
        voice_name,
        rate=rate,
        volume=volume,
        pitch=pitch,
    )
    await communicate.save(out_path)


st.markdown("<br>", unsafe_allow_html=True)

if st.button("▶  Listen in Lao", type="primary"):
    if lao_text.strip():
        with st.spinner("Generating natural Lao speech..."):
            output_path = "output.mp3"
            asyncio.run(
                generate_audio(
                    lao_text, voice_code, rate_str, volume_str, pitch_str, output_path
                )
            )
            st.session_state["audio_path"] = output_path
        st.success("Ready!")
    else:
        st.warning("Please paste some Lao text first!")

if "audio_path" in st.session_state:
    with open(st.session_state["audio_path"], "rb") as f:
        audio_bytes = f.read()

    st.audio(audio_bytes, format="audio/mp3", autoplay=True)

    st.download_button(
        label="⬇  Download MP3",
        data=audio_bytes,
        file_name="lao_speech.mp3",
        mime="audio/mp3",
    )

# ----------------------------------------------------------------------
# Scroll-reveal script — fades/slides sections in as you scroll past them
# ----------------------------------------------------------------------
st.markdown(
    """
    <script>
    function initReveal() {
        const doc = window.parent.document;
        const items = doc.querySelectorAll('.section-label, .stTextArea, .stSlider, .stSelectbox, .stButton, .stDownloadButton');
        items.forEach(el => el.classList.add('reveal'));

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.15 });

        items.forEach(el => observer.observe(el));
    }
    setTimeout(initReveal, 300);
    </script>
    """,
    unsafe_allow_html=True,
)
