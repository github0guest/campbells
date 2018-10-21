from datetime import timezone, datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

import config
from models import Comic, SearchTranscripts
from contextlib import contextmanager


class ComicManager:
    def __init__(self, database, echo=False):
        engine = create_engine(database, echo=echo)
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

    @staticmethod
    def parse_date(date):
        try:
            dt_obj = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise InvalidDateFormatException
        unix_time = datetime(dt_obj.year, dt_obj.month, dt_obj.day, tzinfo=timezone.utc).timestamp()
        return unix_time

    def transcript_from_date(self, date):
        """Transcript for a given date"""
        unix_time = self.parse_date(date)
        with self.session_scope() as s:
            comic = s.query(Comic).filter(Comic.date == unix_time).one()
            return comic.transcript

    def search_transcripts(self, search_term):
        """Searches comic transcripts and returns the dates for matching comics"""
        if search_term is "":
            raise NotImplementedException
        with self.session_scope() as s:
            results = s.query(SearchTranscripts).filter(text('transcript MATCH :search_term')).params(
                search_term=search_term).all()
            return [datetime.utcfromtimestamp(result.date).strftime('%Y-%m-%d') for result in results]

    def get_next_comic(self, date):
        """Returns next chronological comic for given date"""
        unix_time = self.parse_date(date)
        with self.session_scope() as s:
            try:
                selection = s.query(Comic).order_by(Comic.date).filter(Comic.date > unix_time).limit(1).one()
            except NoResultFound:
                raise NonexistentComicException
            return datetime.utcfromtimestamp(selection.date).strftime('%Y-%m-%d')

    def get_previous_comic(self, date):
        """Returns next chronological comic for given date"""
        unix_time = self.parse_date(date)
        with self.session_scope() as s:
            try:
                selection = s.query(Comic).order_by(Comic.date.desc()).filter(Comic.date < unix_time).limit(1).one()
            except NoResultFound:
                raise NonexistentComicException
            return datetime.utcfromtimestamp(selection.date).strftime('%Y-%m-%d')


class NonexistentComicException(Exception):
    pass


class NotImplementedException(Exception):
    pass


if __name__ == "__main__":
    cm = ComicManager(config.database)
    print(cm.transcript_from_date("1999-06-12"))
