from flask import current_app as app, jsonify, render_template,  request, send_file
from flask_security import auth_required, verify_password, hash_password
from applications.models import db
from datetime import datetime
from celerydir.tasks import create_csv

from celery.result import AsyncResult
from flask_cors import CORS  # Import flask_cors


datastore = app.security.datastore
cache = app.cache

@app.get('/cache')
@cache.cached(timeout = 5)
def cache():
    return {'time' : str(datetime.now())}




CORS(app, origins="http://localhost:5173") 
@app.route('/create-csv', methods=['POST'])
def createCSV():
    try:
        task = create_csv.delay()
        
        return jsonify({'task_id': task.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-csv/<id>', methods=['GET'])
def getCSV(id):
    try:
        result = AsyncResult(id)
        if result.ready():
            return send_file(f'./celerydir/user-downloads/{result.result}', as_attachment=True)
        else:
            return jsonify({'message': 'Task not ready yet'}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500



    
