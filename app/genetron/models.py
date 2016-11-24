#coding=utf-8
from .. import db
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
    sample_id = db.Column(db.String(10), nullable=False)
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
    flowcell_id = db.Column(db.Integer, db.ForeignKey('flowcell_info.id'))
    note = db.Column(db.String(200))


    def __init__(self, **kwargs):
        super(Sample_info, self).__init__(**kwargs)
        if kwargs:
            self.from_dict(kwargs)

    def proc_time(self, time_var, time_fmt = "%Y-%m-%d %H:%M:%S"):
        if time_var:
            return time_var.strftime(time_fmt)
        else:
            return ''

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return [self.patient_id,
               self.name,
               self.age,
               self.sex,
               self.hospital,
               self.histology,
               self.tissue,
               self.indication,
               self.panel,
               self.bioinfo,
               self.start_time,
               self.dead_line,
               self.note]

    def proc_panel(self, panel):
        if '88' in panel:
            return 'Panel88'
        elif '203' in panel:
            return 'Panel203'
        elif '509' in panel:
            return 'Panel509'
        elif '51' in panel:
            return panel
        elif '49' in panel:
            return 'Panel49'
        elif '泛生子1号' in panel:
            return 'WES'
        elif 'ct' in panel:
            return 'ctDNA'
        else:
            return panel
    @property
    def json(self):
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
               'panel': self.proc_panel(self.panel),
               'indication':self.indication,
               'tissue' : self.tissue,
               'tumor' : self.tumor,
               'tumor_pos':self.tumor_pos,
               'tumor_type': self.tumor_type,
               'collect_time':self.proc_time(self.collect_time,"%Y-%m-%d %H:%M:%S"),
               'accept_time': self.proc_time(self.accept_time,"%Y-%m-%d %H:%M:%S"),
                'end_time':self.proc_time(self.end_time,"%Y-%m-%d"),
                'class_time':self.proc_time(self.class_time,"%Y-%m-%d %H:%M:%S"),
                'submit_time':self.proc_time(self.submit_time,"%Y-%m-%d %H:%M:%S"),
               'bioinfo': self.bioinfo,
               'bioinfo_time': self.proc_time(self.bioinfo_time, "%Y-%m-%d %H:%M:%S"),
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
    machine_type = db.Column(db.String(10))
    machine_id = db.Column(db.String(10))
    sj_time = db.Column(db.DateTime)
    xj_time = db.Column(db.DateTime)
    sample = db.relationship('Sample_info', backref='flowcell', lazy="dynamic")
