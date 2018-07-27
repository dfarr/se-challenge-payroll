
import os
import uuid
import tasks
import sqlite3

from flask import Flask, request, jsonify, send_from_directory
app = Flask(__name__)


###################################################################################################
## Static frontend
###################################################################################################

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


###################################################################################################
## API
###################################################################################################

@app.route('/api/payments')
def api():

    conn = sqlite3.connect('db.db')

    c = conn.cursor()

    result = [ {'report_id': report_id, 'employee_id': employee_id, 'period': period, 'amount': amount} for report_id, employee_id, period, amount in c.execute('SELECT * FROM report') ]

    conn.close()

    return jsonify(result)


###################################################################################################
## Handle report upload
###################################################################################################

@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return 'Bad Request', 400


    ###################################################################################################
    ## Save file
    ###################################################################################################

    path = os.path.join('./uploads/', '{}.csv'.format(uuid.uuid4()))

    request.files['file'].save(path)


    ###################################################################################################
    ## Execute workflow
    ###################################################################################################

    workflow = tasks.Load(tasks.Transform(tasks.Extract(path)))

    result, status = workflow.execute()

    return (result, 200) if status else (result, 500)

