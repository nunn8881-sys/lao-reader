import asyncio
import edge_tts
import streamlit as st

st.set_page_config(page_title="Lao Reader", page_icon="🔊", layout="centered")

st.title("🔊 Lao Text-to-Speech")
st.write("Paste Lao script below to listen to natural neural speech.")

voice = st.selectbox(
    "Choose Voice:",
    ["lo-LA-KeomanyNeural (Female)", "lo-LA-ChanthavongNeural (Male)"]
)
voice_code = voice.split(" ")[0]

lao_text = st.text_area(
    "Lao Text:",
    height=220,
    placeholder="ວາງໂຄດ ຫຼື ຂໍ້ຄວາມภาษาลาວທີ່ນີ້..."
)

async def generate_audio(text, voice_name):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save("output.mp3")

if st.button("▶ Listen in Lao", type="primary"):
    if lao_text.strip():
        with st.spinner("Generating natural Lao speech..."):
            asyncio.run(generate_audio(lao_text, voice_code))
            st.audio("output.mp3", format="audio/mp3", autoplay=True)
            st.success("Ready!")
    else:
        st.warning("Please paste some Lao text first!")
