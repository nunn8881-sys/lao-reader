import asyncio
import edge_tts
import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Lao Text-to-Speech | Neural Reader",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

HERO_IMAGE = "https://images.unsplash.com/photo-1540611025311-01df3cef54b5?q=80&w=2000&auto=format&fit=crop"

# Custom Editorial CSS
st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Cinzel:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500&display=swap');

    /* Global Full-Screen Background */
    .stApp {
        background:
            linear-gradient(to bottom, rgba(12, 16, 12, 0.55), rgba(8, 10, 8, 0.88)),
            url('__HERO_IMAGE__');
        background-size: cover !important;
        background-position: center center !important;
        background-attachment: fixed !important;
        color: #f7f4ef;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Drifting mist / gold light-leak ambience */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        background:
            radial-gradient(circle at 15% 20%, rgba(226, 192, 141, 0.16), transparent 45%),
            radial-gradient(circle at 85% 75%, rgba(196, 148, 84, 0.14), transparent 50%),
            radial-gradient(ellipse at 50% 100%, rgba(20, 40, 30, 0.5), transparent 60%);
        animation: mistDrift 22s ease-in-out infinite alternate;
    }

    @keyframes mistDrift {
        0%   { opacity: 0.75; transform: translateY(0px) scale(1); }
        100% { opacity: 1;    transform: translateY(-18px) scale(1.04); }
    }

    /* Hide standard Streamlit header & footer */
    header, footer, #MainMenu {
        visibility: hidden;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
        max-width: 820px !important;
        position: relative;
        z-index: 1;
    }

    /* ---------------- Hero Frame (parallax photograph) ---------------- */
    .hero-frame {
        position: relative;
        height: 58vh;
        min-height: 380px;
        border-radius: 26px;
        overflow: hidden;
        margin: 0.5rem 0 2.6rem 0;
        box-shadow: 0 30px 70px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(226, 192, 141, 0.28);
    }

    .parallax-img {
        position: absolute;
        top: -18%;
        left: -6%;
        width: 112%;
        height: 140%;
        background-image: url('__HERO_IMAGE__');
        background-size: cover;
        background-position: center 35%;
        will-change: transform;
        transition: transform 0.05s linear;
    }

    .hero-frame::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(
            to bottom,
            rgba(15, 12, 8, 0.15) 0%,
            rgba(12, 9, 6, 0.35) 55%,
            rgba(8, 6, 4, 0.85) 100%
        );
    }

    .hero-copy {
        position: absolute;
        left: 0; right: 0; bottom: 1.9rem;
        z-index: 2;
        text-align: center;
        padding: 0 1.5rem;
    }

    /* Editorial Header Typography */
    .editorial-sub {
        font-family: 'Cinzel', serif;
        letter-spacing: 0.45em;
        text-transform: uppercase;
        font-size: 0.8rem;
        color: #e2c08d;
        text-align: center;
        margin-bottom: 0.7rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }

    .editorial-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.6rem;
        font-weight: 300;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #ffffff;
        text-align: center;
        text-shadow: 0 4px 25px rgba(0, 0, 0, 0.75);
        margin-bottom: 0.4rem;
        line-height: 1.08;
    }

    .editorial-tagline {
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        font-size: 1.25rem;
        color: #ecdfc8;
        text-align: center;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }

    .editorial-rule {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.9rem;
        margin: 0 auto 1.6rem auto;
        max-width: 220px;
    }
    .editorial-rule .line {
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(226,192,141,0.65), transparent);
    }
    .editorial-rule .dot {
        width: 5px; height: 5px;
        border-radius: 50%;
        background: #e2c08d;
        box-shadow: 0 0 8px rgba(226,192,141,0.8);
    }

    /* Scroll cue */
    .scroll-cue {
        position: absolute;
        bottom: -0.4rem; left: 50%;
        transform: translateX(-50%);
        z-index: 2;
        color: #e2c08d;
        font-size: 1.3rem;
        opacity: 0.85;
        animation: bounce 2.2s ease-in-out infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translate(-50%, 0); opacity: 0.5; }
        50%      { transform: translate(-50%, 8px); opacity: 1; }
    }

    /* ---------------- Scroll-reveal for control groups ---------------- */
    .reveal {
        opacity: 0;
        transform: translateY(32px);
        transition: opacity 0.9s cubic-bezier(0.16,1,0.3,1), transform 0.9s cubic-bezier(0.16,1,0.3,1);
    }
    .reveal.in-view {
        opacity: 1;
        transform: translateY(0);
    }

    /* Journal card that holds the controls */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(10, 12, 9, 0.42) !important;
        backdrop-filter: blur(18px) !important;
        -webkit-backdrop-filter: blur(18px) !important;
        border: 1px solid rgba(226, 192, 141, 0.28) !important;
        border-radius: 22px !important;
        padding: 0.6rem 0.4rem !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.45);
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

    /* Select Dropdown Styling */
    div[data-baseweb="select"], div[data-baseweb="select"] * {
        background-color: rgba(0, 0, 0, 0.35) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(226, 192, 141, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }

    /* COMPLETELY REMOVE BACKGROUND FROM TEXTAREA & PARENT CONTAINERS */
    div[data-testid="stTextArea"],
    div[data-testid="stTextArea"] *,
    div[data-baseweb="textarea"],
    div[data-baseweb="textarea"] * {
        background: transparent !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }

    /* ADD ELEGANT TRANSPARENT BORDER DIRECTLY ON TEXTAREA */
    div[data-baseweb="textarea"] {
        border: 1px solid rgba(226, 192, 141, 0.4) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(4px) !important;
        -webkit-backdrop-filter: blur(4px) !important;
        padding: 0.5rem !important;
    }

    /* TEXT INPUT STYLE */
    textarea[data-testid="stTextArea"],
    .stTextArea textarea {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.15rem !important;
        line-height: 1.75 !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.7);
    }

    textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
        -webkit-text-fill-color: rgba(255, 255, 255, 0.6) !important;
    }

    label p {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
        font-size: 0.78rem !important;
        color: #e2c08d !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.8);
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

    .footer-quote {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        color: #d4c5b3;
        font-size: 1.15rem;
    }

    .footer-mark {
        text-align: center;
        font-family: 'Cinzel', serif;
        letter-spacing: 0.35em;
        text-transform: uppercase;
        font-size: 0.7rem;
        color: rgba(226, 192, 141, 0.6);
        margin-top: 0.8rem;
    }

    /* Audio Player Custom Styling */
    audio {
        width: 100% !important;
        margin-top: 1.5rem !important;
        border-radius: 30px !important;
        filter: invert(0.9) sepia(0.3) saturate(1.8) hue-rotate(340deg);
    }

    /* Gold custom scrollbar */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: rgba(0,0,0,0.3); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #d4a76a, #a3773f);
        border-radius: 10px;
    }
    </style>
