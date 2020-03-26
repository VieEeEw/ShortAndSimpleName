DROP TABLE IF EXISTS user;

CREATE TABLE user (
    `net_id`    VARCHAR(10)     PRIMARY KEY,
    `name`      VARCHAR(255),
    `pswd`      VARCHAR(255)    NOT NULL
);
