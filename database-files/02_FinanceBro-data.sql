SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

USE `financeBrosDB`;

INSERT INTO users (user_id, SSN, f_name, l_name, username, password, email, verified,banned, phone, DOB)
VALUES (1, '123-11-2222', 'Bryan', 'Guen', 'bryanguen', '123', 'bguen@gmail.com', TRUE, FALSE, '857-250-1814', '2004-10-13 11:52:43'),
       (2, '213-22-3333', 'Ethan', 'Xin', 'ethanxin', 'abc', 'exin@hotmail.com', FALSE, FALSE, '508-300-5430', '2004-05-13 08:43:20'),
       (3, '312-33-4444', 'Eitan', 'Berenfield', 'eitanberenfield', '234', 'eberen@outlook.com', FALSE, FALSE, '781-752-6078', '2004-12-21 07:02:45'),
       (4, '242-44-5555', 'John', 'Summit', 'johnsummit', '542', 'jsummit@outlook.com', TRUE, FALSE,  '781-787-6328', '2000-10-23 09:32:43');

INSERT INTO stock (ticker, sharePrice, stockName, beta)
VALUES ('AAPL', 136.57, 'Apple', 1.25),
       ('NVDA', 104.43, 'Nvidia', 4.63),
       ('TSLA', 879.75, 'Tesla', 7.592);

INSERT INTO personalPortfolio (portfolio_id, beta, liquidated_Value, P_L, user_id)
VALUES (10, 1.043, 1234234.43, 655454.63, 1),
       (20, 3.34, 155060.50, 7423.34, 2),
       (30, 4.592, 23030.76, 3234.76, 3);

INSERT INTO portfolioStocks (portfolio_id, ticker)
VALUES (10, 'AAPL'),
       (20, 'NVDA'),
       (30, 'TSLA');

INSERT INTO verifiedPublicProfile (verified_user_id, kpi_id, photo_url, verified_username, biography, user_id)
VALUES (100, 101, 'face.jpg', 'bryanguen', 'I am an experienced trader.', 1),
       (200, 102, 'headShot.jpg', 'johnsummit', 'I love trading stocks everyday', 4),
       (300, 103, 'fancyPic.jpg', 'eitanberenfield', 'Actively trading stocks right now', 3);

INSERT INTO verifiedPrivateProfile (verified_user_id, kpi_id, photo_url, verified_username, biography, user_id)
VALUES (100, 101, 'face.jpg', 'bryanguen', 'I am an experienced trader.', 1),
       (200, 102, 'headShot.jpg', 'johnsummit', 'I love trading stocks everyday', 4),
       (300, 103, 'fancyPic.jpg', 'eitanberenfield', 'Actively trading stocks right now', 3);

INSERT INTO follows (following_id, follower_id, timestamp, count, user_id)
VALUES (1, 2, CURRENT_TIMESTAMP, 1, 1),
       (2, 3, CURRENT_TIMESTAMP, 1, 2),
       (3, 1, CURRENT_TIMESTAMP, 1, 3);

INSERT INTO dashboardFeed (dashboard_feed_id, startTime, endTime, Kpi_id, user_id)
VALUES (1000, '2024-08-09 08:23:00', '2024-08-09 08:24:32', 301, 1),
       (2000, '2024-08-09 09:00:00', '2024-08-09 09:10:11', 302, 2),
       (3000, '2024-08-09 10:00:00', '2024-08-09 10:01:23', 303, 3);

INSERT INTO notifications (notification_id, text, likes, timeCreated, firstViewedAt, lastViewedAt, viewedAtResponseTime, user_id)
VALUES (1, 'I just bought AAPL stock and has risen by 5.6% today', 100, '2024-08-09 12:00:00', '2024-08-09 12:05:00', '2024-08-09 12:15:00', '2024-08-09 12:05:00', 1),
       (2, 'I just sold NVDA stock and has dropped by 3.2%', 150, '2024-07-09 13:00:00', '2024-08-09 13:07:00', '2024-08-09 13:20:00', '2024-08-09 13:07:00', 3),
       (3, 'I sold TSLA stock after it risen by 1.34%', 200, '2024-08-09 14:00:00', '2024-08-09 14:10:00', '2024-08-09 14:25:00', '2024-08-09 14:10:00', 4);

