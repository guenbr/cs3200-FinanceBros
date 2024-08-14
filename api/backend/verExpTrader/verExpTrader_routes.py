from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

experiencedTrader = Blueprint('experiencedTrader', __name__)

# GET /notifications
@experiencedTrader.route('/notifications', methods=['GET'])
def get_all_notifications():
    current_app.logger.info('GET /notifications route')
    user_id = request.args.get('user_id')  # Ensure that you get the correct user_id
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM notifications')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /notifications
@experiencedTrader.route('/notifications', methods=['POST'])
def create_notification():
    current_app.logger.info('POST /notifications route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute(
        'INSERT INTO notifications (notification_id, text, likes, timeCreated, firstViewedAt, lastViewedAt, viewedAtResponseTime, user_id) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
        (data['notification_id'], data['text'], data['likes'], data['timeCreated'], data['firstViewedAt'], data['lastViewedAt'], data['viewedAtResponseTime'], data['user_id'])
    )
    db.get_db().commit()
    return jsonify({'message': 'Notification created successfully'}), 201

# PUT /notifications/{id}
@experiencedTrader.route('/notifications/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
    current_app.logger.info(f'PUT /notifications/{notification_id} route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute(
        'UPDATE notifications SET text = %s WHERE notification_id = %s AND user_id = %s',
        (data['text'], notification_id, data['user_id'])
    )
    db.get_db().commit()
    return jsonify({'message': 'Notification updated successfully'}), 200

# GET /follows
@experiencedTrader.route('/follows', methods=['GET'])
def get_all_followers():
    current_app.logger.info('GET /follows route')
    user_id = request.args.get('user_id')  # Ensure that you get the correct user_id
    cursor = db.get_db().cursor()
    cursor.execute('SELECT follower_id FROM follows WHERE following_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /users/{id}
@experiencedTrader.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    current_app.logger.info(f'GET /users/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT user_id, f_name, l_name, email, username FROM users WHERE user_id = %s', (user_id,))
    theData = cursor.fetchone()  # Fetch one since user_id is unique
    if theData:
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
        the_response.mimetype = 'application/json'
    else:
        the_response = make_response(jsonify({'message': 'User not found'}))
        the_response.status_code = 404
        the_response.mimetype = 'application/json'
    return the_response

# PUT /users/{id}
@experiencedTrader.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    current_app.logger.info(f'PUT /users/{user_id} route')
    data = request.get_json()
    cursor = db.get_db().cursor()
    cursor.execute(
        'UPDATE users SET bio = %s WHERE user_id = %s',
        (data['bio'], user_id)
    )
    db.get_db().commit()
    return jsonify({'message': 'User updated successfully'}), 200

# GET /stocks
@experiencedTrader.route('/stocks', methods=['GET'])
def get_all_stocks():
    current_app.logger.info('GET /stocks route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT ticker, stockName, sharePrice, beta FROM stock')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
