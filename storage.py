from datetime import timezone, datetime
from flask_sqlalchemy import SQLAlchemy
from exceptions import InvalidDateFormatException, NonexistentComicException, NotImplementedException
from models import Comic, SearchTranscripts
from contextlib import contextmanager


class ComicManager:
    def __init__(self, app):
        self.app = app
        self.db = SQLAlchemy(self.app)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.db.session
        try:
            yield session
            session.commit()
        except Exception:
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
        comic = Comic.query.filter(Comic.date == unix_time).one()
        return comic.transcript

    def search_transcripts(self, search_term):
        """Searches comic transcripts and returns the dates for matching comics"""
        if self.app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            results = SearchTranscripts.query.filter(self.db.text('transcript MATCH :search_term')).params(
                search_term=search_term).all()
        elif self.app.config['SQLALCHEMY_DATABASE_URI'].startswith('mysql'):
            results = Comic.query.filter(self.db.text('MATCH(transcript) AGAINST(:search_term)')).params(
                search_term=search_term).all()
        else:
            raise NotImplementedException
        return [datetime.utcfromtimestamp(result.date).strftime('%Y-%m-%d') for result in results]

    def get_next_comic(self, date):
        """Returns next chronological comic for given date"""
        unix_time = self.parse_date(date)
        selection = Comic.query.order_by(Comic.date).filter(Comic.date > unix_time).first()
        if selection is None:
            raise NonexistentComicException
        return datetime.utcfromtimestamp(selection.date).strftime('%Y-%m-%d')

    def get_previous_comic(self, date):
        """Returns next chronological comic for given date"""
        unix_time = self.parse_date(date)
        selection = Comic.query.order_by(Comic.date.desc()).filter(Comic.date < unix_time).first()
        if selection is None:
            raise NonexistentComicException
        return datetime.utcfromtimestamp(selection.date).strftime('%Y-%m-%d')


if __name__ == "__main__":
    pass
