CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    question varchar(128)
);

CREATE TABLE IF NOT EXISTS answers (
    id SERIAL PRIMARY KEY,
    question_id int,
    answer varchar(128),
    correct bool
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username varchar(128),
    nickname varchar(128),
    email varchar(128),
    password varchar(256),
    disabled bool
);