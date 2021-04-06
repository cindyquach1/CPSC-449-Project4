-- $ sqlite3 users.db < users.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY,
    username    TEXT NOT NULL UNIQUE,
    email       TEXT NOT NULL UNIQUE,
    pw          TEXT NOT NULL
);

INSERT INTO users VALUES(1, 'JohnLegend', 'JohnLegend@csu.fullerton.edu', 'John*123');
INSERT INTO users VALUES(2, 'TaylorSwift', 'TaylorSwift@gmail.com', 'Taylor*123');
INSERT INTO users VALUES(3, 'BrunoMars', 'BrunoMars@csu.fullerton.edu', 'Bruno*123');
INSERT INTO users VALUES(4, 'MileyCyrus', 'MileyCyrus@csu.fullerton.edu', 'Miley*123');
INSERT INTO users VALUES(5, 'ElonMusk', 'ElonMusk@csu.fullerton.edu', 'Elon*123');

CREATE TABLE IF NOT EXISTS followers (
    id                  INTEGER PRIMARY KEY,
    username            TEXT NOT NULL,
    usernameToFollow    TEXT NOT NULL,

    FOREIGN KEY(username) REFERENCES users(username),
    FOREIGN KEY(usernameToFollow) REFERENCES users(username),
    UNIQUE(username, usernameToFollow)
);

INSERT INTO followers(username, usernameToFollow) VALUES('JohnLegend', 'TaylorSwift');
INSERT INTO followers(username, usernameToFollow) VALUES('JohnLegend', 'BrunoMars');
INSERT INTO followers(username, usernameToFollow) VALUES('TaylorSwift', 'JohnLegend');
INSERT INTO followers(username, usernameToFollow) VALUES('TaylorSwift', 'BrunoMars');
INSERT INTO followers(username, usernameToFollow) VALUES('TaylorSwift', 'MileyCyrus');
INSERT INTO followers(username, usernameToFollow) VALUES('BrunoMars', 'MileyCyrus');
INSERT INTO followers(username, usernameToFollow) VALUES('MileyCyrus', 'JohnLegend');
INSERT INTO followers(username, usernameToFollow) VALUES('MileyCyrus', 'ElonMusk');
INSERT INTO followers(username, usernameToFollow) VALUES('ElonMusk', 'MileyCyrus');

COMMIT;