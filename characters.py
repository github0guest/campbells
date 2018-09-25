import sqlite3
import re
from operator import itemgetter

conn = sqlite3.connect('foxtrot.db')
c = conn.cursor()
p = re.compile('\w+:')

characters = {}


def char_insertion():
    c.execute('SELECT date, transcript FROM comic')
    date_transcript = c.fetchall()
    for row in date_transcript:
        date = row[0]
        m = p.findall(row[1])
        for word in m:
            name = str(word).rstrip(":")
            try:
                c.execute('INSERT INTO character(first_name, last_name) VALUES(?,?)', (name, ""))
            except sqlite3.IntegrityError as err:
                print(err)
                continue
            c.execute('SELECT id FROM character WHERE first_name = ?', (name, ))
            char_id = c.fetchone()
            try:
                c.execute('INSERT INTO comic_character(comic_date, character_id) VALUES (?,?)', (date, char_id[0]))
            except sqlite3.IntegrityError as err:
                print(err)
                continue
    conn.commit()
    conn.close()

char_insertion()
