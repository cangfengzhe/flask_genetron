from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from models import *
from datetime import datetime

'''
shell time: 
   date "+%Y-%m-%d %H:%M:%S"
'''

@genetron.route('/api')
def api():
    """
    
    """
    api_type = request.args.get('type')
    flowcell_id = request.args.get('flowcell')
    samples = request.args.get('samples')
    dt = request.args.get('dt', datetime.now().strftime('%Y-%m-%d %H%M%S'))
    if api_type == 'sj_time':
        sj_time = request.args.get('sj_time')
        if not sj_time:
            return jsonify(status='error', info='sj_time is null')
        sj_time = datetime.strptime(sj_time, '%Y-%m-%d_%H:%M:%S') # 传入时间使用 %Y-%m-%d_%H:%M:%S
        flowcell = Flowcell_info.query.filter_by(flowcell_id=flowcell_id)
        if flowcell.count()==1:
            flowcell
            
            
        flowcell = Flowcell_info(flowcell_id=flowcell_id,sj_time=sj_time)
        
def flowcell_time('/api/flowcell')
    pass