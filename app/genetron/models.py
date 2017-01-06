#coding=utf-8
from .. import db
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from datetime import datetime
import  sqlalchemy

def proc_time(time_var, time_fmt = "%Y-%m-%d %H:%M:%S"):
    if time_var:
        return time_var.strftime(time_fmt)
    else:
        return ''

class Patient_info(db.Model):
    __tablenane__ = 'patient_info'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    birth = db.Column(db.Date)
    sex = db.Column(db.Integer)
    email = db.Column(db.String(40))
    tel = db.Column(db.String(30))
    hospital = db.Column(db.String(30))
    
    diagnose_history = db.Column(db.String(500))
    therapy_history = db.Column(db.String(500))
    drug_history = db.Column(db.String(500))
    family_history = db.Column(db.String(500))
    
    indication = db.Column(db.String(500)) # 病理提示
    tissue = db.Column(db.String(150))
    tumor = db.Column(db.String(150))
    ask_histology_time = db.Column(db.DateTime)
    get_histology_time = db.Column(db.DateTime)
    ask_histology = db.Column(db.Boolean, default=False)
    note = db.Column(db.Text)
    sample = db.relationship('Sample_info', backref='patient', lazy="dynamic")



class Sample_info(db.Model):
    __tablename__ = 'sample_info'
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.String(50), nullable=False)
    panel = db.Column(db.String(500))
    tumor_type = db.Column(db.String(50))
    tumor_pos = db.Column(db.String(50))
    collect_time = db.Column(db.DateTime)
    accept_time = db.Column(db.DateTime)
    end_time = db.Column(db.Date)
    is_finish = db.Column(db.Boolean, default=False)
    is_finish_time = db.Column(db.DateTime)
    class_time = db.Column(db.DateTime)
    submit_time = db.Column(db.DateTime)
    bioinfo = db.Column(db.Boolean, default=False)
    bioinfo_time = db.Column(db.DateTime)
    indication = db.Column(db.String(500)) # 病理提示
    tissue = db.Column(db.String(150))
    tumor = db.Column(db.String(150))
    ask_histology_time = db.Column(db.DateTime)
    get_histology_time = db.Column(db.DateTime)
    ask_histology = db.Column(db.Boolean, default=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_info.id'))
    #flowcell_id = db.Column(db.Integer, db.ForeignKey('flowcell_info.id'))
    sample_flowcell = db.relationship('Sample_flowcell', backref='sample', lazy="dynamic")
    note = db.Column(db.String(200))
    snp_indel_info = db.relationship('Sample_snp_indel_info', backref='sample', lazy="dynamic")
    cnv_info = db.relationship('Sample_cnv_info', backref='sample', lazy="dynamic")
    sv_info = db.relationship('Sample_sv_info', backref='sample', lazy="dynamic")
    check_info =  db.relationship('Sample_check_info', backref='sample', lazy="dynamic")
    report_info =  db.relationship('Sample_report_info', backref='sample', lazy="dynamic")
    def __init__(self, **kwargs):
        super(Sample_info, self).__init__(**kwargs)
        if kwargs:
            self.from_dict(kwargs)

    def proc_time(self, time_var, time_fmt = "%Y-%m-%d %H:%M:%S"):
        if time_var:
            return time_var.strftime(time_fmt)
        else:
            return ''

    def proc_panel(self, panel):
        if not panel:
            return panel
        panel_name = []
        if '88' in panel:
            panel_name.append('panel88')
        if '203' in panel:
            panel_name.append('panel203')
        if '509' in panel:
            panel_name.append('panel509')
        if '51' in panel:
            panel_name.append(panel)
        if '49' in panel:
            panel_name.append('panel49')
        if '泛生子1号' in panel:
            panel_name.append('WES')
        if 'ct' in panel:
            panel_name.append('CT_DNA')
        if panel_name:
            return '+'.join(panel_name)
        else:
            return panel
    
    def proc_hospital(self, name):
        if name:
            if '北京大学肿瘤医院' in name:
                return '北肿'
            if '郑州大学第一附属医院' in name:
                return '郑大一附院'
        return '其他'
    
    def get_flowcell_time(self, item_type):
        sample_flowcell = self.sample_flowcell.order_by(
            sqlalchemy.desc(Sample_flowcell.id)).first()
        if sample_flowcell:
            flowcell = sample_flowcell.flowcell
            return self.proc_time(getattr(flowcell,item_type))
        else:
            return ''
    
    def get_item_time(self, item_type):
        sample_flowcell = self.sample_flowcell.order_by(
            sqlalchemy.desc(Sample_flowcell.id)).first()
        if sample_flowcell:
            item = sample_flowcell.sample_time.filter_by(item_type=item_type).order_by(sqlalchemy.desc(Sample_time_info.id)).first()
            if item:
                return self.proc_time(item.item_time, '%Y-%m-%d %H:%M:%S')
            else:
                return ''
        else:
            return ''
        

    @property
    def json(self):
        if self.patient:
            if not self.indication:
                self.indication = self.patient.indication
            if not self.tissue:
                self.tissue = self.patient.tissue
            if not self.tumor:
                self.tumor = self.patient.tumor
        
        return {'DT_RowId' : self.id,
               'sample_id' : self.sample_id,
               'name' : self.patient.name,
               'age' : self.patient.age,
               'sex' : self.patient.sex,
               'hospital' : self.patient.hospital,
               'hospital_alias': self.proc_hospital(self.patient.hospital), 
               'panel': self.proc_panel(self.panel),
               'indication':self.indication,
               'tissue' : self.tissue,
               'tumor' : self.tumor,
               'tumor_pos':self.tumor_pos,
               'tumor_type': self.tumor_type,
               'collect_time':self.proc_time(self.collect_time,"%Y-%m-%d %H:%M:%S"),
               'accept_time': self.proc_time(self.accept_time,"%Y-%m-%d %H:%M:%S"),
                'end_time':self.proc_time(self.end_time,"%Y-%m-%d"),
                'xj_time': self.get_flowcell_time('xj_time'),
                'class_time': self.get_item_time('class'),
                'submit_time':self.get_item_time('submit'),
               'bioinfo': self.bioinfo,
               'bioinfo_time': self.get_item_time('bioinfo_finish'),
                'bioinfo_report_time':self.get_item_time('bioinfo_report'),
                'ask_histology': self.ask_histology,
                'ask_histology_time': self.proc_time(self.ask_histology_time, "%Y-%m-%d %H:%M:%S"),
                'get_histology_time': self.proc_time(self.get_histology_time, "%Y-%m-%d %H:%M:%S"),
                'is_finish': self.is_finish,
                'is_finish_time': self.proc_time(self.is_finish_time, "%Y-%m-%d %H:%M:%S"),
                'note' : self.note
               }

    def from_dict(self, dick_data):
        for (k, w) in dick_data.items():
            setattr(self, k, w)

    def __repr__(self):
        return self.sample_id


class Flowcell_info(db.Model):
    __tablename__='flowcell_info'
    id = db.Column(db.Integer, primary_key=True)
    flowcell_id = db.Column(db.String(10))
    sj_time = db.Column(db.DateTime)
    xj_time = db.Column(db.DateTime)
    cf_time = db.Column(db.DateTime)
    sample_flowcell = db.relationship('Sample_flowcell', backref='flowcell', lazy="dynamic")
    
class Sample_flowcell(db.Model):
    __tablename__='sample_flowcell'
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample_info.id'))
    flowcell_id = db.Column(db.Integer, db.ForeignKey('flowcell_info.id'))
    panel=db.Column(db.String(200))
    sample_time =  db.relationship('Sample_time_info', backref='sample_flowcell_id', lazy="dynamic")
#Cannot drop index 'flowcell_id': needed in a foreign key constraint
    
class Sample_time_info(db.Model):
    __tablename__='sample_time_info'
    id = db.Column(db.Integer, primary_key=True)
    sample_flowcell = db.Column(db.Integer, db.ForeignKey('sample_flowcell.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id') )
    item_type = db.Column(db.String(100))
    item_time = db.Column(db.DateTime, default=datetime.now())
    item_note = db.Column(db.String(200))

class Sample_snp_indel_info(db.Model):
    __tablename__='sample_snp_indel_info'
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample_info.id'))
    panel = db.Column(db.String(100))
    gene_name = db.Column(db.String(100))
    refseq_id = db.Column(db.String(50))
    chrome = db.Column(db.String(10))
    start = db.Column(db.BigInteger)
    end = db.Column(db.BigInteger)
    cDNA_change = db.Column(db.String(100))
    aa_change = db.Column(db.String(100))
    mut_type = db.Column(db.String(100))
    t_depth = db.Column(db.Integer)
    t_freq = db.Column(db.Numeric(5,2))
    n_depth = db.Column(db.Integer)
    n_freq = db.Column(db.Numeric(5,2))
    
    @property
    def json(self):
        return {'sample_id': self.sample.sample_id,
               'panel': self.panel,
               'gene_name': self.gene_name,
               'refseq_id': self.refseq_id,
               'chrome': self.chrome,
               'start': self.start,
               'end': self.end,
               'cDNA_change': self.cDNA_change,
               'aa_change': self.aa_change,
               't_freq': str(self.t_freq),
               'mut_type': self.mut_type}
    # mk_user = db.relationship('users', backref='sample_mut_info', lazy="dynamic")
    # mk_time = db.Column(db.DateTime)
    # checked = db.Column(db.Boolean, default=False)
    # check_user = db.relationship('users', backref='sample_mut_info', lazy='dynamic')
    # check_time = db.Column(db.DateTime)
    
    
class Sample_cnv_info(db.Model):
    
    __tablename__='sample_cnv_info'
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample_info.id'))
    panel = db.Column(db.String(100))
    gene_name = db.Column(db.String(100))
    chrome = db.Column(db.String(10))
    start = db.Column(db.BigInteger)
    end = db.Column(db.BigInteger)
    fold = db.Column(db.Numeric(6,2))
    cnv_type = db.Column(db.String(50))
    
    @property
    def json(self):
        return {
            'id': self.id,
            'sample_id': self.sample.sample_id,
            'panel': self.panel,
           'gene_name': self.gene_name,
           'chrome': self.chrome,
           'start': self.start,
           'end': self.end,
           'cnv_type': self.cnv_type,
           'fold': str(self.fold)
               }   

    
class Sample_sv_info(db.Model):
    
    __tablename__='sample_sv_info'
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample_info.id'))
    panel = db.Column(db.String(100))
    gene_name = db.Column(db.String(100))
    break_pos = db.Column(db.String(250))
    extron_pos = db.Column(db.String(10))
    freq = db.Column(db.Numeric(5,2))
    
    @property
    def json(self):
        return {
            'id': self.id,
            'sample_id': self.sample.sample_id,
           'panel': self.panel,
           'gene_name': self.gene_name,
           'break_pos': self.break_pos,
           'extron_pos': self.extron_pos,
           'freq': str(self.freq)
               }


class Biomarker(db.Model):
    """
    基因	Tissue	Tissue (中文)	基因描述	临床意义	Glossary (Gene review)	Summary	Incidence in disease	Effect on drug sensitivity	Effect on drug resistance
"""
    __tablename__='biomarker'
    id = db.Column(db.Integer, primary_key=True)
    gene_name = db.Column(db.String(100))
    tissue_cn = db.Column(db.String(100))
    tissue_en = db.Column(db.String(100))
    gene_info = db.Column(db.Text)
    clinical_info = db.Column(db.Text)
    glossary = db.Column(db.Text)
    summary = db.Column(db.Text)
    incidence_in_disease = db.Column(db.Text)
    effect_of_drug_sensitivity = db.Column(db.Text)
    effect_on_drug_resistance = db.Column(db.Text)
    mk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mk_time = db.Column(db.DateTime)
    checked = db.Column(db.Boolean, default=False)
    check_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    check_time = db.Column(db.DateTime)

    
    
class Molecular_function(db.Model):
    """
    Gene	Tissue	Tissue (中文)	核苷酸变化	AA(abb)	AA	molecular function	位点解析（中文）	 更新记录
"""
    __tablename__='molecular_function'
    id = db.Column(db.Integer, primary_key=True)
    gene_name = db.Column(db.String(50))
    tissue_cn = db.Column(db.String(100))
    tissue_en = db.Column(db.String(100))
    aa_change = db.Column(db.String(50))
    pos_info = db.Column(db.Text)
    mf = db.Column(db.Text)
    update_log = db.Column(db.String(200))
    mk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mk_time = db.Column(db.DateTime)
    checked = db.Column(db.Boolean, default=False)
    check_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    check_time = db.Column(db.DateTime)

    
class Sample_report_info(db.Model):
    """
    样本报告、报告完成
    """
    __tablename__='sample_report_info'
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample_info.id'))
    panel = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    report_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    report_time = db.Column(db.DateTime)
    check_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    check_time = db.Column(db.DateTime)
    finish_time = db.Column(db.DateTime)
    note=db.Column(db.String(500))
    
    def json():
        return {
            'id': self.id,
            'sample_id': self.sample.sample_id,
            'pane': self.panel,
            'start_time': self.start_time,
            'writer':self.reporter.username,
            'report_time': proc_time(self.report_time),
            'checker': self.checker.username,
            'check_time': proc_time(self.check_time),
            'finish_time': proc_time(self.finish_time),
            'note': self.note
            }
    
class Sample_check_info(db.Model):
    """
    样本验证时间
    """
    __tablename__ = 'sample_check_info'
    id = db.Column(db.Integer, primary_key=True)
    flowcell_id = db.Column(db.String(40))
    panel = db.Column(db.String(40))
    check_type = db.Column(db.String(200))
    gene_name = db.Column(db.String(200))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    result = db.Column(db.String(100))
    note = db.Column(db.String(500))
    sample_id = db.Column(db.Integer, db.ForeignKey('sample_info.id'))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    @property
    def json(self):
        return {'id':self.id,
            'sample_id': self.sample.sample_id,
                'flowcell_id': self.flowcell_id,
               'panel': self.panel,
               'gene_name': self.gene_name,
               'start_time': proc_time(self.start_time),
               'end_time': proc_time(self.end_time),
                'check_type':self.check_type,
               'result': self.result,
               'note': self.note,
               }   


    
class Send_info(db.Model):
    __tablename__ = 'infomation'
    id = db.Column(db.Integer, primary_key=True)
    send_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receive_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    info_type = db.Column(db.String(100))
    info_msg = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.now())
    read = db.Column(db.DateTime, default = False)


    def json(self):
        return {
            'send_user':self.send_user.username,
            'info_type':self.info_type,
            'msg': self.info_msg,
        }