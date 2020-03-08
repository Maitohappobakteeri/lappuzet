from .base import Base
from .schema import Schema, Property, PropertyType

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Boolean, CHAR
)
from sqlalchemy.orm import relationship
from flask_restful import fields

OwnNoteSchema = Schema(
    "OwnNote",
    [
        Property("id", PropertyType.integer),
        Property("message", PropertyType.string),
        Property("created_at", PropertyType.datetime),
        Property("resolved", PropertyType.boolean),
        Property("resolved_at", PropertyType.datetime),
    ]
)

NewNoteSchema = Schema(
    "NewNote",
    [
        Property("message", PropertyType.string),
        Property("needsResolve", PropertyType.boolean),
    ]
)

OwnJournalNoteSchema = Schema(
    "OwnJournalNote",
    [
        Property("id", PropertyType.integer),
        Property("message", PropertyType.string),
        Property("created_at", PropertyType.datetime),
        Property("resolved", PropertyType.boolean),
        Property("resolved_at", PropertyType.datetime),

        Property("journal_note_additional", PropertyType.object, schema=Schema(
            "journal_note_additional",
            [
                Property("mood", PropertyType.integer),
                Property("food", PropertyType.integer),
                Property("sleep", PropertyType.integer),
                Property("stress", PropertyType.integer),
            ]
        )),
    ]
)

NewJournalNoteSchema = Schema(
    "NewJournalNote",
    [
        Property("message", PropertyType.string),
        Property("mood", PropertyType.integer),
        Property("food", PropertyType.integer),
        Property("sleep", PropertyType.integer),
        Property("stress", PropertyType.integer),
    ]
)


class Note(Base):
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True)
    owner = Column(Integer, nullable=False)
    message = Column(String(2048), nullable=False)
    type = Column(CHAR(32), nullable=False)
    created_at = Column(DateTime, nullable=False)

    resolved = Column(Boolean, nullable=False)
    resolved_at = Column(DateTime)

    category = Column(Integer, ForeignKey('note_category.id'), nullable=False)

    journal_note_additional = relationship("JournalNoteAdditional", backref="note", uselist=False)
