import json, streamlit as st
from components.theme import apply, hero
from components.animations import floating_hearts, confetti
from utils.dates import love_duration, next_anniversary
from utils.storage import init
init(); apply(); floating_hearts()
cfg=json.load(open("couple.json"))
st.set_page_config(page_title="ForeverVerse — Our Infinite Love Story",page_icon="❤️",layout="wide")
hero(cfg["welcome"],cfg["name1"],cfg["name2"],cfg["intro"])
if st.button("💗 Enter Our Love Story",use_container_width=True):
    confetti(); st.switch_page("pages/1_Our_Story.py")
st.markdown("## ⏳ Live Love Counter")
d=love_duration(cfg["relationship_start"])
c1,c2,c3,c4=st.columns(4)
c1.metric("Years",d["years"]);c2.metric("Months",d["months"]);c3.metric("Days",d["days"]);c4.metric("Total days",d["total_days"])
@st.fragment(run_every=1)
def tick():
    from datetime import datetime
    s=datetime.strptime(cfg["relationship_start"],"%Y-%m-%d")
    secs=int((datetime.now()-s).total_seconds())
    st.caption(f"❤️ {secs:,} seconds of us — updating live")
tick()
st.markdown("## 📅 Anniversary Countdown")
nx=next_anniversary(cfg["anniversary"])
st.markdown(f"<div class='glass'><h3>{nx['days_left']} days</h3><p>until {nx['date']} — our next anniversary</p><p style='opacity:.6;font-size:13px'>Feb 29 policy: celebrated Feb 28 in non-leap years.</p></div>",unsafe_allow_html=True)
st.markdown("### 🎵 Music")
up=st.file_uploader("Upload a song (mp3/wav)",type=["mp3","wav"])
if up: st.audio(up)
st.caption("Autoplay is not promised — press play after uploading.")
st.markdown("---")
st.markdown(f"<div class='glass' style='text-align:center'><h2 class='grad'>{cfg['finale']} ❤️</h2></div>",unsafe_allow_html=True)
if st.button("🎆 Celebrate"): confetti()
