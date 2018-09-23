import sqlite3
import re
from operator import itemgetter

download_directory = '/Users/shirley/Desktop/foxtrot/'
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
with open(download_directory + "character_list.txt", 'a') as f:
    for item in sorted_list:
        if item[1] > 2:
            f.write(item[0]+"\n")

conn.close()