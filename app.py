import asyncio
import base64
import os

import edge_tts
import streamlit as st

st.set_page_config(page_title="Lao Reader", page_icon="🔊", layout="centered")

ASSETS_DIR = "."


def raw(html: str) -> str:
    """Strip leading whitespace from every line so Streamlit's markdown
    parser doesn't mistake indented HTML/CSS for a code block."""
    return "\n".join(line.lstrip() for line in html.strip("\n").splitlines())


def image_to_data_uri(filename: str) -> str | None:
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{b64}"


hero_bg = image_to_data_uri("hero_river.jpg")
temple_img = image_to_data_uri("hero_temple.jpg")
monks_img = image_to_data_uri("hero_monks.jpg")

missing = [
    name
    for name, val in [
        ("hero_river.jpg", hero_bg),
        ("hero_temple.jpg", temple_img),
        ("hero_monks.jpg", monks_img),
    ]
    if val is None
]

# ----------------------------------------------------------------------
# Base styling (fonts, cards, inputs, buttons)
# ----------------------------------------------------------------------
st.markdown(
    raw(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .stApp { background: #FBF4E8; }
        #MainMenu, footer, header { visibility: hidden; }
        .block-container {
            max-width: 560px;
            padding-top: 0 !important;
            padding-bottom: 3rem;
        }

        .reveal {
            opacity: 0;
            transform: translateY(24px);
            transition: opacity 0.7s ease, transform 0.7s ease;
        }
        .reveal.visible { opacity: 1; transform: translateY(0); }

        .section-label {
            font-size: 0.72rem;
            font-weight: 600;
            color: #8A6D4A;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-top: 1.3rem;
            margin-bottom: 0.4rem;
        }

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

        /* Hero */
        .hero {
            position: relative;
            overflow: hidden;
            margin: 0 -1rem 2rem -1rem;
            height: 280px;
            border-radius: 0 0 26px 26px;
        }
        .hero-bg {
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center 35%;
            transform: scale(1.08);
            will-change: transform;
        }
        .hero-scrim {
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(30,20,10,0.15) 0%, rgba(30,20,10,0.05) 40%, rgba(30,20,10,0.55) 100%);
        }
        .hero-content {
            position: relative;
            z-index: 2;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            padding-bottom: 1.8rem;
            text-align: center;
        }
        .hero-eyebrow {
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #F6E6C6;
            margin-bottom: 0.5rem;
        }
        .hero-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.4rem;
            font-weight: 600;
            color: #FFFCF5;
            margin: 0;
            line-height: 1.1;
        }
        .hero-sub {
            font-size: 0.82rem;
            font-weight: 500;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #E9D2A0;
            margin-top: 0.4rem;
        }
        .hero-sub::before, .hero-sub::after { content: "—"; margin: 0 10px; opacity: 0.7; }

        /* Scroll photo panels */
        .photo-panel {
            position: relative;
            margin: 1.6rem 0;
            border-radius: 18px;
            overflow: hidden;
            height: 190px;
        }
        .photo-panel img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
        .photo-caption {
            position: absolute;
            left: 14px;
            bottom: 12px;
            z-index: 2;
            color: #FFFCF5;
            font-size: 0.78rem;
            font-weight: 500;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .photo-scrim {
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(20,15,5,0) 55%, rgba(20,15,5,0.55) 100%);
        }
        </style>
        """
    ),
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Hero banner (real photo background)
# ----------------------------------------------------------------------
if hero_bg:
    st.markdown(
        raw(
            f"""
            <div class="hero">
                <div class="hero-bg" id="heroBg" style="background-image:url('{hero_bg}');"></div>
                <div class="hero-scrim"></div>
                <div class="hero-content">
                    <div class="hero-eyebrow">Jet Set Journal · Text to Speech</div>
                    <div class="hero-title">Lao Reader</div>
                    <div class="hero-sub">Laos</div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        raw(
            """
            <div class="hero" style="background:linear-gradient(180deg,#F6D9A8,#E3A868);">
                <div class="hero-content">
                    <div class="hero-eyebrow">Jet Set Journal · Text to Speech</div>
                    <div class="hero-title">Lao Reader</div>
                    <div class="hero-sub">Laos</div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

if missing:
    st.info(
        "Add these files to an `assets/` folder next to app.py to enable the "
        "photo hero and panels: " + ", ".join(missing)
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
# Scroll photo panel 1
# ----------------------------------------------------------------------
if temple_img:
    st.markdown(
        raw(
            f"""
            <div class="photo-panel reveal">
                <img src="{temple_img}" alt="Misty temple roofline in Luang Prabang">
                <div class="photo-scrim"></div>
                <div class="photo-caption">Luang Prabang, Laos</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

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
# Scroll photo panel 2
# ----------------------------------------------------------------------
if monks_img:
    st.markdown(
        raw(
            f"""
            <div class="photo-panel reveal">
                <img src="{monks_img}" alt="Morning alms procession in Luang Prabang">
                <div class="photo-scrim"></div>
                <div class="photo-caption">Morning alms, Luang Prabang</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

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
# Scroll-reveal + hero parallax script
# ----------------------------------------------------------------------
st.markdown(
    raw(
        """
        <script>
        function initScrollFx() {
            const doc = window.parent.document;

            const items = doc.querySelectorAll(
                '.section-label, .stTextArea, .stSlider, .stSelectbox, .stButton, .stDownloadButton, .photo-panel'
            );
            items.forEach(el => el.classList.add('reveal'));

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) entry.target.classList.add('visible');
                });
            }, { threshold: 0.15 });
            items.forEach(el => observer.observe(el));

            const scrollContainer = doc.querySelector('section.main') || doc;
            const heroBg = doc.getElementById('heroBg');
            if (heroBg) {
                const onScroll = () => {
                    const y = (scrollContainer.scrollTop || window.parent.scrollY || 0);
                    heroBg.style.transform = `scale(1.08) translateY(${Math.min(y * 0.25, 40)}px)`;
                };
                scrollContainer.addEventListener('scroll', onScroll);
                window.parent.addEventListener('scroll', onScroll);
            }
        }
        setTimeout(initScrollFx, 300);
        </script>
        """
    ),
    unsafe_allow_html=True,
)
