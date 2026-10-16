TEMPLATES={
 "romantic":("{a}, my love {b}: every heartbeat whispers your name. {mem} Happy anniversary, my forever.","template"),
 "emotional":("Through every tear and triumph, {b}, you are my home, {a} confesses. {mem} I love you endlessly.","template"),
 "poetic":("Like stars scripted in velvet skies, {a} found {b}. {mem} Our love, a poem with no final line.","template"),
 "funny":("Warning {b}: {a} still steals the blanket and your fries. {mem} Wouldn't have it any other way!","template"),
 "deep":("{b}, in the quiet between heartbeats, {a} found eternity. {mem} You are my always.","template")}
def generate_letter(a,b,tone,mem=""):
    t,mode=TEMPLATES.get(tone,TEMPLATES["romantic"])
    return t.format(a=a,b=b,mem=(mem+" " if mem else "")),mode
def validate_text(s,m=2000): return isinstance(s,str) and 1<=len(s.strip())<=m
REASONS=[f"Reason {i+1}: you turn ordinary days into magic." for i in range(100)]
