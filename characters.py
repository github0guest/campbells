import sqlite3
import re
from datetime import timezone, datetime


def char_insertion():
    p = re.compile('\w+:')
    for row in c.execute('SELECT date, transcript FROM comic'):
        date = row[0]
        transcript = p.findall(row[1])
        for word in transcript:
            name = str(word).rstrip(":")
            c2 = conn.cursor()
            try:
                c2.execute('INSERT INTO character(first_name, last_name) VALUES(?,?)', (name, ""))
            except sqlite3.IntegrityError as err:
                print(err)
                pass
            c2.execute('SELECT id FROM character WHERE first_name = ?', (name, ))
            char_row = c2.fetchone()
            try:
                c2.execute('INSERT INTO comic_character(comic_date, character_id) VALUES (?,?)', (date, char_row[0]))
            except sqlite3.IntegrityError as err:
                print(err)
                pass
    conn.commit()


# TODO: Upgrade this function so that it takes a list of characters to remove
# TODO: Can create column in character table to flag suspicious names
# TODO: Write a test(s) for this action that will verify the changes in the tables
def remove_character(first_name):
    """Remove a row from the character table"""
    c.execute('DELETE FROM character WHERE first_name = ?', (first_name, ))
    conn.commit()


def characters_from_date(date):
    """List of characters given a date"""
    dt_obj = datetime.strptime(date, '%Y-%m-%d')
    unix_time = datetime(dt_obj.year, dt_obj.month, dt_obj.day, tzinfo=timezone.utc).timestamp()
    c.execute('SELECT first_name '
              'FROM character '
              'JOIN comic_character '
              'ON comic_character.character_id = character.id '
              'WHERE comic_character.comic_date = ?', (unix_time, ))
    result = c.fetchall()
    names = []
    for entry in result:
        names.append(entry[0])
    return sorted(names, key=str.lower)


def dates_from_character(first_name):
    """List of dates on which a given character appears"""
    c.execute('SELECT comic_date '
              'FROM comic_character '
              'JOIN character '
              'ON comic_character.character_id = character.id '
              'WHERE character.first_name = ?', (first_name, ))
    unix_dates = c.fetchall()
    readable_dates = []
    for date in unix_dates:
        readable_dates.append(datetime.utcfromtimestamp(date[0]).strftime('%Y-%m-%d'))
    return readable_dates


# TODO: search through transcripts
# TODO: make a front-end


# TODO: command line arguments


if __name__ == "__main__":
    conn = sqlite3.connect('foxtrot.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    # characters_from_date("1988-08-03")
    dates_from_character('IndsertString')
    # char_insertion()
    # remove_character('punishment')
    conn.close()