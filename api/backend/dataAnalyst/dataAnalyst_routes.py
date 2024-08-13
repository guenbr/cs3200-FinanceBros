########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

dataAnalyst = Blueprint('dataAnalyst', __name__)

@dataAnalyst.route('/dataAnalyst', methods=['GET'])
def get_all_dataAnalyst():
    current_app.logger.info('GET /dataAnalyst route')
    cursor = db.get_db().cursor()
    # the_query = '''
    # SELECT * 
    # FROM stock
    # '''
    cursor.execute('select * from stock')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response