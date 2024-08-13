########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, jsonify, make_response
import json
from backend.db_connection import db

dataAnalyst = Blueprint('dataAnalyst', __name__)

@dataAnalyst.route('/dataAnalyst', methods=['GET'])
def get_all_dataAnalyst():
    cursor = db.get_db().cursor()
    the_query = """
    SELECT * 
    FROM employees
    """
    cursor.execute(the_query)
    rows = cursor.fetchall()

    # Get the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Convert the rows to a list of dictionaries
    theData = [dict(zip(column_names, row)) for row in rows]

    # Convert the data to JSON format
    data_json = json.dumps(theData)
    
    # Create a response object
    the_response = make_response(data_json)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

    