""".replace("__HERO_IMAGE__", HERO_IMAGE), unsafe_allow_html=True)

# Hero photograph with parallax + editorial masthead overlaid
st.markdown(f"""
    <div class="hero-frame">
        <div class="parallax-img" data-speed="0.35"></div>
        <div class="hero-copy">
            <div class="editorial-sub">Neural Voice Synthesis</div>
            <div class="editorial-title">Lao Text to Speech</div>
            <div class="editorial-tagline">— Transform Lao script into natural, resonant voice —</div>
        </div>
        <div class="scroll-cue">⌄</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="editorial-rule"><div class="line"></div><div class="dot"></div><div class="line"></div></div>
""", unsafe_allow_html=True)

# Journal card holding the controls
with st.container(border=True):
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

    # Script Input Area
    lao_text = st.text_area(
        "Lao Script Passage",
        height=220,
        placeholder="ວາງຂໍ້ຄວາມພາສາລາວຢູ່ທີ່ນີ້..."
    )

    # Async Audio Generation
    async def generate_audio(text, voice_name, rate, pitch_val):
        communicate = edge_tts.Communicate(text, voice_name, rate=rate, pitch=pitch_val)
        await communicate.save("output.mp3")

    # Trigger Action
    if st.button("▶ Read Aloud"):
        if lao_text.strip():
            with st.spinner("Synthesizing natural Lao speech..."):
                asyncio.run(generate_audio(lao_text, voice_code, rate_str, pitch_str))
                st.audio("output.mp3", format="audio/mp3", autoplay=True)
                st.success("Playback Ready")
        else:
            st.warning("Please paste Lao script first.")

# Footer
st.markdown("""
    <div class="gold-divider"></div>
    <div class="footer-quote">"Resonant Lao neural speech, crafted for long-form listening."</div>
    <div class="footer-mark">Jet Set Journal · Luang Prabang</div>
""", unsafe_allow_html=True)

# Scroll-driven parallax + fade-in reveal (reaches into the parent Streamlit
# document since the component iframe shares the same origin).
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
        'div[data-testid="stVerticalBlockBorderWrapper"]',
        'div[data-testid="stSelectbox"]',
        'div[data-testid="stSlider"]',
        'div[data-testid="stTextArea"]',
        'div[data-testid="stButton"]',
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

    function onScroll() {
        const y = window.parent.scrollY || 0;
        doc.querySelectorAll('.parallax-img').forEach((el) => {
            const speed = parseFloat(el.dataset.speed || '0.3');
            el.style.transform = 'translate3d(0,' + (y * speed) + 'px,0)';
        });
    }

    window.parent.addEventListener('scroll', onScroll, { passive: true });
    const observer = new MutationObserver(observeNewReveals);
    observer.observe(doc.body, { childList: true, subtree: true });

    observeNewReveals();
    onScroll();
})();
</script>
""", height=0)
