#coding=utf-8


from flask import Flask, Blueprint, jsonify, make_response
from flask_restful import Api, Resource, url_for, reqparse
from json import dumps
import json

from . import api
from ..genetron.models import *
from ..models import *
from ..tips import *


class SnpIndel(Resource):
    def get(self,id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            snp_indel_info = sample.snp_indel_info
            return jsonify(data=[xx.json for xx in snp_indel_info])
        else:
            return jsonify(data='error')

    
class Cnv(Resource):
    def get(self,id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            cnv_info = sample.cnv_info
            return jsonify(data=[xx.json for xx in cnv_info])
        else:
            return jsonify(data='error')

    def put(self, id):
        return {'aa':'bb'}

    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('age', type=int, help='Rate cannot be converted')
        parser.add_argument('panel')
        args = parser.parse_args()
        return {'type':[args.age, args.panel]}
        

        
class Sv(Resource):
    def get(self,id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            sv_info = sample.sv_info
            return jsonify(data=[xx.json for xx in sv_info])
        else:
            return jsonify(data='error')
 

class Check_info(Resource):
    def get(self,sample_id):
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
        id=args.id
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
        
        if id !='':
            # // update
            check_info = Sample_check_info.query.get(id)
            check_info.sample_id=sample.id
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
            check_info = Sample_check_info(sample_id=sample.id, flowcell_id=flowcell_id, panel=panel, check_type=check_type, gene_name=gene_name,
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
        return jsonify(data=[{'id':id}])
 

class Report_info(Resource):
    def get(self,sample_id):
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
        parser.add_argument('writer', type=str, help='gene_name')
        parser.add_argument('report_time', type=str, help='start_time')
        parser.add_argument('checker', type=str, help='end_time')
        parser.add_argument('check_time', type=str, help='result')
        parser.add_argument('finish_time', type=str, help='result')
        parser.add_argument('note', type=str, help='note')
        # parser.add_argument('callback', type=str, help='note')
        args = parser.parse_args()
        id=args.id
        panel = args.panel
        start_time = args.start_time
        writer = args['writer']
        report_time = args.report_time
        checker = args['checker']
        check_time = args.check_time
        finish_time = args.finish_time
        note = args.note
        # callback=args.callback
        sample = Sample_info.query.filter_by(sample_id=sample_id).first()
        
        if id !='':
            # // update
            report_info = Sample_report_info.query.get(id)
            report_info.sample_id=sample.id
            report_info.panel = panel
            report_info.start_time = strptime(start_time)
            report_info.report_user_id = writer #User.query.filter_by(username=writer).first().id
            report_info.report_time = strptime(report_time)
            report_info.check_user_id = checker #User.query.filter_by(username=checker).first().id
            report_info.check_time = strptime(check_time)
            report_info.finish_time = strptime(finish_time)
            report_info.note = note
            db.session.commit()
            return jsonify(data=[report_info.json])
            # return jsonify(data={})
            # return '{}'
        else:
            # create
            report_info = Sample_report_info()
            report_info.sample_id=sample.id
            report_info.panel = panel
            report_info.start_time = strptime(start_time)
            report_info.report_user_id = writer #User.query.filter_by(username=writer).first().id
            report_info.report_time = strptime(report_time)
            report_info.check_user_id = checker # User.query.filter_by(username=checker).first().id
            report_info.check_time = strptime(check_time)
            report_info.finish_time = strptime(finish_time)
            report_info.note = note
            db.session.add(report_info)
            db.session.commit()
            print(type(report_info))
            return jsonify(data=[report_info.json])
    
    def delete(self, sample_id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='id')
        args = parser.parse_args()
        id = args.id
        print('del', id)
        report_info = Sample_report_info.query.get(id)
        db.session.delete(report_info)
        db.session.commit()
        return jsonify(data=[{'id':id}])       
        

class Report_User(Resource):
    def get(self, role_name):
        role = Role.query.filter_by(name=role_name).first()
        users =  role.users
        response = make_response(dumps([xx.json for xx in users]))                                      
        response.headers['Content-Type'] = 'application/json'            
        return response

class Sample_Panel(Resource):
    
    def get(self):
        pass
    
api.add_resource(SnpIndel, '/snpindel/<string:id>')
api.add_resource(Cnv, '/cnv/<string:id>')
api.add_resource(Sv, '/sv/<string:id>')
api.add_resource(Check_info, '/check/<string:sample_id>')  
api.add_resource(Report_info, '/report/<string:sample_id>')
api.add_resource(Report_User, '/user/<string:role_name>')
