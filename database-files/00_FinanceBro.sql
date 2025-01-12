DROP SCHEMA IF EXISTS financeBrosDB;
CREATE SCHEMA financeBrosDB;
USE financeBrosDB;

CREATE TABLE IF NOT EXISTS users (
    user_id INT NOT NULL,
    SSN VARCHAR(255) UNIQUE NOT NULL,
    f_name VARCHAR(255) NOT NULL,
    l_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    banned BOOLEAN DEFAULT FALSE,
    phone VARCHAR(20) UNIQUE NOT NULL,
    DOB DATETIME NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS stock (
    ticker VARCHAR(10) NOT NULL,
    sharePrice DECIMAL(10, 2) NOT NULL ,
    stockName VARCHAR(255) NOT NULL,
    beta DECIMAL(50, 6) NOT NULL,
    PRIMARY KEY (ticker)
);

ALTER TABLE stock
ADD COLUMN historical_data JSON DEFAULT NULL,
ADD COLUMN trend_indicator DECIMAL(10,2) DEFAULT 0.00;

CREATE TABLE stock_historical_data (
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    close_price DECIMAL(10,2) NOT NULL,
    volume INT NOT NULL,
    PRIMARY KEY (ticker, date),
    FOREIGN KEY (ticker) REFERENCES stock(ticker)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DELIMITER //
CREATE FUNCTION calculate_trend_indicator(
    ticker_symbol VARCHAR(10)
) RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE trend DECIMAL(10,2);
    
    SELECT 
        ((last_price - first_price) / first_price) * 100 INTO trend
    FROM (
        SELECT 
            MAX(CASE WHEN rn = 1 THEN close_price END) as last_price,
            MAX(CASE WHEN rn = total THEN close_price END) as first_price
        FROM (
            SELECT 
                close_price,
                ROW_NUMBER() OVER (ORDER BY date DESC) as rn,
                COUNT(*) OVER () as total
            FROM stock_historical_data
            WHERE ticker = ticker_symbol
            ORDER BY date DESC
            LIMIT 30
        ) ranked_prices
    ) price_comparison;
    
    RETURN COALESCE(trend, 0);
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_trend_indicator
AFTER INSERT ON stock_historical_data
FOR EACH ROW
BEGIN
    UPDATE stock
    SET trend_indicator = calculate_trend_indicator(NEW.ticker)
    WHERE ticker = NEW.ticker;
END //
DELIMITER ;

CREATE TABLE IF NOT EXISTS personalPortfolio (
    portfolio_id INT NOT NULL,
    beta DECIMAL(50, 6) NOT NULL,
    liquidated_Value DECIMAL(20, 2) NOT NULL,
    P_L DECIMAL(10, 2) NOT NULL DEFAULT 0,
    user_id INT NOT NULL,
    PRIMARY KEY (portfolio_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS portfolioStocks (
    portfolio_id INT NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    primary key (portfolio_id, ticker),
    FOREIGN KEY (ticker)
        REFERENCES stock(ticker)
        ON UPDATE cascade ON DELETE cascade,
    FOREIGN KEY (portfolio_id)
        REFERENCES personalPortfolio(portfolio_id)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS verifiedPublicProfile (
    verified_user_id INT NOT NULL,
    kpi_id INT NOT NULL,
    photo_url VARCHAR(255),
    verified_username VARCHAR(255),
    biography varchar(2500),
    user_id INT NOT NULL,
    PRIMARY KEY (verified_user_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS verifiedPrivateProfile (
    verified_user_id INT NOT NULL,
    kpi_id INT,
    photo_url VARCHAR(255),
    verified_username VARCHAR(255),
    biography varchar(2500),
    user_id INT NOT NULL,
    PRIMARY KEY (verified_user_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS follows (
    following_id INT,
    follower_id INT,
    timestamp DATETIME,
    count INT,
    user_id INT,
    PRIMARY KEY (following_id, follower_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON UPDATE cascade ON DELETE cascade,
    FOREIGN KEY (follower_id)
        REFERENCES users(user_id)
        ON UPDATE cascade ON DELETE cascade,
    FOREIGN KEY (following_id)
        REFERENCES users(user_id)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS dashboardFeed (
    dashboard_feed_id INT NOT NULL,
    startTime DATETIME,
    endTime DATETIME,
    Kpi_id INT,
    updatedTime DATETIME DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    PRIMARY KEY (dashboard_feed_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT UNIQUE AUTO_INCREMENT,
    text TEXT,
    likes INT,
    timeCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    firstViewedAt DATETIME,
    lastViewedAt DATETIME,
    viewedAtResponseTime INT,
    user_id INT NOT NULL,
    PRIMARY KEY (notification_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS dashboardNotifications (
    notification_id INT NOT NULL,
    dashboard_feed_id INT AUTO_INCREMENT,
    PRIMARY KEY (notification_id, dashboard_feed_id),
    FOREIGN KEY (notification_id)
        REFERENCES notifications(notification_id)
        ON UPDATE cascade ON DELETE restrict,
    FOREIGN KEY (dashboard_feed_id)
        REFERENCES dashboardFeed(dashboard_feed_id)
        ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS userNotifications (
    user_id INT NOT NULL,
    notification_id INT NOT NULL,
    PRIMARY KEY (user_id, notification_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON UPDATE cascade ON DELETE restrict,
    FOREIGN KEY (notification_id)
        REFERENCES notifications(notification_id)
        ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS userMetrics (
    user_metric_ID INT NOT NULL,
    dmStartTime DATETIME,
    dmEndTime DATETIME,
    mStartTime DATETIME,
    mEndTime DATETIME,
    activeUsers INT,
    user_id INT NOT NULL,
    PRIMARY KEY (user_metric_ID),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id INT NOT NULL,
    f_name VARCHAR(255),
    l_name VARCHAR(255),
    city VARCHAR(255),
    start_date DATETIME,
    DOB DATETIME,
    user_metric_id INT NOT NULL,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (user_metric_id)
        REFERENCES userMetrics(user_metric_ID)
);


TRUNCATE TABLE stock_historical_data;

DELIMITER //
CREATE FUNCTION IF NOT EXISTS generate_price(
    base_price DECIMAL(10,2),
    beta DECIMAL(10,4),
    days_ago INT
) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE volatility DECIMAL(10,4);
    DECLARE random_factor DECIMAL(10,4);
    DECLARE price_change DECIMAL(10,4);
    
    SET volatility = beta * 0.01; 
    SET random_factor = (RAND() - 0.5) * 2;
    SET price_change = 1 + (random_factor * volatility * (1 - (days_ago / 60)));
    
    RETURN ROUND(base_price * price_change, 2);
END //
DELIMITER ;

DELIMITER //
CREATE FUNCTION IF NOT EXISTS generate_volume(
    base_price DECIMAL(10,2),
    beta DECIMAL(10,4)
)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE base_volume INT;
    DECLARE random_factor DECIMAL(10,4);
    
    SET base_volume = FLOOR(1000000 / (base_price * 0.1));
    SET random_factor = 0.5 + (RAND() * 1.5);
    
    RETURN FLOOR(base_volume * random_factor);
END //
DELIMITER ;

INSERT INTO stock_historical_data (ticker, date, close_price, volume)
SELECT 
    s.ticker,
    d.date,
    generate_price(s.sharePrice, s.beta, DATEDIFF(CURRENT_DATE, d.date)),
    generate_volume(s.sharePrice, s.beta)
FROM stock s
CROSS JOIN (
    SELECT DATE_SUB(CURRENT_DATE, INTERVAL n DAY) as date
    FROM (
        SELECT @row := @row + 1 as n
        FROM (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) t1
        CROSS JOIN (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2) t2
        CROSS JOIN (SELECT @row := -1) t3
        ORDER BY n
    ) numbers
    WHERE n <= 30
) d;

DROP FUNCTION IF EXISTS generate_price;
DROP FUNCTION IF EXISTS generate_volume;

UPDATE stock s
INNER JOIN (
    SELECT ticker, close_price
    FROM stock_historical_data
    WHERE date = (SELECT MAX(date) FROM stock_historical_data)
) h ON s.ticker = h.ticker
SET s.sharePrice = h.close_price;