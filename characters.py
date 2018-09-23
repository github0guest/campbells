import sqlite3
import re
from operator import itemgetter

conn = sqlite3.connect('foxtrot.db')
c = conn.cursor()
p = re.compile('\w+:')

characters = {}

for row in c.execute('SELECT transcript FROM comics'):
    m = p.findall(row[0])
    for word in m:
        name = str(word).rstrip(":")
        if name not in characters:
            characters[name] = 0
        characters[name] += 1

sorted_list = sorted(characters.items(), key=itemgetter(1), reverse=True)
for item in sorted_list:
    c.execute('INSERT INTO characters(name) VALUES(?)', (item[0],))

conn.commit()
conn.close()
