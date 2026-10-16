import os,sys;sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))
from utils.dates import love_duration,next_anniversary
from utils.generators import generate_letter,validate_text,REASONS
from PIL import Image
def test_duration(): d=love_duration("2022-02-14"); assert d["total_days"]>700 and d["years"]>=1
def test_countdown(): assert next_anniversary("2023-02-14")["days_left"]>=0
def test_feb29(): r=next_anniversary("2020-02-29"); assert r["date"][5:]=="02-28" or r["date"][5:]=="02-29"
def test_letter(): t,m=generate_letter("A","B","poetic","stars"); assert "A" in t and m=="template"
def test_validation(): assert validate_text("hi") and not validate_text("")
def test_reasons(): assert len(REASONS)==100
def test_card(tmp_path):
    im=Image.new("RGB",(800,600),(255,77,141)); p=str(tmp_path/"c.png"); im.save(p); assert os.path.exists(p)
