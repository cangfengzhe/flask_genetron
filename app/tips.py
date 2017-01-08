from datetime import datetime

def strptime(string, format='%Y-%m-%d %H:%M:%S'):
    if string:
        return datetime.strptime(string, format);