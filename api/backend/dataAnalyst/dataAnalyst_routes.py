
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

dataAnalyst = Blueprint('dataAnalyst', __name__)


# GET /user

@dataAnalyst.route('/users', methods=['GET'])
def get_all_users():
    current_app.logger.info('GET /users route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM users')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /users{id}

@dataAnalyst.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    current_app.logger.info(f'GET /users/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /influencers

@dataAnalyst.route('/influencers', methods=['GET'])
def get_all_influencers():
    current_app.logger.info('GET /influencers route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM verifiedPublicProfile')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /influencers/{id}

@dataAnalyst.route('/influencers/<verified_user_id>', methods=['GET'])
def get_influencer_by_id(verified_user_id):
    current_app.logger.info(f'GET /influencers/{verified_user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM verifiedPublicProfile WHERE verified_user_id = %s', (verified_user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /portfolios

@dataAnalyst.route('/portfolios', methods=['GET'])
def get_all_portfolios():
    current_app.logger.info('GET /portfolios route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM personalPortfolio')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /portfolios/{id}

@dataAnalyst.route('/portfolios/<portfolio_id>', methods=['GET'])
def get_portfolio_by_id(portfolio_id):
    current_app.logger.info(f'GET /portfolios/{portfolio_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM personalPortfolio WHERE portfolio_id = %s', (portfolio_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /stocks

@dataAnalyst.route('/stocks', methods=['GET'])
def get_all_stocks():
    current_app.logger.info('GET /stocks route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT dmStartTime, dmEndTime, user_metric_ID, user_id FROM userMetrics WHERE user_id = %s', (user_id,))
    cursor.execute('SELECT * FROM stock')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



# GET /stocks/{id}

@dataAnalyst.route('/stocks/<ticker>', methods=['GET'])
def get_stock_by_id(ticker):
    current_app.logger.info(f'GET /stock/{ticker} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM stock WHERE ticker = %s', (ticker,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /notifications

@dataAnalyst.route('/notifications/<notification_id>', methods=['GET'])
def get_notification_by_id(notification_id):
    current_app.logger.info('GET /notifications/{notification_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM notifications WHERE notification_id = %s', (notification_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Delete /users/{id}

@dataAnalyst.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    current_app.logger.info(f'DELETE /users/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
    db.get_db().commit()
    the_response = make_response({'message': 'User deleted successfully'})
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
