#coding=utf-8
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

def proc_hospital(name):
    if name:
        if '北京大学肿瘤医院' in name:
            return '北肿'
        if '郑州大学第一附属医院' in name:
            return '郑大一附院'
    return '其他'
    