import asyncio
import base64
import edge_tts
import streamlit as st

st.set_page_config(page_title="Lao Reader", page_icon="🔊", layout="centered")

# ----------------------------------------------------------------------
# Custom CSS — iOS-HIG-inspired, mobile-first, clean card aesthetic
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* App-wide font + background */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text",
                         "Segoe UI", Roboto, sans-serif;
        }

        .stApp {
            background: linear-gradient(180deg, #F2F2F7 0%, #FFFFFF 100%);
        }

        /* Hide default Streamlit chrome for a more "app-like" feel */
        #MainMenu, footer, header {visibility: hidden;}

        /* Center container width, add card padding on mobile */
        .block-container {
            max-width: 560px;
            padding-top: 2.2rem;
            padding-bottom: 3rem;
        }

        /* Title */
        h1 {
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
            color: #1C1C1E;
        }

        /* Card wrapper around the main controls */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #FFFFFF;
            border-radius: 18px;
            padding: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 8px 24px rgba(0,0,0,0.04);
        }

        /* Text area */
        .stTextArea textarea {
            border-radius: 14px !important;
            border: 1px solid #E5E5EA !important;
            font-size: 1rem !important;
            background: #F9F9FB !important;
        }
        .stTextArea textarea:focus {
            border-color: #007AFF !important;
            box-shadow: 0 0 0 3px rgba(0,122,255,0.15) !important;
        }

        /* Select box */
        div[data-baseweb="select"] > div {
            border-radius: 12px !important;
            border: 1px solid #E5E5EA !important;
        }

        /* Sliders — iOS blue accent */
        .stSlider [data-baseweb="slider"] div[role="slider"] {
            background-color: #007AFF !important;
            box-shadow: 0 2px 6px rgba(0,122,255,0.4) !important;
        }
        .stSlider [data-baseweb="slider"] > div > div {
            background: #007AFF !important;
        }

        /* Primary button — pill shaped, iOS blue */
        .stButton > button[kind="primary"] {
            background: #007AFF;
            border: none;
            border-radius: 14px;
            padding: 0.7rem 1rem;
            font-weight: 600;
            font-size: 1.05rem;
            width: 100%;
            transition: transform 0.05s ease-in-out;
        }
        .stButton > button[kind="primary"]:active {
            transform: scale(0.98);
        }

        /* Download button */
        .stDownloadButton > button {
            border-radius: 14px;
            border: 1px solid #007AFF;
            color: #007AFF;
            background: #FFFFFF;
            font-weight: 600;
            width: 100%;
        }

        /* Counter pill */
        .counter-pill {
            display: inline-block;
            background: #F2F2F7;
            color: #6E6E73;
            font-size: 0.82rem;
            padding: 4px 12px;
            border-radius: 999px;
            margin-top: -6px;
            margin-bottom: 10px;
        }

        /* Section labels */
        .section-label {
            font-size: 0.78rem;
            font-weight: 600;
            color: #8E8E93;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-top: 1.1rem;
            margin-bottom: 0.2rem;
        }

        audio {
            width: 100%;
            border-radius: 12px;
            margin-top: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔊 Lao Text-to-Speech")
st.caption("Paste Lao script below to listen to natural neural speech.")

# ----------------------------------------------------------------------
# Voice selection
# ----------------------------------------------------------------------
st.markdown('<div class="section-label">Voice</div>', unsafe_allow_html=True)
voice = st.selectbox(
    "Choose Voice:",
    ["lo-LA-KeomanyNeural (Female)", "lo-LA-ChanthavongNeural (Male)"],
    label_visibility="collapsed",
)
voice_code = voice.split(" ")[0]

# ----------------------------------------------------------------------
# Text input + live word/character counter
# ----------------------------------------------------------------------
st.markdown('<div class="section-label">Text</div>', unsafe_allow_html=True)
lao_text = st.text_area(
    "Lao Text:",
    height=220,
    placeholder="ວາງຂໍ້ຄວາມພາສາລາວທີ່ນີ້...",
    label_visibility="collapsed",
)

char_count = len(lao_text)
word_count = len(lao_text.split()) if lao_text.strip() else 0
st.markdown(
    f'<span class="counter-pill">✏️ {word_count} words · {char_count} characters</span>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Speed / Pitch / Volume controls
# ----------------------------------------------------------------------
st.markdown('<div class="section-label">Playback Settings</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    rate_pct = st.slider("Speed", min_value=-50, max_value=50, value=0, step=5, format="%d%%")
with col2:
    volume_pct = st.slider("Volume", min_value=-50, max_value=50, value=0, step=5, format="%d%%")

pitch_hz = st.slider("Pitch", min_value=-20, max_value=20, value=0, step=2, format="%dHz")

# edge-tts expects signed strings like "+10%", "-5%", "+0Hz"
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

# Persist audio + show player/download across reruns (e.g. slider tweaks)
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
