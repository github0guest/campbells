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
        w = str(word).rstrip(":").casefold().capitalize()
        if w not in characters:
            characters[w] = 0
        characters[w] += 1

sorted_list = sorted(characters.items(), key=itemgetter(1), reverse=True)
print(sorted_list)
