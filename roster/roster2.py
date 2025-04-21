import json
import sqlite3

conn = sqlite3.connect('rosterdb2.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS member;

CREATE TABLE user (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name    TEXT UNIQUE
);

CREATE TABLE course (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title   TEXT UNIQUE
);

CREATE TABLE member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
);

''')


fname = input("Enter file name: ")
if len(fname) < 1:
    fname = 'roster_data.json'

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:

    name = entry[0]
    title = entry[1]
    role = entry[2]

    print((name,title))

    cur.execute('''INSERT OR IGNORE INTO user (name)
        VALUES ( ? )''', (name,))
    cur.execute('''SELECT id FROM user WHERE name = ? ''', (name,))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO course (title)
        VALUES ( ? )''', (title,))
    cur.execute('''SELECT id FROM course WHERE title = ? ''', (title,))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO member (user_id, course_id, role)
        VALUES ( ?, ?, ? )''', (user_id, course_id, role))

    conn.commit()

