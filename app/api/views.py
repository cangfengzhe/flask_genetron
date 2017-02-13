# coding=utf-8

from json import dumps

from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from sqlalchemy import text

from . import api
from ..genetron.configure import Configure as configure
from ..models import *
from ..tips import *


def get_todo_sample(xx):
    sample_id = xx.sample_flowcell_id.sample.sample_id
    if not xx.sample_flowcell_id.sample.patient:
        return False
    is_finish = xx.finish
    panel = xx.sample_flowcell_id.panel
    if (('LAA' in sample_id and sample_id[-2] == 'T') or \
                ('LAA' not in sample_id and 'T' in sample_id)) and \
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
            return jsonify(data=[xx.json for xx in snp_indel_info])
        else:
            return jsonify(data='error')


class Cnv(Resource):
    def get(self, id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            cnv_info = sample.cnv_info
            return jsonify(data=[xx.json for xx in cnv_info])
        else:
            return jsonify(data='error')

    def put(self, id):
        return {'aa': 'bb'}

    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('age', type=int, help='Rate cannot be converted')
        parser.add_argument('panel')
        args = parser.parse_args()
        return {'type': [args.age, args.panel]}


class Sv(Resource):
    def get(self, id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            sv_info = sample.sv_info
            return jsonify(data=[xx.json for xx in sv_info])
        else:
            return jsonify(data='error')


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
            print(check_type)
            check_info.gene_name = gene_name
            check_info.start_time = start_time
            check_info.end_time = end_time
            check_info.result = result
            check_info.note = note
            db.session.commit()
            print('update')
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
            print(type(check_info))
            return jsonify(data=[check_info.json])

    def delete(self, sample_id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id')
        args = parser.parse_args()
        id = args.id
        print('del', id)
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
                print('proc_time finish')
                
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
                print('proc_time finish')
            
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


class Sample_Panel(Resource):
    def get(self):
        pass


class Sample_Sate(Resource):
    def json(self):
        pass

    def get(self):
        pass


class Sample_Flowcell_Info(Resource):
    def get(self):
        return jsonify(data=[xx.json for xx in Sample_flowcell_info.query.all() if get_todo_sample(xx)])

    
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
  note_info.note_info
FROM sample_flowcell
  # 选择最近一次的下机信息
  INNER JOIN (SELECT
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
         concat(flowcell_id, '下机样本于 ', start_time, ' 申请进行', gene_name, ' ', check_type, '验证, ', end_time, ' 反馈结果：',
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
        (substring(sample_info.sample_id, 7, 1) = 'T' AND sample_info.sample_id LIKE 'LAA%')) AND
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
                'note_info': row[26]
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
            print(type(note_info))
            return jsonify(data=[note_info.json])

    def delete(self, sample_id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id')
        args = parser.parse_args()
        id = args.id
        print('del', id)
        note_info = Sample_note_info.query.get(id)
        db.session.delete(note_info)
        db.session.commit()
        return jsonify(data=[{'id': id}])
    

api.add_resource(SnpIndel, '/snpindel/<string:id>')
api.add_resource(Cnv, '/cnv/<string:id>')
api.add_resource(Sv, '/sv/<string:id>')
api.add_resource(Check_info, '/check/<string:sample_id>')
api.add_resource(Note_info, '/note/<string:sample_id>')
api.add_resource(Report_info, '/report/<string:sample_id>')
api.add_resource(Report_User, '/user/<string:role_name>')
api.add_resource(Sample_Flowcell_Info, '/sample_flowcell')
api.add_resource(Sample_Stat, '/sample_stat')