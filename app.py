import asyncio
import edge_tts
import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Lao Text-to-Speech",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------------
# Global styling — Apple × Notion: white space, restrained type, one accent.
# ---------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg: #ffffff;
        --bg-soft: #f5f5f7;
        --text: #1d1d1f;
        --text-soft: #6e6e73;
        --border: rgba(0, 0, 0, 0.08);
        --accent: #0071e3;
        --accent-soft: rgba(0, 113, 227, 0.10);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 8%, rgba(0, 113, 227, 0.07), transparent 38%),
            radial-gradient(circle at 88% 18%, rgba(191, 90, 242, 0.06), transparent 42%),
            var(--bg) !important;
        color: var(--text);
    }

    header, footer, #MainMenu { visibility: hidden; }

    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 6rem !important;
        max-width: 760px !important;
    }

    /* ---------------- Hero ---------------- */
    .eyebrow {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-soft);
        margin-bottom: 1.1rem;
    }
    .eyebrow .dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: var(--accent);
    }

    .hero-title {
        font-size: clamp(2.6rem, 6vw, 4.2rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.05;
        text-align: center;
        color: var(--text);
        margin-bottom: 1.1rem;
    }
    .hero-title .accent { color: var(--accent); }

    .hero-sub {
        font-size: 1.15rem;
        font-weight: 400;
        color: var(--text-soft);
        text-align: center;
        max-width: 520px;
        margin: 0 auto 3.2rem auto;
        line-height: 1.6;
    }

    /* ---------------- Scroll reveal ---------------- */
    .reveal {
        opacity: 0;
        transform: translateY(22px) scale(0.98);
        transition: opacity 0.7s cubic-bezier(0.16,1,0.3,1), transform 0.7s cubic-bezier(0.16,1,0.3,1);
    }
    .reveal.in-view { opacity: 1; transform: translateY(0) scale(1); }

    /* Stagger the three feature columns */
    div[data-testid="stHorizontalBlock"]:has(.feature-card) > div:nth-of-type(1) .reveal { transition-delay: 0s; }
    div[data-testid="stHorizontalBlock"]:has(.feature-card) > div:nth-of-type(2) .reveal { transition-delay: 0.08s; }
    div[data-testid="stHorizontalBlock"]:has(.feature-card) > div:nth-of-type(3) .reveal { transition-delay: 0.16s; }

    /* ---------------- Feature cards (Notion-style) ---------------- */
    .feature-card {
        background: var(--bg);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.3rem 1.2rem;
        height: 100%;
        transition: border-color 0.25s ease, transform 0.25s ease;
    }
    .feature-card:hover {
        border-color: rgba(0, 113, 227, 0.35);
        transform: translateY(-2px);
    }
    .feature-icon { font-size: 1.3rem; margin-bottom: 0.6rem; }
    .feature-title {
        font-size: 0.92rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 0.3rem;
    }
    .feature-desc {
        font-size: 0.84rem;
        color: var(--text-soft);
        line-height: 1.5;
    }

    /* ---------------- Main control card ---------------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        padding: 0.8rem 0.6rem !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 12px 32px rgba(0,0,0,0.05) !important;
        margin-top: 0.5rem;
    }

    .section-label {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: var(--text-soft);
        margin: 0.4rem 0 1.2rem 0;
    }

    label p {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: 0 !important;
        text-transform: none !important;
        font-size: 0.86rem !important;
        color: var(--text-soft) !important;
    }

    /* Select */
    div[data-baseweb="select"] > div {
        background-color: var(--bg-soft) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
    }
    div[data-baseweb="select"] * { color: var(--text) !important; }

    /* Sliders */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #ffffff !important;
        border: 2px solid var(--accent) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.25) !important;
    }
    div[data-baseweb="slider"] > div > div > div {
        background: var(--accent) !important;
    }
    div[data-testid="stTickBar"], div[data-baseweb="slider"] div[data-testid="stSliderTickBar"] {
        background-color: var(--border) !important;
    }
    div[data-baseweb="slider"] div { color: var(--text-soft) !important; }

    /* Text area */
    div[data-testid="stTextArea"] textarea,
    .stTextArea textarea {
        background-color: var(--bg-soft) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.02rem !important;
        line-height: 1.7 !important;
        padding: 0.9rem !important;
    }
    textarea::placeholder {
        color: rgba(29, 29, 31, 0.35) !important;
        -webkit-text-fill-color: rgba(29, 29, 31, 0.35) !important;
    }

    /* Button — Apple pill CTA */
    .stButton > button {
        width: 100%;
        background: var(--text) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0 !important;
        text-transform: none !important;
        font-size: 1rem !important;
        padding: 0.85rem 2rem !important;
        border-radius: 999px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15) !important;
        transition: all 0.25s ease !important;
        margin-top: 1.4rem !important;
    }
    .stButton > button:hover {
        background: var(--accent) !important;
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(0, 113, 227, 0.3) !important;
    }

    /* Audio player */
    audio {
        width: 100% !important;
        margin-top: 1.4rem !important;
        border-radius: 14px !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
    }

    /* Footer */
    .footer-row {
        border-top: 1px solid var(--border);
        margin-top: 3.5rem;
        padding-top: 1.6rem;
        text-align: center;
        color: var(--text-soft);
        font-size: 0.82rem;
    }

    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown("""
    <div class="eyebrow"><span class="dot"></span>Neural Text-to-Speech</div>
    <div class="hero-title">Lao, spoken<br><span class="accent">naturally.</span></div>
    <div class="hero-sub">
        Paste Lao script and hear it read aloud in a clear, natural neural voice —
        tune the speed and pitch until it sounds just right.
    </div>
""", unsafe_allow_html=True)

