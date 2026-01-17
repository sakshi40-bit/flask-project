CREATE DATABASE exam_reg;
USE exam_reg;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50),
    password VARCHAR(50)
);

CREATE TABLE exam_registration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(50),
    exam_name VARCHAR(50),
    subject VARCHAR(50)
);
