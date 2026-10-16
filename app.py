import json, os, sqlite3, time
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
DB_PATH = os.path.join(BASE, "foreverus.db")

def load_config():
    with open(CONFIG_PATH) as f: return json.load(f)

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute("CREATE TABLE IF NOT EXISTS memories(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,date TEXT,description TEXT,image TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS letters(id INTEGER PRIMARY KEY AUTOINCREMENT,content TEXT,created_at TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,message TEXT,created_at TEXT)")
    cur = db.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    if cur == 0:
        for t in load_config().get("timeline", []):
            db.execute("INSERT INTO memories(title,date,description,image) VALUES(?,?,?,?)",(t["title"],t["date"],t["description"],t.get("image","")))
    db.commit(); db.close()

def q(sql, args=(), one=False, commit=False):
    db = sqlite3.connect(DB_PATH); db.row_factory = sqlite3.Row
    cur = db.execute(sql, args)
    if commit: db.commit()
    rows = cur.fetchone() if one else cur.fetchall()
    db.close()
    return rows

cfg = load_config(); init_db()
C = cfg["couple"]; M = cfg["messages"]

st.set_page_config(page_title="ForeverUs — Our Love Story", page_icon="❤️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;800&family=Poppins:wght@300;400;600&display=swap');
.stApp{background:radial-gradient(1200px 800px at 50% -10%,#2b1030,#0b0710);color:#ffeef4;font-family:'Poppins',sans-serif}
h1,h2,h3{font-family:'Playfair Display',serif !important;color:#f7b1c8 !important}
.glass{background:rgba(255,255,255,.07);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.15);border-radius:20px;padding:28px;box-shadow:0 10px 40px rgba(255,94,138,.15)}
.glow{text-shadow:0 0 24px #ff5e8a,0 0 60px #f7b1c8}
.btn{background:linear-gradient(135deg,#ff5e8a,#e8c476);color:#20101a;font-weight:700;border-radius:999px;padding:12px 28px;border:0;cursor:pointer}
.hero{text-align:center;padding:60px 20px}
.counter{display:flex;gap:12px;justify-content:center;text-align:center;flex-wrap:wrap}
.counter div{flex:1;min-width:110px}.counter b{font-size:38px;color:#e8c476;display:block}
.polaroid{background:#fff;color:#333;padding:10px 10px 30px;border-radius:8px;text-align:center;font-style:italic}
.timeline{border-left:3px solid #ff5e8a;padding-left:20px;margin:10px 0}
.small{opacity:.7;font-size:13px}
</style>
""", unsafe_allow_html=True)

# floating hearts background
components.html("""
<canvas id="h" style="position:fixed;inset:0;pointer-events:none;z-index:1"></canvas>
<script>
const c=document.getElementById('h'),x=c.getContext('2d');c.width=innerWidth;c.height=innerHeight;
let p=[];for(let i=0;i<35;i++)p.push({x:Math.random()*innerWidth,y:Math.random()*innerHeight,v:.4+Math.random()});
(function l(){x.clearRect(0,0,c.width,c.height);x.font='16px serif';p.forEach(q=>{q.y-=q.v;if(q.y<-20){q.y=innerHeight;q.x=Math.random()*innerWidth}x.globalAlpha=.5;x.fillText('❤',q.x,q.y)});requestAnimationFrame(l)})();
</script>
""", height=0)

# music (user gesture required)
st.sidebar.markdown("### 🎵 Music")
if st.sidebar.button("▶ Play / ⏸ Pause music"):
    st.sidebar.markdown(f"<audio autoplay loop controls src='{cfg['music_url']}' style='width:100%'></audio>", unsafe_allow_html=True)

# 1. Welcome
st.markdown(f"""<div class="hero glass">
<p style="letter-spacing:4px;color:#e8c476">{C['name1']} ♥ {C['name2']}</p>
<h1 class="glow" style="font-size:clamp(30px,6vw,56px)">{M['welcome']} ❤️</h1>
<p>Anniversary · {C['anniversary_date']}</p></div>""", unsafe_allow_html=True)
if st.button("Begin Our Journey ↓", key="begin"): st.balloons()

# 2. Counter
st.markdown("## ⏳ Love Duration Counter")
start = datetime.fromisoformat(C["relationship_start"])
s = int((datetime.now()-start).total_seconds())
st.markdown(f"""<div class="glass counter"><div><b>{s//86400}</b><span>days</span></div>
<div><b>{(s%86400)//3600}</b><span>hours</span></div><div><b>{(s%3600)//60}</b><span>minutes</span></div>
<div><b>{s%60}</b><span>seconds</span></div></div>""", unsafe_allow_html=True)
if st.button("Refresh counter"): st.rerun()

# 3. Timeline
st.markdown("## 📖 Our Love Story Timeline")
rows = q("SELECT * FROM memories ORDER BY date")
for r in rows:
    st.markdown(f"""<div class="timeline"><b>{r['title']}</b> <span class="small">{r['date'] or ''}</span><br>{r['description']}</div>""", unsafe_allow_html=True)
with st.expander("➕ Add a memory"):
    with st.form("mem"):
        t=st.text_input("Title"); d=st.date_input("Date"); desc=st.text_area("Description"); img=st.text_input("Image URL (optional)")
        if st.form_submit_button("Save Memory"):
            if t.strip() and desc.strip():
                q("INSERT INTO memories(title,date,description,image) VALUES(?,?,?,?)",(t.strip(),str(d),desc.strip(),img.strip()),commit=True)
                st.success("Memory saved ❤️"); time.sleep(.6); st.rerun()
            else: st.error("Title and description required.")

# 4. Gallery
st.markdown("## 📸 Memory Gallery")
rows = q("SELECT * FROM memories ORDER BY date")
cols = st.columns(3)
for i,r in enumerate(rows):
    with cols[i%3]:
        img = r["image"] or f"https://picsum.photos/seed/forever{i}/500/350"
        st.markdown(f"<div class='polaroid'><img src='{img}' style='width:100%;border-radius:6px'><div>{r['title']}</div></div>", unsafe_allow_html=True)
        if st.button(f"🔍 View", key=f"v{i}"):
            st.image(img, caption=r["title"], use_container_width=True)

# 5. Love universe
st.markdown("## 💫 3D Love Universe")
components.html("""
<canvas id="u" width="800" height="320" style="width:100%;border-radius:16px;background:#140a1c"></canvas>
<script>
const c=document.getElementById('u'),x=c.getContext('2d');let hp=[];
for(let i=0;i<130;i++)hp.push({t:Math.random()*7,s:.005+Math.random()*.008});
(function l(){x.clearRect(0,0,800,320);hp.forEach(p=>{p.t+=p.s;
const hx=16*Math.pow(Math.sin(p.t),3),hy=13*Math.cos(p.t)-5*Math.cos(2*p.t)-2*Math.cos(3*p.t)-Math.cos(4*p.t);
x.fillStyle='#ff5e8a';x.shadowBlur=12;x.shadowColor='#ff5e8a';x.beginPath();x.arc(400+hx*10,160-hy*10,2.6,0,7);x.fill()});
x.shadowBlur=0;x.fillStyle='#e8c476';x.font='16px Georgia';
x.fillText(['I love you','Forever','Mon amour','❤'][Math.floor(Date.now()/2000)%4],360,300);requestAnimationFrame(l)})();
</script>""", height=340)

# 6. Love letter
st.markdown("## 💌 Digital Love Letter")
if "opened" not in st.session_state: st.session_state.opened=False
if st.button("💌 Open the envelope", key="env"): st.session_state.opened=True
if st.session_state.opened:
    letter = st.text_area("Your letter (editable, saved to DB)", value=M["love_letter"], height=200, key="letter")
    components.html(f"""
<div id="tw" style="white-space:pre-wrap;font-size:17px;line-height:1.8;background:rgba(255,255,255,.07);padding:24px;border-radius:16px;border:1px solid rgba(255,255,255,.15)"></div>
<script>const t={json.dumps(letter)};let i=0;const el=document.getElementById('tw');
const iv=setInterval(()=>{{el.textContent+=t[i++]||'';if(i>t.length)clearInterval(iv)}},22);</script>""", height=320)
    if st.button("Save letter"): 
        q("INSERT INTO letters(content,created_at) VALUES(?,?)",(letter,datetime.now().isoformat()),commit=True)
        st.success("Letter saved ❤️")

# 7. Reasons
st.markdown("## 💗 Reasons I Love You")
reasons = cfg.get("reasons", [])
rc = st.columns(3)
for i,r in enumerate(reasons):
    with rc[i%3]:
        if st.button(f"💗 Reveal #{i+1}", key=f"r{i}"): st.info(r)
if st.button("🔀 Shuffle a reason"):
    import random; st.success("💕 "+random.choice(reasons)); st.balloons()

# 8. Surprise gift
st.markdown("## 🎁 Anniversary Surprise")
if st.button("🎁 Open your mystery gift", key="gift"):
    st.balloons(); st.snow()
    st.markdown(f"<div class='glass' style='text-align:center'><h3>🎉 Surprise!</h3><p style='font-size:18px'>{M['surprise']}</p></div>", unsafe_allow_html=True)

# 9. Future dreams + love notes
st.markdown("## ✨ Future Dreams")
for d in cfg.get("dreams", []): st.markdown(f"<div class='glass' style='margin-bottom:8px'>✨ {d}</div>", unsafe_allow_html=True)
st.markdown("### ✍️ Leave a Love Note")
with st.form("note"):
    n=st.text_input("Your name"); msg=st.text_area("Message")
    if st.form_submit_button("Send ❤️"):
        if msg.strip(): q("INSERT INTO messages(name,message,created_at) VALUES(?,?,?)",(n[:100] or "Anonymous",msg.strip(),datetime.now().isoformat()),commit=True); st.success("Sent!"); time.sleep(.5); st.rerun()
        else: st.error("Write something sweet first.")
for r in q("SELECT * FROM messages ORDER BY id DESC LIMIT 20"):
    st.markdown(f"<div class='glass' style='margin-bottom:8px'><b>{r['name']}</b><br>{r['message']}</div>", unsafe_allow_html=True)

# 10. Finale
st.markdown("---")
st.markdown(f"""<div class="hero glass"><h1 class="glow">{M['finale']} ❤️</h1>
<p>{C['name1']} & {C['name2']} · ForeverUs</p></div>""", unsafe_allow_html=True)
if st.button("🎆 Celebrate"): st.balloons(); st.snow(); st.success("Forever & always ❤️")

with st.sidebar.expander("⚙️ Customize"):
    st.write("Edit `config.json` to change names, dates, messages, music, reasons, timeline, and dreams. Then rerun.")
