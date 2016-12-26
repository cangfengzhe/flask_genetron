#coding=utf-8
import json

from flask import Flask, Blueprint, jsonify
from flask_restful import Api, Resource, url_for, reqparse
from . import api
from ..genetron.models import *




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
        sample = Sample_info.query.filter_by(sample_id=sample_id).first()
        
        if id !='':
            check_info = Sample_check_info.query.get(id)
            check_info.sample_id=sample.id
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
        else:
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
        
        
        
    
api.add_resource(SnpIndel, '/snpindel/<string:id>')
api.add_resource(Cnv, '/cnv/<string:id>')
api.add_resource(Check_info, '/check/<string:sample_id>')     