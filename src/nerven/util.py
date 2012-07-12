import wx, datetime

def date_to_wxdate(date):
    t = date.timetuple()
    return wx.DateTimeFromDMY(t[2], t[1]-1, t[0])

def wxdate_to_date(wxdate):
    ymd = map(int, wxdate.FormatISODate().split('-')) 
    return datetime.date(*ymd) 
