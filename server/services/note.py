from .service import Service, current_user_id, current_client_id
from models.note import Note
from models.note_category import NoteCategory
from utility import isTrue, isFalse, isNone, notNone

import datetime


NOTE_TYPE = "note"


class NoteService(Service):
    def __init__(self, session):
        super().__init__(session)

    def new(self, category, message, needsResolve):
        note = Note(
            owner=current_client_id(),
            message=message,
            resolved=not needsResolve,
            created_at=datetime.datetime.utcnow(),
            category=category,
            type=NOTE_TYPE
        )

        self._session.add(note)
        self._session.commit()
        return note

    def resolve(self, noteId):
        note = self.note(noteId)
        note.resolved = True
        note.resolved_at = datetime.datetime.utcnow()
        return note

    def note(self, noteId):
        return self._query(Note).get(noteId)

    def unresolved(self, category):
        return self._query(Note) \
                   .filter(Note.owner == current_client_id()) \
                   .filter(Note.type == NOTE_TYPE) \
                   .filter(Note.category == category) \
                   .filter(isFalse(Note.resolved)) \
                   .all()

    def history(self, category, start, amount):
        return self._query(Note) \
                   .filter(Note.owner == current_client_id()) \
                   .filter(Note.type == NOTE_TYPE) \
                   .filter(Note.category == category) \
                   .filter(isTrue(Note.resolved)) \
                   .order_by(Note.created_at.desc()) \
                   .offset(start) \
                   .limit(amount) \
                   .all()

    def categoryList(self):
       return self._query(NoteCategory) \
                  .filter(NoteCategory.owner == current_client_id()) \
                  .filter(isNone(NoteCategory.deleted_at)) \
                  .all()

    def newCategory(self, name):
       category = NoteCategory(
           owner=current_client_id(),
           name=name,
           created_at=datetime.datetime.utcnow()
       )

       self._session.add(category)
       self._session.commit()
       return category
