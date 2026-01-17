CREATE DATABASE mini_ecom;
USE mini_ecom;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50),
    password VARCHAR(50)
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    price INT
);

CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50),
    product VARCHAR(50),
    price INT
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50),
    total INT
);

INSERT INTO users VALUES (1,'test@gmail.com','123');
INSERT INTO products(name,price) VALUES
('Laptop',50000),
('Mobile',20000),
('Headphone',3000);