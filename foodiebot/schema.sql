DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS custom_black_list;
DROP TABLE IF EXISTS custom_food;
DROP TABLE IF EXISTS response;




CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  email TEXT UNIQUE NOT NULL,
  password TEXT,
  gender TEXT,
  birthday TEXT
);


INSERT INTO user(email,gender, birthday) VALUES ('guest', 'guest','guest');





CREATE TABLE custom_food(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT  NOT NULL,
    singlepeople INTEGER ,
    manypeople INTEGER ,
    cheap INTEGER ,
    expensive INTEGER ,
    breakfast INTEGER,
    lunch INTEGER ,
    dinner INTEGER ,
    night INTEGER ,
    hot INTEGER ,
    cold INTEGER,
    user_id INTEGER NOT NULL,
    activate INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (id)
);



INSERT INTO custom_food (category, singlepeople, manypeople, cheap, expensive, breakfast, lunch, dinner, night, hot, cold, user_id, activate)
VALUES
('牛肉麵',  1, 0, 1, 0, 0, 1, 1, 1, 1, 1,1,1),
('炒飯',    1, 0, 1, 0, 0, 1, 1, 1, 1, 1,1,1),
('早餐',    1, 0, 1, 0, 1, 0, 0, 0, 1, 1,1,1),
('鍋燒麵',  1, 0, 1, 0, 0, 1, 1, 1, 1, 1,1,1),
('燒臘',    1, 0, 1, 0, 0, 1, 1, 0, 1, 1,1,1),
('永和豆漿', 1, 0, 1, 0, 1, 0, 0, 1, 1, 1,1,1),
('咖哩',    1, 1, 1, 1, 0, 1, 1, 0, 1, 1,1,1),
('水餃',    1, 0, 1, 0, 0, 1, 1, 1, 1, 1,1,1),
('鍋貼',    1, 0, 1, 0, 0, 1, 1, 1, 1, 1,1,1),
('熱炒',    0, 1, 0, 1, 0, 0, 1, 1, 1, 1,1,1),
('豬腳飯',  1, 0, 1, 0, 0, 1, 1, 1, 1, 1,1,1),
('拉麵',    1, 1, 1, 1, 0, 1, 1, 1, 1, 1,1,1),
('乾麵',    1, 0, 1, 0, 0, 1, 1, 1, 1, 1,1,1),
('海南雞',  1, 0, 1, 0, 0, 1, 1, 1,  1, 1,1,1),
('速食',    1, 0, 1, 0, 0, 1, 1, 1,  1, 1,1,1),
('涼麵',    1, 0, 1, 0, 0, 1, 1, 1,  1, 0,1,1),
('臭臭鍋',  1, 0, 1, 0, 0, 1, 1, 1,  1, 1,1,1),
('豬排',   1, 1, 0, 1, 0, 1, 1, 1,  1, 1,1,1),
('宵夜',   1, 0, 1, 0, 0, 0, 0, 1,  1, 1,1,1),
('壽司',   0, 1, 0, 1, 0, 1, 1, 1,  1, 1,1,1),
('簡餐',   0, 1, 0, 1, 0, 1, 1, 0,  1, 1,1,1),
('日本料理', 0, 1, 0, 1, 0, 1, 1, 0,  1, 1,1,1),
('雞肉飯',  1, 0, 1, 0, 0, 1, 1, 1,  1, 1,1,1),
('晚餐',   1, 0, 1, 0, 0, 1, 1, 1,  1, 1,1,1),
('粥',      1, 0, 1, 0, 0, 1, 1, 1,  0, 1,1,1),
('河粉',    1, 0, 1, 0, 0, 1, 1, 1,  1, 0,1,1),
('滷肉飯',   1, 0, 1, 0, 0, 1, 1, 1,  1, 1,1,1),
('便當',    1, 0, 1, 0, 0, 1, 1, 1,  1, 1,1,1),
('滷味',   1, 0, 1, 0, 0, 0, 1, 1,  1, 1,1,1),
('火鍋',   0, 1, 0, 1, 0, 1, 1, 0,  1, 1,1,1),
('牛排',   0, 1, 0, 1, 0, 1, 1, 0,  1, 1,1,1),
('燒肉',   0, 1, 0, 1, 0, 1, 1, 0,  1, 1,1,1),
('羊肉爐',  0, 1, 0, 1, 0, 1, 1, 0,  0, 1,1,1),
('麻油雞',  0, 1, 0, 1, 0, 1, 1, 0,  0, 1,1,1),
('薑母鴨',  0, 1, 0, 1, 0, 1, 1, 0,  0, 1,1,1),
('丼飯',    1, 0, 0, 1, 0, 1, 1, 0,  1, 1,1,1),
('pizza',  1, 0, 1, 0, 0, 1, 1, 1,  1, 1,1,1),
('自助餐',  1, 0, 1, 0, 0, 1, 1, 1,  1, 1,1,1),
('poke',   1, 0, 1, 0, 0, 1, 1, 1,  1, 0,1,1),
('早午餐',  1, 1, 0, 1, 1, 1, 0, 0,  1, 1,1,1)
;



CREATE TABLE custom_black_list(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
name TEXT  NOT NULL,
FOREIGN KEY (user_id) REFERENCES user (id)
);


INSERT INTO custom_black_list (user_id, name)
VALUES
(1, '八方雲集'),
(1, '星巴克'),
(1, '路易莎'),
(1, '麥當勞'),
(1, '生水餃'),
(1, '冷凍'),
(1, '素')
;



CREATE TABLE response(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    IP TEXT,
    ts TIMESTAMP,
    user_id INTEGER NOT NULL,
    category TEXT,
    restaurant TEXT,
    response TEXT
);
