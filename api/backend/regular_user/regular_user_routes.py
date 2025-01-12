from flask import Blueprint, request, jsonify, make_response, current_app
from backend.stock_analyzer import StockAnalyzer
import json
from backend.db_connection import db

user = Blueprint('user', __name__)

# GET /users/<username>
# [Emily-4]
#This function displays the specific user_id of the given username that
# Emily wants to view.
@user.route('/users/<username>', methods=['GET'])
def get_username_by_id(username):
    current_app.logger.info(f'GET /users/{username} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# GET /influencers
# [Emily-4]
# This function gets all usernames of all verified users in the database.
@user.route('/influencers', methods=['GET'])
def get_all_influencers():
    current_app.logger.info('GET /influencers route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT username FROM users WHERE verified = True')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /influencers/{id}
# [Emily-4]
# This returns the verified public profile of the selected verified user, Emily selects.
@user.route('/influencers/<username>', methods=['GET'])
def get_influencer_by_username(username):
    current_app.logger.info(f'GET /influencers/{username} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT verified_username, biography, photo_url\
                    FROM verifiedPublicProfile WHERE verified_username = %s', (username,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /portfolios/{id}
# [Emily-2]
# This function returns all portfolios statistics of a specific user. 
@user.route('/myportfolios/<int:user_id>', methods=['GET'])
def get_my_portfolios(user_id):
    current_app.logger.info(f'GET /personalPortfolio/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT P_L, liquidated_Value, beta FROM personalPortfolio WHERE user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /portfolios/{id}
# [Emily-2]
# This returns all stocks in the portfolio of the specific user_id
@user.route('/portfolios_stock/<int:user_id>', methods=['GET'])
def get_portfolios_userID(user_id):
    current_app.logger.info(f'GET /personalPortfolio/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT s.ticker, s.sharePrice, s.stockName, s.beta FROM users u JOIN personalPortfolio ps ON u.user_id = ps.user_id JOIN portfolioStocks p ON ps.portfolio_id = p.portfolio_id JOIN stock s ON s.ticker = p.ticker WHERE u.user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /stocks
# [Emily-2]
# Returns all stocks a user can add to their portfolio.
@user.route('/stocks', methods=['GET'])
def get_all_stocks():
    current_app.logger.info('GET /stocks route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM stock')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET /recStocks
# [Emily-2]
# Returns top 5 rec. stocks that the stock has the lowest beta of all stocks.
@user.route('/recStocks', methods=['GET'])
def recStocks():
    current_app.logger.info('GET /stocks route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM stock ORDER BY beta LIMIT 5')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# GET notifications/{user_id}
# [Emily-3]
# This function returns all notifications from the users followed by specfic user_id
@user.route('/notifications/<int:user_id>', methods=['GET'])
def get_notifications_for_user(user_id):
    current_app.logger.info(f'GET /notifications/{user_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT n.user_id AS verifiedUser, n.text AS Post, n.likes, n.timeCreated FROM users u JOIN dashboardFeed df ON u.user_id = df.user_id JOIN dashboardNotifications dn ON dn.dashboard_feed_id = df.dashboard_feed_id JOIN notifications n ON n.notification_id = dn.notification_id WHERE u.user_id = %s', (user_id,))
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /follow/{user_id}
# [Emily-4]
# This function allows the user to follow another verified user by verfied users' user_id.
@user.route('/follow/<int:user_id>/<int:following_id>', methods=['POST'])
def follow_user(user_id, following_id):
    current_app.logger.info(f'POST /follow/{user_id}/{following_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO follows (follower_id, following_id) VALUES (%s, %s)', (9379, following_id))
    response = make_response({'message': f'User {user_id} followed {following_id} successfully'})
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# GET /stocks
# [Emily-2]
# This functions allows the user to click the TICKER name they want to add to their portfolio.
@user.route('/getTicker', methods=['GET'])
def get_all_ticker():
    current_app.logger.info('GET /getTicker route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT ticker FROM stock')
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# POST /stocks
# [Emily-1]
# This function allows the user to INSERT a specfic stock in their portfolio_id by ticker name.
@user.route('/addStockToPortfolio/<int:portfolio_id>/<string:ticker>', methods=['POST'])
def addStock(portfolio_id, ticker):
    current_app.logger.info(f'POST /addStock route for portfolio_id: {portfolio_id} and ticker: {ticker}')
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO portfolioStocks (portfolio_id, ticker) VALUES (%s, %s)', (portfolio_id, ticker))
    db.get_db().commit()
    response = make_response({'message': f'You added {ticker} to portfolio {portfolio_id}!'})
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# GET /stock/analysis/{ticker}
# Returns comprehensive analysis for a specific stock
@user.route('/stock/analysis/<ticker>', methods=['GET'])
def get_stock_analysis(ticker):
    current_app.logger.info(f'GET /stock/analysis/{ticker} route')
    analyzer = StockAnalyzer(db.get_db())
    
    try:
        analysis = analyzer.analyze_stock(ticker)
        if "error" in analysis:
            return jsonify({"error": analysis["error"]}), 404
            
        the_response = make_response(jsonify(analysis))
        the_response.status_code = 200
        the_response.mimetype = 'application/json'
        return the_response
        
    except Exception as e:
        current_app.logger.error(f"Error analyzing stock {ticker}: {e}")
        return jsonify({"error": "Failed to analyze stock"}), 500

# GET /stock/recommendations
# Returns top stock recommendations based on analysis
@user.route('/stock/recommendations', methods=['GET'])
def get_stock_recommendations():
    current_app.logger.info('GET /stock/recommendations route')
    analyzer = StockAnalyzer(db.get_db())
    
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT ticker FROM stock')
        stocks = cursor.fetchall()
        
        recommendations = []
        for stock in stocks:
            analysis = analyzer.analyze_stock(stock['ticker'])
            if "error" not in analysis and analysis["confidence"] > 70:
                recommendations.append(analysis)
                
        # Sort by confidence
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Return top 5 recommendations
        the_response = make_response(jsonify(recommendations[:5]))
        the_response.status_code = 200
        the_response.mimetype = 'application/json'
        return the_response
        
    except Exception as e:
        current_app.logger.error(f"Error getting stock recommendations: {e}")
        return jsonify({"error": "Failed to get recommendations"}), 500