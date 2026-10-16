import sqlite3, os
DB=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"foreververse.db")
def init():
    db=sqlite3.connect(DB)
    db.execute("CREATE TABLE IF NOT EXISTS capsule(id INTEGER PRIMARY KEY AUTOINCREMENT,message TEXT,created TEXT,reveal TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS dreams(id INTEGER PRIMARY KEY AUTOINCREMENT,text TEXT,done INTEGER DEFAULT 0)")
    db.execute("CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,message TEXT)")
    if db.execute("SELECT COUNT(*) FROM dreams").fetchone()[0]==0:
        for d in ["Travel to Paris together","Build our dream home","Watch sunsets in Santorini"]:
            db.execute("INSERT INTO dreams(text) VALUES(?)",(d,))
    db.commit();db.close()
def add_capsule(msg,reveal):
    from datetime import date
    db=sqlite3.connect(DB);db.execute("INSERT INTO capsule(message,created,reveal) VALUES(?,?,?)",(msg,str(date.today()),reveal));db.commit();db.close()
def list_capsule():
    db=sqlite3.connect(DB);db.row_factory=sqlite3.Row
    rows=db.execute("SELECT * FROM capsule ORDER BY id DESC").fetchall();db.close();return rows
