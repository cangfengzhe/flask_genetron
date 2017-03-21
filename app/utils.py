#coding=utf-8
import datetime


def proc_panel(panel):
    if not panel:
        return panel
    panel_name = []
    if '泛生子1号' in panel or '外显子' in panel:
        panel_name.append('WES')
    if '88' in panel:
        panel_name.append('88')
    if '203' in panel:
        panel_name.append('203')
    if '509' in panel:
        panel_name.append('509')
    if '51' in panel:
        panel_name.append(panel)
    if '49' in panel:
        panel_name.append('49')
    if 'ct' in panel or 'CT' in panel or '63' in panel :
        panel_name.append('63')
    if '六项' in panel:
        panel_name.append('6项')
    if panel_name:
        return '+'.join(panel_name)
    else:
        return panel
    



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


def proc_sex(sex):
    return '男' if sex == 1 else '女'