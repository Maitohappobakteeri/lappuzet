from .base import Base
from .schema import Schema, Property, PropertyType

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Boolean, CHAR
)
from flask_restful import fields

NoteCategorySchema = Schema(
    "NoteCategory",
    [
        Property("id", PropertyType.integer),
        Property("name", PropertyType.string),
        Property("created_at", PropertyType.datetime)
    ]
)

NewNoteCategorySchema = Schema(
    "NewNoteCategory",
    [
        Property("name", PropertyType.string),
    ]
)

class NoteCategory(Base):
    __tablename__ = 'note_category'

    id = Column(Integer, primary_key=True)
    owner = Column(Integer, nullable=False)

    name = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
