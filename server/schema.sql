DROP TABLE IF EXISTS user;

CREATE TABLE user (
    `net_id`    VARCHAR(10) PRIMARY KEY,
    `name`      VARCHAR(255),
    `pswd`      VARCHAR(255) NOT NULL,
    `token`     TEXT NOT NULL,
    `xpire_t`   TIMESTAMP
);
INSERT INTO user(net_id, name, pswd, token) VALUES ("ACCESS", "", "ACCESS_TOKEN");

CREATE TABLE IF NOT EXISTS vars (
    `var_name`  TEXT PRIMARY KEY,
    `var`       TEXT NOT NULL
);
INSERT OR REPLACE INTO vars VALUES ('xpire_gap', '+300 minutes');   -- Should be in that format

DROP TRIGGER IF EXISTS xpire_t_after_update_checker;
CREATE TRIGGER xpire_t_after_update_checker
    AFTER UPDATE ON user
    WHEN NEW.token NOT NULL
BEGIN
    UPDATE user
    SET xpire_t = datetime('now', (SELECT var FROM vars WHERE var_name="xpire_gap"))
    WHERE "net_id" = NEW.net_id;
END;

DROP TRIGGER IF EXISTS xpire_t_after_insert_checker;
CREATE TRIGGER xpire_t_after_insert_checker
    AFTER INSERT ON user
    WHEN NEW.token NOT NULL
BEGIN
    UPDATE user
    SET xpire_t = datetime('now', (SELECT var FROM vars WHERE var_name="xpire_gap"))
    WHERE "net_id" = NEW.net_id;
END;
