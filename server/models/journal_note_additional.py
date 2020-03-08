from .base import Base

from sqlalchemy import (
    Column, Integer, ForeignKey
)


class JournalNoteAdditional(Base):
    __tablename__ = 'journal_note_additional'

    id = Column(Integer, ForeignKey('note.id'), primary_key=True)

    mood = Column(Integer)
    sleep = Column(Integer)
    stress = Column(Integer)
    food = Column(Integer)
