import datetime
from flask import jsonify, request
from flask import render_template
from collections import defaultdict
from models import *
from . import genetron
from flask_login import login_required

def get_request_data(form):
    '''
    return dict list with data from request.form

    :param form: MultiDict from `request.form`
    :rtype: {id1: {field1:val1, ...}, ...} [fieldn and valn are strings]
    '''

    # request.form comes in multidict [('data[id][field]',value), ...]

    # fill in id field automatically
    data = defaultdict(lambda: {})
    for formkey in form.keys():
        if formkey == 'action':
            data['type'] = form['action']
            # print(data['type'])
            continue
        datapart, idpart, fieldpart = formkey.split('[')
        # if datapart != 'data': raise ParameterError, "invalid input in request: {}".format(formkey)

        idvalue = int(idpart[0:-1])
        fieldname = fieldpart[0:-1]

        data[idvalue][fieldname] = form[formkey]
        data[idvalue]['DT_RowId'] = idvalue
    # return decoded result
    return data




@genetron.route('/', methods=['GET', 'POST'])
@genetron.route('/index', methods=['GET', 'POST'])
@genetron.route('/patient')
def patient():
    return render_template('genetron/patient.html')


@genetron.route('/patient_table')
def patient_table():
    data = Patient.query.all()
    return jsonify(
        data=[i.json for i in data]
    )


@genetron.route('/patientresponse', methods=['GET', 'POST'])
def patientresponse():
    form_data = get_request_data(request.form)
    var = [form_data[x] for x in form_data if x != 'type'][0]
    DT_RowId = var['DT_RowId']
    print(var)
    if form_data['type'] == 'remove':
        patient = Patient.query.filter_by(id=var['DT_RowId']).first()
        db.session.delete(patient)
        db.session.commit()
        return jsonify(data=[])
    if form_data['type'] == 'create':
        var.pop('DT_RowId')
        print('dead_time', var['dead_line'])
        if not var['start_time'] == u'':
            var['start_time'] = datetime.datetime.strptime(var['start_time'], '%Y-%m-%d').date()
        if not var['dead_line'] == u'':
            var['dead_line'] = datetime.datetime.strptime(var['dead_line'], '%Y-%m-%d').date()
        if 'bioinfo' in var:
            if var['bioinfo']=='true':
                var['bioinfo']=True
            else:
                var['bioinfo']=False
        if 'is_finish' in var:
            if var['is_finish']=="true":
                var['is_finish']=True
            else:
                var['is_finish']=False

        patient = Patient(**var)
        db.session.add(patient)
        db.session.flush()
        db.session.refresh(patient)
        DT_RowId = patient.id
        var['DT_RowId'] = patient.id
    elif form_data['type'] == 'edit':
        patient = Patient.query.filter_by(id=var['DT_RowId']).first()
        # print(var['start_time'])
        if 'start_time' in var:
            var['start_time'] = datetime.datetime.strptime(var['start_time'], '%Y-%m-%d').date()
        if 'dead_line' in var:
            var['dead_line'] = datetime.datetime.strptime(var['dead_line'], '%Y-%m-%d').date()
            print(var['dead_line'])
	if 'bioinfo' in var:
            if var['bioinfo']=='true':
		var['bioinfo']=True
	    else:
		var['bioinfo']=False
	if 'is_finish' in var:
	    if var['is_finish']=="true":
		var['is_finish']=True
	    else:
		var['is_finish']=False
        patient.from_dict(var)
        print('dead_line', patient.dead_line)
        print('age', patient.age)
    db.session.commit()
    dt = Patient.query.filter_by(id=DT_RowId).first()
    return jsonify(data=[dt.json])
