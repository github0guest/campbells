import re
import sqlite3
from datetime import timezone, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Comic, Character, ComicCharacter, SearchTranscripts
from contextlib import contextmanager


class ComicManager:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.conn.cursor().execute('PRAGMA foreign_keys = ON')

    def close(self):
        self.conn.close()

    def char_insertion(self):
        p = re.compile('\w+:')
        c = self.conn.cursor()
        for row in c.execute('SELECT date, transcript FROM comic'):
            date = row[0]
            transcript = p.findall(row[1])
            for word in transcript:
                name = str(word).rstrip(":")
                c2 = self.conn.cursor()
                try:
                    c2.execute('INSERT INTO character(first_name, last_name) VALUES(?,?)', (name, ""))
                except sqlite3.IntegrityError as err:
                    print(err)
                    pass
                c2.execute('SELECT id FROM character WHERE first_name = ?', (name,))
                char_row = c2.fetchone()
                try:
                    c2.execute('INSERT INTO comic_character(comic_date, character_id) VALUES (?,?)',
                               (date, char_row[0]))
                except sqlite3.IntegrityError as err:
                    print(err)
                    pass
        self.conn.commit()

    # TODO: Upgrade this function so that it takes a list of characters to remove
    # TODO: Can create column in character table to flag suspicious names
    # TODO: Write a test(s) for this action that will verify the changes in the tables
    def remove_character(self, first_name):
        """Remove a row from the character table"""
        c = self.conn.cursor()
        c.execute('DELETE FROM character WHERE first_name = ?', (first_name,))
        self.conn.commit()

    def characters_from_date(self, date):
        """List of characters given a date"""
        dt_obj = datetime.strptime(date, '%Y-%m-%d')
        unix_time = datetime(dt_obj.year, dt_obj.month, dt_obj.day, tzinfo=timezone.utc).timestamp()
        c = self.conn.cursor()
        c.execute('SELECT first_name '
                  'FROM character '
                  'JOIN comic_character '
                  'ON comic_character.character_id = character.id '
                  'WHERE comic_character.comic_date = ?', (unix_time,))
        result = c.fetchall()
        names = []
        for entry in result:
            names.append(entry[0])
        return sorted(names, key=str.lower)

    def dates_from_character(self, first_name):
        """List of dates on which a given character appears"""
        c = self.conn.cursor()
        c.execute('SELECT comic_date '
                  'FROM comic_character '
                  'JOIN character '
                  'ON comic_character.character_id = character.id '
                  'WHERE character.first_name = ?', (first_name,))
        unix_dates = c.fetchall()
        readable_dates = []
        for date in unix_dates:
            readable_dates.append(datetime.utcfromtimestamp(date[0]).strftime('%Y-%m-%d'))
        return readable_dates

    def search_transcripts(self, search_term):
        """Searches comic transcripts and returns the dates for matching comics"""
        c = self.conn.cursor()
        if search_term is "":
            raise EmptySearchException
        c.execute('SELECT date FROM search_transcripts WHERE transcript MATCH ?', (search_term,))
        unix_dates = c.fetchall()
        readable_dates = []
        for date in unix_dates:
            readable_dates.append(datetime.utcfromtimestamp(date[0]).strftime('%Y-%m-%d'))
        return readable_dates

    # TODO: command line arguments


class ComicManagerAlchemy:
    def __init__(self):
        engine = create_engine('sqlite:///foxtrot.db')
        self.DBSession = sessionmaker(bind=engine)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.DBSession()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def char_insertion(self):
        reg_word_before_colon = re.compile('(\w+):')
        with self.session_scope() as s:
            set_names_all_characters = set()
            for entry in s.query(Comic):
                names = reg_word_before_colon.findall(entry.transcript)
                set_names_for_date = set()
                for name in names:
                    if name not in set_names_all_characters:
                        char_entry = Character(first_name=name)
                        with self.session_scope() as s2:
                            s2.add(char_entry)
                            set_names_all_characters.add(name)
                    if name not in set_names_for_date:
                        with self.session_scope() as s2:
                            char = s2.query(Character).filter(Character.first_name == name).one()
                            comic_char_entry = ComicCharacter(comic_date=entry.date, character_id=char.id)
                            s2.add(comic_char_entry)
                            set_names_for_date.add(name)

    def characters_from_date(self, date):
        """List of characters given a date"""
        dt_obj = datetime.strptime(date, '%Y-%m-%d')
        unix_time = datetime(dt_obj.year, dt_obj.month, dt_obj.day, tzinfo=timezone.utc).timestamp()
        with self.session_scope() as s:
            comic = s.query(Comic).filter(Comic.date==unix_time).one()
            return [character.first_name for character in comic.characters]

    def dates_from_character(self, first_name):
        """List of dates on which a given character appears"""
        with self.session_scope() as s:
            char = s.query(Character).filter(Character.first_name==first_name).one()
            return [datetime.utcfromtimestamp(comic.date).strftime('%Y-%m-%d') for comic in char.comics]

    def search_transcripts(self, search_term):
        """Searches comic transcripts and returns the dates for matching comics"""

        with self.session_scope() as s:
            results = s.query(SearchTranscripts).filter('transcript MATCH :search_term').params(search_term=search_term).all()
            return [datetime.utcfromtimestamp(result.date).strftime('%Y-%m-%d') for result in results]

class EmptySearchException(Exception):
    pass


if __name__ == "__main__":
    test = ComicManagerAlchemy()
    test.char_insertion()
