CREATE TABLE IF NOT EXISTS escalators (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       top VARCHAR(100) NOT NULL,
       bottom VARCHAR(100) NOT NULL,
       up INTEGER NOT NULL DEFAULT 1,
       down INTEGER NOT NULL DEFAULT 1
);

DELETE FROM escalators;
DELETE FROM sqlite_sequence WHERE name='escalators';

INSERT INTO escalators (bottom, top) VALUES (
       'Sur La Table',
       'Currency Exchange'
);

INSERT INTO escalators (bottom, top) VALUES (
       'Au Bon Pain',
       'Louis Vuitton'
);

INSERT INTO escalators (bottom, top) VALUES (
       'Marriott',
       'Tiffany''s'
);

CREATE TABLE IF NOT EXISTS escalator_history (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       escalator INTEGER NOT NULL,
       direction VARCHAR(4) NOT NULL,
       event VARCHAR(25) NOT NULL,
       added VARCHAR(25) NOT NULL
);

DELETE FROM escalator_history;
DELETE FROM sqlite_sequence WHERE name='escalator_history';

INSERT INTO escalator_history (escalator, direction, event, added)
VALUES (
       1, 'up', 'broken', '2017-01-01 07:00:00.000');

INSERT INTO escalator_history (escalator, direction, event, added)
VALUES (
       1, 'up', 'broken', '2017-01-01 07:30:00.000');

INSERT INTO escalator_history (escalator, direction, event, added)
VALUES (
       1, 'up', 'fixed', '2017-01-01 08:00:00.000');

INSERT INTO escalator_history (escalator, direction, event, added)
VALUES (
       1, 'down', 'broken', '2017-01-01 09:00:00.000');

INSERT INTO escalator_history (escalator, direction, event, added)
VALUES (
       1, 'down', 'broken', '2017-01-01 09:30:00.000');

INSERT INTO escalator_history (escalator, direction, event, added)
VALUES (
       1, 'down', 'fixed', '2017-01-01 10:00:00.000');

INSERT INTO escalator_history (escalator, direction, event, added)
VALUES (
       1, 'down', 'broken', '2017-01-01 10:30:00.000');
