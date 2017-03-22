# coding=utf-8


import os
import datetime



from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from sqlalchemy import text
from json import dumps

from . import api
from app.genetron.configure import Configure as configure
from app.models import *
from app.genetron.models import *
from .. import app_dir
from app.utils import *
from flask_login import current_user

def get_todo_sample(xx):
    sample_id = xx.sample_flowcell_id.sample.sample_id
    if not xx.sample_flowcell_id.sample.patient:
        return False
    is_finish = xx.finish
    panel = xx.sample_flowcell_id.panel
    if (('LAA' in sample_id and sample_id[-2] == 'T') or \
                ('LAA' not in sample_id and 'T' in sample_id) or \
                panel == 'CT_DNA' or  panel == 'panel51')  and \
                    panel in configure.panel_clinical and \
            not is_finish:
        return True
    else:
        return False


class SnpIndel(Resource):
    def get(self, id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            snp_indel_info = sample.snp_indel_info
            return jsonify(data=[xx.json for xx in snp_indel_info if not xx.removed])
        else:
            return jsonify(data='error')
        
    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        args = parser.parse_args()
        snv_indel_id = args.id
        snv_indel = Sample_snp_indel_info.query.get(snv_indel_id)
        
        snv_indel.removed = True
        print(snv_indel_id, snv_indel.removed)
        snv_indel.user_id = current_user.id
        db.session.commit()
        return {'id': snv_indel_id}


class Cnv(Resource):
    def get(self, id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            cnv_info = sample.cnv_info
            return jsonify(data=[xx.json for xx in cnv_info if not xx.removed])
        else:
            return jsonify(data='error')


    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        args = parser.parse_args()
        cnv_id = args.id
        cnv = Sample_cnv_info.query.get(cnv_id)
        cnv.removed = True
        cnv.user_id = current_user.id
        db.session.commit()
        return jsonify({'id':cnv_id})


class Sv(Resource):
    def get(self, id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            sv_info = sample.sv_info
            return jsonify(data=[xx.json for xx in sv_info if not xx.removed])
        else:
            return jsonify(data='error')
        
    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        
        args = parser.parse_args()
        sv_id = args.id
        sv = Sample_sv_info.query.get(sv_id)
        sv.removed = True
        sv.user_id = current_user.id
        db.session.commit()
        return jsonify({'id':sv_id})


class Check_info(Resource):
    def get(self, sample_id):
        sample = Sample_info.query.filter_by(sample_id=sample_id).first()
        if sample:
            check_info = sample.check_info
            return jsonify(data=[xx.json for xx in check_info])
        else:
            return jsonify(data='error')

    def post(self, sample_id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id')
        parser.add_argument('flowcell_id', type=str, help='flowcell_id')
        parser.add_argument('panel', type=str, help='panel')
        parser.add_argument('check_type', type=str, help='check_type')
        parser.add_argument('gene_name', type=str, help='gene_name')
        parser.add_argument('start_time', type=str, help='start_time')
        parser.add_argument('end_time', type=str, help='end_time')
        parser.add_argument('result', type=str, help='result')
        parser.add_argument('note', type=str, help='note')
        # parser.add_argument('callback', type=str, help='note')
        args = parser.parse_args()
        id = args.id
        flowcell_id = args.flowcell_id
        panel = args.panel
        check_type = args.check_type
        gene_name = args.gene_name
        start_time = args.start_time
        end_time = args.end_time
        result = args.result
        note = args.note
        # callback=args.callback
        sample = Sample_info.query.filter_by(sample_id=sample_id).first()

        if id != '':
            # // update
            check_info = Sample_check_info.query.get(id)
            check_info.sample_id = sample.id
            check_info.flowcell_id = flowcell_id
            check_info.panel = panel
            check_info.check_type = check_type
            check_info.gene_name = gene_name
            check_info.start_time = start_time
            check_info.end_time = end_time
            check_info.result = result
            check_info.note = note
            db.session.commit()
            return jsonify(data=[check_info.json])
            # return jsonify(data={})
            # return '{}'
        else:
            # creat
            check_info = Sample_check_info(sample_id=sample.id, flowcell_id=flowcell_id, panel=panel,
                                           check_type=check_type, gene_name=gene_name,
                                           start_time=start_time, end_time=end_time, result=result, note=note)
            db.session.add(check_info)
            db.session.commit()
            return jsonify(data=[check_info.json])

    def delete(self, sample_id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id')
        args = parser.parse_args()
        id = args.id
        check_info = Sample_check_info.query.get(id)
        db.session.delete(check_info)
        db.session.commit()
        return jsonify(data=[{'id': id}])

    
def proc_finish_time(sample, panel, finish_time):
    sf = Sample_flowcell.query.filter_by(sample_id=sample.id, panel=panel).order_by(
    sqlalchemy.desc(Sample_flowcell.id)).first()
    sf.sample_flowcell_info.first().finish = True
    sf.sample_flowcell_info.first().finish_time = finish_time
    db.session.commit()

    
class Report_info(Resource):
    def get(self, sample_id):
        sample = Sample_info.query.filter_by(sample_id=sample_id).first()
        if sample:
            report_info = sample.report_info
            return jsonify(data=[xx.json for xx in report_info])
        else:
            return jsonify(data='error')

    def post(self, sample_id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id')
        parser.add_argument('panel', type=str, help='panel')
        parser.add_argument('start_time', type=str, help='check_type')
        parser.add_argument('reporter', type=str, help='gene_name')
        parser.add_argument('report_type', type=str)
        # parser.add_argument('checker', type=str, help='end_time')
        # parser.add_argument('check_time', type=str, help='result')
        parser.add_argument('finish_time', type=str, help='result')
        parser.add_argument('note', type=str, help='note')
        # parser.add_argument('callback', type=str, help='note')
        args = parser.parse_args()
        id = args.id
        panel = args.panel
        start_time = args.start_time
        reporter = args['reporter']
        report_type = args.report_type
        # checker = args['checker']
        # check_time = args.check_time
        finish_time = args.finish_time
        note = args.note
        # callback=args.callback
        sample = Sample_info.query.filter_by(sample_id=sample_id).first()

        if id != '':
            # // update
            report_info = Sample_report_info.query.get(id)
            report_info.sample_id = sample.id
            report_info.panel = panel
            report_info.start_time = strptime(start_time)
            report_info.report_user_id = reporter  # User.query.filter_by(username=writer).first().id
            report_info.report_type = report_type
            # report_info.check_user_id = checker  # User.query.filter_by(username=checker).first().id
            # report_info.check_time = strptime(check_time)
            report_info.finish_time = strptime(finish_time)
            report_info.note = note
            if report_type == '复核' and report_info.finish_time:
                proc_finish_time(sample, panel, report_info.finish_time)
                
            db.session.commit()
            return jsonify(data=[report_info.json])
            # return jsonify(data={})
            # return '{}'
        else:
            # create
            report_info = Sample_report_info()
            report_info.sample_id = sample.id
            report_info.panel = panel
            report_info.start_time = strptime(start_time)
            report_info.report_user_id = reporter  # User.query.filter_by(username=writer).first().id
            report_info.report_type = report_type
            # report_info.check_user_id = checker  # User.query.filter_by(username=checker).first().id
            # report_info.check_time = strptime(check_time)
            report_info.finish_time = strptime(finish_time)
            report_info.note = note
            db.session.add(report_info)
            if report_type == '复核' and report_info.finish_time:
                proc_finish_time(sample, panel, report_info.finish_time)
            
            db.session.commit()
            return jsonify(data=[report_info.json])

    def delete(self, sample_id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id')
        args = parser.parse_args()
        id = args.id

        report_info = Sample_report_info.query.get(id)
        db.session.delete(report_info)
        db.session.commit()
        return jsonify(data=[{'id': id}])


class Report_User(Resource):
    def get(self, role_name):
        role = Role.query.filter_by(name=role_name).first()
        users = role.users
        response = make_response(dumps([xx.json for xx in users]))
        response.headers['Content-Type'] = 'application/json'
        return response



class Sample_Flowcell_Info(Resource):
    def get(self):
        return jsonify(data=[xx.json for xx in Sample_flowcell_info.query.all() if get_todo_sample(xx)])
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, help='id')
        parser.add_argument('is_problem', type=str)
        args = parser.parse_args()
        id = args.id
        is_problem = args.is_problem
        sf = Sample_flowcell_info.query.get(id)
        if is_problem == 'true':
            sf.is_problem = True
        if is_problem == 'false':
            sf.is_problem = False
        db.session.commit()
        return jsonify(data=[sf.json])
            
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, help='id')
        parser.add_argument('is_problem', type=str)
        args = parser.parse_args()
        id = args.id
        sf = Sample_flowcell_info.query.get(id)
        sf.finish = True
        return jsonify(data=[{'id': id}])
        
    
class Sample_Stat(Resource):
    
    def get(self):
        sql=text("""
SELECT
  sample_info.sample_id, #0
  patient_info.name,
  patient_info.hospital,
  sample_flowcell.panel,
  sample_info.indication,
  sample_info.tissue, # 5
  sample_info.tumor, 
  sample_info.collect_time,
  sample_info.accept_time,
  flowcell_info.xj_time,
  flowcell_info.cf_time, #10
  sample_flowcell_info.class_time,
  sample_flowcell_info.submit_time,
  sample_flowcell_info.bioinfo_finish_time,
  sample_flowcell_info.bioinfo_report_time,
  sample_info.ask_histology_time, # 15
  sample_info.get_histology_time,
  sample_flowcell_info.finish_time,
  sample_flowcell_info.finish,
  sample_flowcell_info.finish_time,
  max_flowcell.count, #20
  max_flowcell.flowcell_concat,
  first_xj.flowcell_id,
  first_xj.xj_time,
  first_xj.bioinfo_finish_time,
  check_info.check_info, #25
  note_info.note_info,
  sample_info.note # 27
FROM sample_flowcell
  # 选择最近一次的下机信息
  left JOIN (SELECT
                max(sample_flowcell.id)                 AS id,
                count(sample_flowcell.id)               AS count,
                group_concat(flowcell_info.flowcell_id) AS flowcell_concat
              FROM sample_flowcell
                INNER JOIN flowcell_info ON sample_flowcell.flowcell_id = flowcell_info.id
              GROUP BY sample_flowcell.sample_id, sample_flowcell.panel) AS max_flowcell
    ON sample_flowcell.id = max_flowcell.id

  # 获取第一次下机信息
  LEFT JOIN
  (SELECT
     min_sample_flowcell.sample_id,
     min_sample_flowcell.panel,
     flowcell_info.flowcell_id,
     flowcell_info.xj_time,
     sample_flowcell_info.bioinfo_finish_time
   FROM
     (SELECT
        min(id) AS min_sample_flowcell_id,
        flowcell_id,
        sample_id,
        panel
      FROM sample_flowcell
      GROUP BY sample_id, panel) AS min_sample_flowcell
     LEFT JOIN flowcell_info ON flowcell_info.id = min_sample_flowcell.flowcell_id
     LEFT JOIN sample_flowcell_info
       ON sample_flowcell_info.sample_flowcell = min_sample_flowcell.min_sample_flowcell_id) AS first_xj
    ON first_xj.sample_id = sample_flowcell.sample_id AND first_xj.panel = sample_flowcell.panel
  LEFT JOIN sample_flowcell_info ON sample_flowcell_info.sample_flowcell = sample_flowcell.id
  LEFT JOIN sample_info ON sample_info.id = sample_flowcell.sample_id
  LEFT JOIN flowcell_info ON flowcell_info.id = sample_flowcell.flowcell_id
  LEFT JOIN patient_info ON patient_info.id = sample_info.patient_id
  LEFT JOIN
  (SELECT
     sample_id,
     panel,
     group_concat(
         concat(flowcell_id, '下机样本于 ', start_time, ' 申请进行', if(gene_name is null , '', gene_name), ' ', check_type, '验证, ', end_time, ' 反馈结果：',
                result) SEPARATOR ';') AS check_info
   FROM sample_check_info
   GROUP BY sample_id, panel) AS check_info
    ON check_info.sample_id = sample_flowcell.sample_id AND check_info.panel = sample_flowcell.panel
  LEFT JOIN
  (SELECT
     sample_id,
     panel,
     group_concat(concat(flowcell_id, '下机样本', note) SEPARATOR ';') AS note_info
   FROM sample_note_info
   GROUP BY sample_id, panel) AS note_info
    ON note_info.sample_id = sample_flowcell.sample_id AND note_info.panel = sample_flowcell.panel
HAVING sample_flowcell.panel IN ('panel203', 'panel509', 'panel51', 'panel88', 'WES', 'CT_DNA', 'CT_SEQ') AND
       ((sample_info.sample_id LIKE '%T%' AND sample_info.sample_id NOT LIKE 'LAA%') OR
        (substring(sample_info.sample_id, 7, 1) = 'T' AND sample_info.sample_id LIKE 'LAA%') OR
        (sample_flowcell.panel like 'CT%')
        ) AND
       sample_info.tissue IS NOT NULL;

""")

        result = db.engine.execute(sql).fetchall()
        sample_list = []

        for row in result:
            sample_dict = {
               'sample_id' : row[0],
               'name' : row[1],
               'hospital' : row[2],
               'panel': row[3],
               'indication': row[4],
               'tissue' : row[5],
               'tumor' : row[6], 
               'collect_time': date2str(row[7]), #sample_info.collect_time, 
               'accept_time': datetime2str(row[8]),  #sample_info.accept_time,
                'end_time': '',
                'xj_time': datetime2str(row[9]),
                'class_time': datetime2str(row[11]),
                'submit_time': datetime2str(row[12]),
               'bioinfo_time': datetime2str(row[13]),
                'bioinfo_report_time': datetime2str(row[14]),
                # 'ask_histology': datetime2str(row[15]),
                'ask_histology_time': datetime2str(row[15]),
                'get_histology_time': datetime2str(row[16]),
                'is_finish_time': datetime2str(row[19]),
                'is_finish': date2str(row[18]),
                
                'xj_count': row[20], # 下机count
                'xj_flowcell':row[21],
                'first_flowcell': row[22],
                'first_xj_time': datetime2str(row[23]),
                'frist_bioinfo_finish_time': datetime2str(row[24]),
                'check_info': row[25],
                'note_info': row[26],
                'report_note': row[27]
            }

            sample_list.append(sample_dict)
        return jsonify(data=[xx for xx in sample_list])
    
class Note_info(Resource):
    def get(self, sample_id):
        sample = Sample_info.query.filter_by(sample_id=sample_id).first()
        if sample:
            note_info = sample.note_info
            return jsonify(data=[xx.json for xx in note_info])
        else:
            return jsonify(data='error')

    def post(self, sample_id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id')
        parser.add_argument('flowcell_id', type=str, help='flowcell_id')
        parser.add_argument('panel', type=str, help='panel')
        parser.add_argument('note', type=str, help='note')
        # parser.add_argument('callback', type=str, help='note')
        args = parser.parse_args()
        id = args.id
        flowcell_id = args.flowcell_id
        panel = args.panel
        note = args.note
        # callback=args.callback
        sample = Sample_info.query.filter_by(sample_id=sample_id).first()

        if id != '':
            # // update
            note_info = Sample_note_info.query.get(id)
            note_info.sample_id = sample.id
            note_info.flowcell_id = flowcell_id
            note_info.panel = panel
            note_info.note = note
            db.session.commit()
            return jsonify(data=[note_info.json])
            # return jsonify(data={})
            # return '{}'
        else:
            # creat
            note_info = Sample_note_info(sample_id=sample.id, flowcell_id=flowcell_id, panel=panel,
                                           note=note)
            db.session.add(note_info)
            db.session.commit()
            return jsonify(data=[note_info.json])

    def delete(self, sample_id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id')
        args = parser.parse_args()
        id = args.id
        note_info = Sample_note_info.query.get(id)
        db.session.delete(note_info)
        db.session.commit()
        return jsonify(data=[{'id': id}])

    
class Barcode(Resource):
    
    def barcodepng(self, code, outdir):
        import barcode
        from barcode.writer import ImageWriter
        
        for xx in os.listdir(outdir):
            os.remove(os.path.join(outdir, xx))
        
        try:
            x = barcode.get_barcode_class('code39')
            x.default_writer_options['module_height']=5.128205128205129
            x.default_writer_options['module_width']=0.1
            x.default_writer_options['font_size'] = 0
            x.default_writer_options['quiet_zone'] = 0
            y = x(code,writer=ImageWriter(),add_checksum=False)
            fullname = y.save(os.path.join(outdir,code))
            return code + '.png'
        except barcode.errors.WrongCountryCodeError:
            pass
        
    def get(self, code):
        pic_name = self.barcodepng(code, os.path.join(app_dir,'static', 'barcode'))
        if pic_name:
            return jsonify(data=[{'file_name': pic_name, 'stutas':'success'}])
        else:
            return jsonify(data=[{'stutas':'error'}])


class Sample(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id')
        parser.add_argument('tissue', type=str)
        parser.add_argument('tumor', type=str, )
        parser.add_argument('indication', type=str)
        parser.add_argument('note', type=str)
        parser.add_argument('ask_histology', type=str)
        args = parser.parse_args()
        row_id = args.id
        sample = Sample_info.query.get(row_id)
        args.pop('id')
        if '[object Object]' in [args['tissue'],  args['tumor']]:
            return 'error'
        
        
        if args['ask_histology'] == 'true':
            args['ask_histology'] = True
            sample.ask_histology_time = datetime.datetime.now()
        elif args['ask_histology'] == 'false':
            args['ask_histology'] = False
            
        else:
            args['ask_histology'] = False
        
        for xx in args:
            setattr(sample, xx, args[xx])
            if xx in ['tissue','tumor']:
                sample.get_histology_time = datetime.datetime.now()
                      
        db.session.commit()
        return jsonify(data=[sample.json])

class Tissue(Resource):
    
    def get(self):
        tissues = Tissue_info.query.all()
        response = make_response(dumps([xx.json for xx in tissues]))
        response.headers['Content-Type'] = 'application/json'
        return response

    
class Tumor(Resource):
    
    def get(self):
        tumors = Tumor_info.query.all()
        response = make_response(dumps([xx.json for xx in tumors]))
        response.headers['Content-Type'] = 'application/json'
        return response

class My_Work(Resource):
    
    def get(self,user_id, work_type):
        if work_type == 'bioinfo':
            sample_flowcell = Sample_flowcell_info.query.filter_by(user_id=user_id)
            return jsonify(data=[xx.my_work_json for xx in sample_flowcell])
        if work_type == 'report':
            dt = Sample_report_info.query.filter_by(report_user_id=user_id)
            return jsonify(data = [{
                    'sample_id': xx.sample.sample_id,
                    'panel': xx.panel,
                    'type': xx.report_type,
                    'start_time': datetime2str(xx.start_time),
                    'finish_time': datetime2str(xx.finish_time),
                    } for xx in dt])

class Mut_Info(Resource):
    
    def get(self):
        sql = text("""
SELECT
  sample_info.sample_id, # 0
  patient_info.name,
  patient_info.age,
  patient_info.sex,
  patient_info.dept,
  patient_info.doctor, # 5
  sample_info.indication,
  sample_info.tumor_type,
  sample_info.panel,
  mut_info.gene_name,
  mut_info.mut_type, # 10 
  mut_info.freq,
  mut_info.aa_change,
  mut_info.cDNA_change,
  sample_info.accept_time,
  sample_info.tissue, #15
  sample_info.tumor, #16
  report_time.finish_time,
  patient_info.xiaoshou 
FROM sample_info
  LEFT JOIN patient_info ON sample_info.patient_id = patient_info.id
  LEFT JOIN ((SELECT DISTINCT
                sample_id,
                gene_name,
                cDNA_change,
                aa_change,
                mut_type,
                concat(t_freq, '%') AS freq
              FROM sample_snp_indel_info where removed = 0)
             UNION (SELECT DISTINCT
                      sample_id,
                      gene_name,
                      '',
                      '',
                      '扩增',
                      concat(fold, '倍') AS freq
                    FROM sample_cnv_info where removed = 0)
             UNION (SELECT DISTINCT
                      sample_id,
                      gene_name,
                      '',
                      break_pos,
                      '结构变异',
                      concat(freq * 100, '%') AS freq
                    FROM sample_sv_info where removed = 0)) AS mut_info
    ON mut_info.sample_id = sample_info.id
    left join (select sample_id, finish_time from sample_report_info where report_type = '复核') as report_time
    on report_time.sample_id = sample_info.id
WHERE sample_info.is_show = 1;
        
        """)
        result = db.engine.execute(sql).fetchall()
        mut_list = []
        
        for row in result:
            mut_dict = {
               'sample_id' : row[0],
               'name' : row[1],
               'age' : row[2],
               'sex': proc_sex(row[3]),
               'dept': row[4],
               'doctor' : row[5],
               'indication' : row[6], 
                'tumor_type': row[7],
                'panel': proc_panel(row[8]),
                'gene_name': row[9],
                'mut_type': row[10],
                'freq': row[11],
                'aa_change':row[12],
                'cDNA_change':row[13],
                'accept_time': datetime2str(row[14]),
                'tissue':row[15],
                'tumor':row[16],
                'finish_time': datetime2str(row[17]),
                'xiaoshou': row[18]
                }
            mut_list.append(mut_dict)
        return jsonify(data=[xx for xx in mut_list]) 
        
 


api.add_resource(SnpIndel, '/snpindel/<string:id>')
api.add_resource(Cnv, '/cnv/<string:id>')
api.add_resource(Sv, '/sv/<string:id>')
api.add_resource(Check_info, '/check/<string:sample_id>')
api.add_resource(Note_info, '/note/<string:sample_id>')
api.add_resource(Report_info, '/report/<string:sample_id>')
api.add_resource(Report_User, '/user/<string:role_name>')
api.add_resource(Sample_Flowcell_Info, '/sample_flowcell')
api.add_resource(Sample_Stat, '/sample_stat')
api.add_resource(Barcode, '/barcode/<string:code>')
api.add_resource(Sample, '/sample/')
api.add_resource(Tissue, '/tissue/')
api.add_resource(Tumor, '/tumor/')
api.add_resource(Mut_Info, '/mut_info/')
api.add_resource(My_Work, '/my_work/<string:work_type>/<int:user_id>')

