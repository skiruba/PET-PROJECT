DROP DATABASE IF EXISTS petFinder;

CREATE DATABASE IF NOT EXISTS PetFinder;

USE petFinder;

CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT NOT NULL,
    user_username VARCHAR(255) NOT NULL,
    user_password VARCHAR(225) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    user_age INT NOT NULL,
    user_gender VARCHAR(255) NOT NULL,
    user_email_address VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS pet (
    pet_id INT AUTO_INCREMENT NOT NULL,
    pet_name VARCHAR(255) NOT NULL,
    pet_age INT NOT NULL,
    pet_gender VARCHAR(255) NOT NULL,
    pet_type VARCHAR(255) NOT NULL,
    pet_breed VARCHAR(255) NOT NULL,
    pet_health VARCHAR(255) NOT NULL,
    pet_owner INT NOT NULL,
    pet_training VARCHAR(255) NOT NULL,
    pet_about VARCHAR(255) NOT NULL,
    photo VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state CHAR(2) NOT NULL,
    PRIMARY KEY (pet_id),
    FOREIGN KEY (pet_owner) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS comment (
	comment_id INT AUTO_INCREMENT NOT NULL,
    author_id INT NOT NULL,
    comment_content VARCHAR(255) NOT NULL,
    post_id INT NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (post_id) REFERENCES pet(pet_id),
    FOREIGN KEY (author_id) REFERENCES user(user_id)
);