# Feature strip
feat_cols = st.columns(3)
features = [
    ("🗣️", "Two neural voices", "A warm female voice and a grounded male voice, both native to Lao."),
    ("🎚️", "Fine-tuned control", "Dial in speech speed and pitch to match the tone you need."),
    ("⚡", "Instant playback", "Generates and plays back your passage as an MP3 in seconds."),
]
for col, (icon, title, desc) in zip(feat_cols, features):
    with col:
        st.markdown(f"""
            <div class="reveal feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height: 2.6rem'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Control card
# ---------------------------------------------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-label">Configure</div>', unsafe_allow_html=True)

    voice = st.selectbox(
        "Voice",
        ["lo-LA-KeomanyNeural (Female)", "lo-LA-ChanthavongNeural (Male)"]
    )
    voice_code = voice.split(" ")[0]

    col_speed, col_pitch = st.columns(2)

    with col_speed:
        speed = st.slider("Speed", min_value=0.6, max_value=1.4, value=1.0, step=0.05)
        rate_str = f"{int((speed - 1.0) * 100):+d}%"

    with col_pitch:
        pitch = st.slider("Pitch", min_value=-20, max_value=20, value=0, step=5)
        pitch_str = f"{pitch:+d}Hz"

    lao_text = st.text_area(
        "Lao script",
        height=200,
        placeholder="ວາງຂໍ້ຄວາມພາສາລາວຢູ່ທີ່ນີ້..."
    )

    async def generate_audio(text, voice_name, rate, pitch_val):
        communicate = edge_tts.Communicate(text, voice_name, rate=rate, pitch=pitch_val)
        await communicate.save("output.mp3")

    if st.button("Generate speech"):
        if lao_text.strip():
            with st.spinner("Synthesizing speech..."):
                asyncio.run(generate_audio(lao_text, voice_code, rate_str, pitch_str))
                st.audio("output.mp3", format="audio/mp3", autoplay=True)
                st.success("Playback ready")
        else:
            st.warning("Paste some Lao script first.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("""
    <div class="footer-row">Built for clear, natural Lao listening.</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Scroll-driven reveal (reaches into the parent Streamlit document, since the
# component iframe shares the same origin — plain <script> tags in
# st.markdown never execute).
# ---------------------------------------------------------------------------
components.html("""
<script>
(function() {
    const doc = window.parent.document;
    if (doc.__laoReaderInit) { return; }
    doc.__laoReaderInit = true;

    const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
            }
        });
    }, { threshold: 0.12 });

    const revealSelectors = [
        '.feature-card',
        'div[data-testid="stVerticalBlockBorderWrapper"]',
        'div[data-testid="stAudio"]',
        'div[data-testid="stAlert"]'
    ].join(', ');

    function observeNewReveals() {
        doc.querySelectorAll(revealSelectors).forEach((el) => {
            if (!el.classList.contains('reveal')) {
                el.classList.add('reveal');
                io.observe(el);
            }
        });
    }

    const observer = new MutationObserver(observeNewReveals);
    observer.observe(doc.body, { childList: true, subtree: true });
    observeNewReveals();
})();
</script>
""", height=0)
