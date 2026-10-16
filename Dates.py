from datetime import date, datetime
from dateutil.relativedelta import relativedelta
def parse(d):
    return datetime.strptime(d,"%Y-%m-%d").date() if isinstance(d,str) else d
def love_duration(start):
    s=parse(start); n=date.today(); rd=relativedelta(n,s)
    return {"years":rd.years,"months":rd.months,"days":rd.days,"total_days":(n-s).days}
def next_anniversary(ann):
    """Feb 29 policy: celebrated on Feb 28 in non-leap years."""
    m,d=parse(ann).month,parse(ann).day
    t=date.today()
    def mk(y):
        if m==2 and d==29:
            import calendar
            return date(y,2,29 if calendar.isleap(y) else 28)
        return date(y,m,d)
    nxt=mk(t.year)
    if nxt<=t: nxt=mk(t.year+1)
    return {"date":nxt.isoformat(),"days_left":(nxt-t).days}
