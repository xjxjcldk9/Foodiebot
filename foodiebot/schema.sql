DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS no_eat;
DROP TABLE IF EXISTS last_eat;
DROP TABLE IF EXISTS black_list;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);



CREATE TABLE food(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT UNIQUE NOT NULL,
    manypeople INTEGER NOT NULL,
    money INTEGER NOT NULL,
    lunch INTEGER NOT NULL,
    dinner INTEGER NOT NULL,
    night INTEGER NOT NULL,
    ordinary INTEGER NOT NULL,
    hot INTEGER NOT NULL,
    cold INTEGER NOT NULL
);


INSERT INTO food
VALUES
(1, '牛肉麵', 0, 0, 1, 1, 0, 1, 1, 1),
(2, '早餐', 0, 0, 1, 0, 0, 1, 1, 1),
(3, '鍋燒麵', 0, 0, 1, 1, 0, 1, 1, 1),
(4, '燒臘', 0, 0, 1, 1, 0, 1, 1, 1),
(5, '永和豆漿', 0, 0, 0, 0, 1, 1, 1, 1),
(6, '咖哩', 0, 1, 1, 1, 0, 1, 1, 1),
(7, '粥', 0, 0, 1, 1, 1, 1, 0, 1),
(8, '河粉', 0, 0, 1, 1, 0, 1, 1, 1),
(9, '滷肉飯', 0, 0, 1, 1, 0, 1, 1, 1),
(10, '便當', 0, 0, 1, 1, 0, 1, 1, 1),
(11, '滷味', 0, 0, 0, 0, 1, 1, 1, 1),
(12, '火鍋', 1, 1, 1, 1, 0, 1, 0, 1),
(13, '牛排', 1, 1, 1, 1, 0, 1, 1, 1),
(14, '燒肉', 1, 1, 0, 1, 0, 1, 0, 1),
(15, '羊肉爐', 1, 1, 0, 1, 0, 0, 0, 1),
(16, '麻油雞', 1, 1, 0, 1, 0, 0, 0, 1),
(17, '薑母鴨', 1, 1, 0, 1, 0, 0, 0, 1),
(18, '丼飯', 0, 1, 1, 1, 0, 1, 1, 1),
(19, '拉麵', 0, 1, 1, 1, 0, 1, 1, 1),
(20, '水餃', 0, 0, 1, 1, 0, 1, 1, 1),
(21, '鍋貼', 0, 0, 1, 1, 0, 1, 1, 1),
(22, '熱炒', 1, 1, 0, 1, 0, 1, 1, 1),
(23, '豬腳飯', 0, 0, 1, 1, 0, 1, 1, 1),
(24, '乾麵', 0, 0, 1, 1, 0, 1, 1, 1),
(25, '海南雞', 0, 0, 1, 1, 0, 1, 1, 1),
(26, '速食', 0, 0, 1, 1, 1, 1, 1, 0),
(27, '涼麵', 0, 0, 1, 0, 1, 1, 1, 0),
(28, '臭臭鍋', 0, 0, 1, 1, 0, 1, 1, 1),
(29, 'pizza', 1, 1, 0, 1, 0, 1, 1, 1),
(30, '自助餐', 0, 0, 1, 1, 0, 1, 1, 1),
(31, 'poke', 0, 0, 1, 1, 0, 1, 1, 0),
(32, '早午餐', 1, 1, 1, 0, 0, 1, 1, 1),
(33, '豬排', 0, 1, 1, 1, 0, 1, 1, 1),
(34, '宵夜', 0, 0, 0, 0, 1, 1, 1, 1),
(35, '壽司', 1, 1, 1, 1, 0, 1, 1, 0),
(36, '簡餐', 1, 1, 1, 1, 0, 1, 1, 1),
(37, '日本料理', 1, 1, 1, 1, 0, 1, 1, 0),
(38, '雞肉飯', 0, 0, 1, 1, 0, 1, 1, 1),
(39, '晚餐', 0, 0, 0, 1, 0, 1, 1, 1)
;




CREATE TABLE no_eat(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
category TEXT UNIQUE NOT NULL,
FOREIGN KEY (user_id) REFERENCES user (id)
);



CREATE TABLE last_eat(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
category TEXT UNIQUE NOT NULL,
FOREIGN KEY (user_id) REFERENCES user (id)
);


CREATE TABLE black_list(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
name TEXT UNIQUE NOT NULL,
FOREIGN KEY (user_id) REFERENCES user (id)
);