import json, os, sqlite3, re
from flask import Flask, render_template, request, jsonify, g
from datetime import datetime
app = Flask(__name__)
BASE=os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH=os.path.join(BASE,"config.json")
DB_PATH=os.path.join(BASE,"foreverus.db")
def load_config():
 with open(CONFIG_PATH) as f: return json.load(f)
def get_db():
 db=getattr(g,"_db",None)
 if db is None:
  db=g._db=sqlite3.connect(DB_PATH);db.row_factory=sqlite3.Row
 return db
def init_db():
 db=sqlite3.connect(DB_PATH)
 db.execute("CREATE TABLE IF NOT EXISTS memories(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,date TEXT,description TEXT,image TEXT)")
 db.execute("CREATE TABLE IF NOT EXISTS letters(id INTEGER PRIMARY KEY AUTOINCREMENT,content TEXT NOT NULL,created_at TEXT)")
 db.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,message TEXT NOT NULL,created_at TEXT)")
 cur=db.execute("SELECT COUNT(*) FROM memories")
 if cur.fetchone()[0]==0:
  cfg=load_config()
  [db.execute("INSERT INTO memories(title,date,description,image) VALUES(?,?,?,?)",(t["title"],t["date"],t["description"],t.get("image",""))) for t in cfg.get("timeline",[])]
 db.commit();db.close()
@app.teardown_appcontext
def close_db(e):
 db=getattr(g,"_db",None)
 if db: db.close()
@app.route("/")
def index(): return render_template("index.html",config=load_config())
@app.route("/api/config")
def api_config(): return jsonify(load_config())
@app.route("/api/counter")
def api_counter():
 cfg=load_config();s=int((datetime.now()-datetime.fromisoformat(cfg["couple"]["relationship_start"])).total_seconds())
 return jsonify({"days":s//86400,"hours":(s%86400)//3600,"minutes":(s%3600)//60,"seconds":s%60})
def valid(s,m=2000): return isinstance(s,str) and 1<=len(s.strip())<=m
@app.route("/api/memories",methods=["GET","POST"])
def api_memories():
 db=get_db()
 if request.method=="GET": return jsonify([dict(r) for r in db.execute("SELECT * FROM memories ORDER BY date").fetchall()])
 d=request.get_json(force=True)
 if not valid(d.get("title",""),200) or not valid(d.get("description",""),2000): return jsonify({"error":"Invalid"}),400
 cur=db.execute("INSERT INTO memories(title,date,description,image) VALUES(?,?,?,?)",(d["title"].strip(),d.get("date",""),d["description"].strip(),d.get("image","")));db.commit()
 return jsonify({"id":cur.lastrowid}),201
@app.route("/api/letters",methods=["GET","POST"])
def api_letters():
 db=get_db()
 if request.method=="GET": return jsonify([dict(r) for r in db.execute("SELECT * FROM letters ORDER BY id DESC").fetchall()])
 d=request.get_json(force=True)
 if not valid(d.get("content",""),5000): return jsonify({"error":"Invalid"}),400
 cur=db.execute("INSERT INTO letters(content,created_at) VALUES(?,?)",(d["content"].strip(),datetime.now().isoformat()));db.commit()
 return jsonify({"id":cur.lastrowid}),201
@app.route("/api/messages",methods=["GET","POST"])
def api_messages():
 db=get_db()
 if request.method=="GET": return jsonify([dict(r) for r in db.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 50").fetchall()])
 d=request.get_json(force=True)
 if not valid(d.get("message",""),1000): return jsonify({"error":"Invalid"}),400
 cur=db.execute("INSERT INTO messages(name,message,created_at) VALUES(?,?,?)",(d.get("name","Anonymous")[:100],d["message"].strip(),datetime.now().isoformat()));db.commit()
 return jsonify({"id":cur.lastrowid}),201
if __name__=="__main__":
 init_db();app.run(host="0.0.0.0",port=5000,debug=True)
