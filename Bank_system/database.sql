CREATE DATABASE banking;
USE banking;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100),
    balance INT DEFAULT 0
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    type VARCHAR(20),
    amount INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email, password, balance)
VALUES ('Ram','ram@gmail.com','123',0);

INSERT INTO users (name, email, password, balance)
 VALUES('Shyam','shyam@gmail.com',334,0);