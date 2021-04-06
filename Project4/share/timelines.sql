-- $ sqlite3 timelines.db < timelines.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS users (
    username    TEXT NOT NULL PRIMARY KEY,
    email       TEXT NOT NULL UNIQUE,
    pw          TEXT NOT NULL
);

INSERT INTO users VALUES('JohnLegend', 'JohnLegend@csu.fullerton.edu', 'John*123');
INSERT INTO users VALUES('TaylorSwift', 'TaylorSwift@gmail.com', 'Taylor*123');
INSERT INTO users VALUES('BrunoMars', 'BrunoMars@csu.fullerton.edu', 'Bruno*123');
INSERT INTO users VALUES('MileyCyrus', 'MileyCyrus@csu.fullerton.edu', 'Miley*123');
INSERT INTO users VALUES('ElonMusk', 'ElonMusk@csu.fullerton.edu', 'Elon*123');

CREATE TABLE IF NOT EXISTS followers (
    id                  INTEGER,
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

CREATE TABLE IF NOT EXISTS posts (
    id              INTEGER PRIMARY KEY,
    username        TEXT NOT NULL,
    post            TEXT NOT NULL,
    timestamp       INTEGER DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(username) REFERENCES users(username)
);

INSERT INTO posts(username, post) VALUES('JohnLegend', "All of me");
INSERT INTO posts(username, post) VALUES('TaylorSwift', "You belong with me");
INSERT INTO posts(username, post) VALUES('ElonMusk', "Time to tell a story about SPACEX and Tesla");
INSERT INTO posts(username, post) VALUES('ElonMusk', "Good morning");
INSERT INTO posts(username, post) VALUES('MileyCyrus', "It's the climb");
INSERT INTO posts(username, post) VALUES('BrunoMars', "Locked out of heaven");


COMMIT;

