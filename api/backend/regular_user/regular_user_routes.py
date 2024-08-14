
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

user = Blueprint('user', __name__)


# GET /users
# [Emily-1]
@user.route('/users', methods=['GET'])
def get_all_users():
    current_app.logger.info('GET /users route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM users')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /users
# [Emily-1]
@user.route('/users', methods=['POST'])
def create_user():
    current_app.logger.info('POST /users route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', 
                   (data['username'], data['email'], data['password']))
    db.get_db().commit()
    the_response = make_response({'message': 'User created successfully'})
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

# GET /users/{id}
# [Emily-2]
@user.route('/users/<int:user_id>', methods=['GET'])
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
# [Emily-4]
@user.route('/influencers', methods=['GET'])
def get_all_influencers():
    current_app.logger.info('GET /influencers route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM influencers')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /influencers/{id}/notifications
# [Emily-4]
@user.route('/influencers/<int:influencer_id>/notifications', methods=['POST'])
def create_influencer_notification(influencer_id):
    current_app.logger.info(f'POST /influencers/{influencer_id}/notifications route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO notifications (influencer_id, message) VALUES (%s, %s)', 
                   (influencer_id, data['message']))
    db.get_db().commit()
    the_response = make_response({'message': 'Notification created successfully'})
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

# GET /influencers/{id}
# [Emily-4]
@user.route('/influencers/<int:influencer_id>', methods=['GET'])
def get_influencer_by_id(influencer_id):
    current_app.logger.info(f'GET /influencers/{influencer_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM influencers WHERE influencer_id = %s', (influencer_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /portfolios
# [Emily-2]
@user.route('/portfolios', methods=['GET'])
def get_all_portfolios():
    current_app.logger.info('GET /portfolios route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM portfolios')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /portfolios/{id}
# [Emily-1]
@user.route('/portfolios/<int:user_id>', methods=['POST'])
def create_portfolio(user_id):
    current_app.logger.info(f'POST /portfolios/{user_id} route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO portfolios (user_id, portfolio_name) VALUES (%s, %s)', 
                   (user_id, data['portfolio_name']))
    db.get_db().commit()
    the_response = make_response({'message': 'Portfolio created successfully'})
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

# GET /portfolios/{id}
# [Emily-2]
@user.route('/portfolios/<int:portfolio_id>', methods=['GET'])
def get_portfolio_by_id(portfolio_id):
    current_app.logger.info(f'GET /portfolios/{portfolio_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM portfolios WHERE portfolio_id = %s', (portfolio_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /stocks
# [Emily-2]
@user.route('/stocks', methods=['GET'])
def get_all_stocks():
    current_app.logger.info('GET /stocks route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM stocks')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /stocks/{id}
# [Emily-2]
@user.route('/stocks/<int:stock_id>', methods=['GET'])
def get_stock_by_id(stock_id):
    current_app.logger.info(f'GET /stocks/{stock_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM stocks WHERE stock_id = %s', (stock_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /notifications
# [Emily-3]
@user.route('/notifications', methods=['GET'])
def get_all_notifications():
    current_app.logger.info('GET /notifications route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM notifications')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