INSERT INTO dashboardNotifications (notification_id, dashboard_feed_id)
VALUES (1, 1000),
       (2, 2000),
       (3, 3000);

INSERT INTO userNotifications (user_id, notification_id)
VALUES (1, 1),
       (2, 2),
       (3, 3);

INSERT INTO userMetrics (user_metric_ID, dmStartTime, dmEndTime, mStartTime, mEndTime, activeUsers, user_id)
VALUES (1, '2024-08-09 08:00:00', '2024-08-09 16:00:00', '2024-08-09 12:00:00', '2024-08-09 14:00:00', 150, 1),
       (2, '2024-08-09 09:00:00', '2024-08-09 17:00:00', '2024-08-09 13:00:00', '2024-08-09 15:00:00', 200, 2),
       (3, '2024-08-09 10:00:00', '2024-08-09 18:00:00', '2024-08-09 14:00:00', '2024-08-09 16:00:00', 250, 3);

INSERT INTO employees (employee_id, f_name, l_name, city, start_date, DOB, user_metric_id)
VALUES (1, 'Luke', 'Skywalker', 'New York', '2024-01-01 00:00:00', '2000-01-01 00:00:00', 1),
       (2, 'John', 'Wick', 'Los Angeles', '2024-02-01 00:00:00', '2001-05-15 00:00:00', 2),
       (3, 'Tiger', 'Woods', 'Chicago', '2024-02-04 00:00:00', '2004-12-25 00:00:00', 3);

-- User story 1 of persona #1 has user_id = 1
SELECT s.ticker, s.beta, s.sharePrice
From stock s
ORDER BY s.beta ASC
LIMIT 1;

-- User story 2 of persona #1 has user_id = 1
SELECT ps.ticker, p.P_L, p.liquidated_Value
FROM personalPortfolio p
     JOIN portfolioStocks ps ON ps.portfolio_id = p.portfolio_id
WHERE p.user_id = 1;

-- User story 3 of persona #1 has user_id = 1
SELECT n.text
FROM notifications n
WHERE DATE(n.timeCreated) = CURDATE();

-- User story 4 of persona #1 has user_id = 2 which should see influencer user_id1
SELECT *
FROM verifiedPublicProfile p
     JOIN follows f on p.user_id = f.user_id
WHERE f.follower_id = 2;

-- -----------------------------------
-- User story 1 of persona #2
INSERT INTO notifications (notification_id, text, likes, timeCreated,
                           firstViewedAt, lastViewedAt, viewedAtResponseTime, user_id)
VALUES (7, 'I just bought American Airlines (AAL) and has risen by 15.2% today', 0,
        '2024-08-09 07:00:00', '2024-08-09 07:05:00', '2024-08-09 12:15:00', '2024-07-09 12:05:00', 1);

-- User story 2 of persona #2 user_id = 1
UPDATE notifications
SET text = 'I just sold AAPL stock and has risen by 5.6% today'
WHERE user_id = 1;

-- User story 3 of persona #2 user_id = 1
UPDATE verifiedPrivateProfile
SET biography = 'Hey! Click this link: "mylink.com", where I offer personal videos to teach my trading strategy!'
WHERE user_id = 1;

-- User story 4 of persona #2 user_id = 3
SELECT f.count
FROM follows f
WHERE f.user_id = 3;

-- -----------------------------------
-- User story 1 of persona #3
SELECT um.dmStartTime, um.dmEndTime, um.user_metric_ID, um.user_id
FROM userMetrics um;
-- User story 2 of persona #3
SELECT *
FROM userMetrics um
     JOIN notifications n ON um.user_id = n.user_id
     JOIN follows f ON f.following_id = n.user_id
ORDER BY likes, timeCreated;

-- User story 3 of persona #3
SELECT *
FROM personalPortfolio
WHERE liquidated_Value > 20000 AND P_L >= (liquidated_Value * .15)
ORDER BY P_L DESC;

-- User story 4 of persona #3
UPDATE users
SET banned = true
WHERE user_id = 4;