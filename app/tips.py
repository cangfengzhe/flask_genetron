import datetime

def strptime(string, format='%Y-%m-%d %H:%M:%S'):
    if string:
        return datetime.datetime.strptime(string, format);
    
def datetime2str(dt, format='%Y-%m-%d %H:%M:%S'):
    if isinstance(dt, datetime.datetime):
        return dt.strftime(format)
    else:
        return ''
    
def date2str(dt, format='%Y-%m-%d'):
    return datetime2str(dt)
    