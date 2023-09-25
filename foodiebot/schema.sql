DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS default_food;
DROP TABLE IF EXISTS default_black_list;
DROP TABLE IF EXISTS custom_black_list;
DROP TABLE IF EXISTS custom_food_onboard;
DROP TABLE IF EXISTS custom_food_reserve;




CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL
);


CREATE TABLE default_food(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT UNIQUE NOT NULL,
    singlepeople INTEGER ,
    manypeople INTEGER ,
    cheap INTEGER ,
    expensive INTEGER ,
    breakfast INTEGER,
    lunch INTEGER ,
    dinner INTEGER ,
    night INTEGER ,
    ordinary INTEGER ,
    hot INTEGER ,
    cold INTEGER
);


INSERT INTO default_food (category, singlepeople, manypeople, cheap, expensive, breakfast, lunch, dinner, night, ordinary, hot, cold)
VALUES
('牛肉麵',  1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1),
('早餐',    1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1),
('鍋燒麵',  1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1),
('燒臘',    1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1),
('永和豆漿', 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1)
;

/*
('咖哩', 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1),
('粥', 0, 0, 0,1, 1, 1, 1, 0, 1),
('河粉', 0, 0, 0,1, 1, 0, 1, 1, 1),
('滷肉飯', 0, 0, 0,1, 1, 0, 1, 1, 1),
('便當', 0, 0, 0,1, 1, 0, 1, 1, 1),
('滷味', 0, 0, 0,0, 0, 1, 1, 1, 1),
('火鍋', 1, 1, 0,1, 1, 0, 1, 0, 1),
('牛排', 1, 1, 0,1, 1, 0, 1, 1, 1),
('燒肉', 1, 1, 0,0, 1, 0, 1, 0, 1),
('羊肉爐', 1, 1, 0,0, 1, 0, 0, 0, 1),
('麻油雞', 1, 1, 0,0, 1, 0, 0, 0, 1),
('薑母鴨', 1, 1, 0,0, 1, 0, 0, 0, 1),
('丼飯', 0, 1, 0,1, 1, 0, 1, 1, 1),
('拉麵', 0, 1, 0,1, 1, 0, 1, 1, 1),
('水餃', 0, 0, 0,1, 1, 0, 1, 1, 1),
('鍋貼', 0, 0, 0,1, 1, 0, 1, 1, 1),
('熱炒', 1, 1, 0,0, 1, 0, 1, 1, 1),
('豬腳飯', 0, 0, 0,1, 1, 0, 1, 1, 1),
('乾麵', 0, 0, 0,1, 1, 0, 1, 1, 1),
('海南雞', 0, 0, 0,1, 1, 0, 1, 1, 1),
('速食', 0, 0, 0,1, 1, 1, 1, 1, 0),
('涼麵', 0, 0, 0,1, 0, 1, 1, 1, 0),
('臭臭鍋', 0, 0, 0,1, 1, 0, 1, 1, 1),
('pizza', 1, 1, 0,0, 1, 0, 1, 1, 1),
('自助餐', 0, 0, 0,1, 1, 0, 1, 1, 1),
('poke', 0, 0, 0,1, 1, 0, 1, 1, 0),
('早午餐', 1, 1,0, 1, 0, 0, 1, 1, 1),
('豬排', 0, 1, 0,1, 1, 0, 1, 1, 1),
('宵夜', 0, 0, 0,0, 0, 1, 1, 1, 1),
('壽司', 1, 1,0, 1, 1, 0, 1, 1, 0),
('簡餐', 1, 1, 0,1, 1, 0, 1, 1, 1),
('日本料理', 1, 1,0, 1, 1, 0, 1, 1, 0),
('雞肉飯', 0, 0,0, 1, 1, 0, 1, 1, 1),
('晚餐', 0, 0,0, 0, 1, 0, 1, 1, 1)
*/



CREATE TABLE custom_food_reserve(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT UNIQUE NOT NULL,
    singlepeople INTEGER ,
    manypeople INTEGER ,
    cheap INTEGER ,
    expensive INTEGER ,
    breakfast INTEGER,
    lunch INTEGER ,
    dinner INTEGER ,
    night INTEGER ,
    ordinary INTEGER ,
    hot INTEGER ,
    cold INTEGER,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);




CREATE TABLE custom_food_onboard(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT UNIQUE NOT NULL,
    singlepeople INTEGER ,
    manypeople INTEGER ,
    cheap INTEGER ,
    expensive INTEGER ,
    breakfast INTEGER,
    lunch INTEGER ,
    dinner INTEGER ,
    night INTEGER ,
    ordinary INTEGER ,
    hot INTEGER ,
    cold INTEGER,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);




CREATE TABLE default_black_list(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE NOT NULL
);

INSERT INTO default_black_list (name)
VALUES
('八方雲集'),
('星巴克'),
('路易莎'),
('麥當勞'),
('生水餃'),
('冷凍'),
('素')
;

CREATE TABLE custom_black_list(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
name TEXT UNIQUE NOT NULL,
FOREIGN KEY (user_id) REFERENCES user (id)
);