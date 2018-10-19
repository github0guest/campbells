from sqlalchemy import Column, ForeignKey, Integer, Text, create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Comic(Base):
    __tablename__ = 'comic'
    date = Column(Integer, primary_key=True)
    transcript = Column(Text)
    characters = relationship(
        'Character',
        secondary='comic_character'
    )


class Character(Base):
    __tablename__ = 'character'
    __table_args__ = (
        UniqueConstraint('first_name', 'last_name'),
    )
    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)
    comics = relationship(
        Comic,
        secondary='comic_character'
    )


class ComicCharacter(Base):
    __tablename__ = 'comic_character'
    character_id = Column(Integer, ForeignKey('character.id'), primary_key=True)
    comic_date = Column(Integer, ForeignKey('comic.date'), primary_key=True)


class SearchTranscripts(Base):
    __tablename__ = 'search_transcripts'
    transcript = Column(Text)
    date = Column(Integer, primary_key=True)


if __name__ == '__main__':
    engine = create_engine('sqlite:///foxtrot.db')
    Base.metadata.create_all(engine)
