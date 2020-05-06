DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_crn;

CREATE TABLE user (
    `net_id`    VARCHAR(10) PRIMARY KEY,
    `name`      VARCHAR(255),
    `pswd`      VARCHAR(255) NOT NULL,
    `token`     TEXT NOT NULL,
    `xpire_t`   TIMESTAMP
);

CREATE TABLE user_crn (
    `net_id`    VARCHAR(10) NOT NULL,
    `crn`       VARCHAR(5) NOT NULL,
    FOREIGN KEY(`net_id`) REFERENCES user(`net_id`),
    PRIMARY KEY (net_id, crn)
);

CREATE TABLE IF NOT EXISTS vars (
    `var_name`  TEXT PRIMARY KEY,
    `var`       TEXT NOT NULL
);

DROP TRIGGER IF EXISTS vars_prevent_update;
DROP TRIGGER IF EXISTS vars_prevent_insert;
INSERT OR REPLACE INTO vars VALUES ('xpire_gap', '+300 minutes');   -- Should be in that format

CREATE TRIGGER vars_prevent_update
    BEFORE UPDATE ON vars
BEGIN
    SELECT RAISE(ABORT, 'Read-only table, contact db manager for help.');
END;

CREATE TRIGGER vars_prevent_insert
    BEFORE INSERT ON vars
BEGIN
    SELECT RAISE(ABORT, 'Read-only table, contact db manager for help.');
END;

DROP TRIGGER IF EXISTS xpire_t_after_update_checker;
CREATE TRIGGER xpire_t_after_update_checker
    AFTER UPDATE ON user
    WHEN NEW.token NOT NULL
BEGIN
    UPDATE user
    SET xpire_t = datetime('now', (SELECT var FROM vars WHERE var_name='xpire_gap'))
    WHERE "net_id" = NEW.net_id;
END;

DROP TRIGGER IF EXISTS xpire_t_after_insert_checker;
CREATE TRIGGER xpire_t_after_insert_checker
    AFTER INSERT ON user
    WHEN NEW.token NOT NULL
BEGIN
    UPDATE user
    SET xpire_t = datetime('now', (SELECT var FROM vars WHERE var_name='xpire_gap'))
    WHERE "net_id" = NEW.net_id;
END;
INSERT INTO user(net_id, pswd, token) VALUES ('ACCESS', '', 'ACCESS_TOKEN');

-- The following is for demo
DROP TABLE IF EXISTS courses;
-- CREATE TABLE courses (
--     `number`    INT NOT NULL,
--     `subject`   VARCHAR(10) NOT NULL,
--     PRIMARY KEY(`number`, `subject`)
-- );
DROP TABLE IF EXISTS sections;
-- CREATE TABLE sections (
--     `course_number`     INT NOT NULL,
--     `course_subject`    VARCHAR(10) NOT NULL,
--     `crn`               INT PRIMARY KEY,
--     FOREIGN KEY(`course_number`, "course_subject") REFERENCES courses(number, subject)
-- );
