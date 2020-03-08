from .service import Service, current_user_id, current_client_id
from models.note import Note
from models.journal_note_additional import JournalNoteAdditional

from sqlalchemy.orm import joinedload

import datetime


JOURNAL_TYPE = "journal"


class JournalService(Service):
    def __init__(self, session):
        super().__init__(session)

    def new(self, message, additional):
        note = Note(
            owner=current_client_id(),
            message=message,
            resolved=True,
            created_at=datetime.datetime.utcnow(),
            type=JOURNAL_TYPE,
            journal_note_additional=JournalNoteAdditional(
                food=additional["food"],
                sleep=additional["sleep"],
                stress=additional["stress"],
                mood=additional["mood"]
            )
        )

        self._session.add(note)
        self._session.commit()

        return note

    def history(self, start, amount):
        return self._query(Note) \
                   .filter(Note.owner == current_client_id()) \
                   .filter(Note.type == JOURNAL_TYPE) \
                   .order_by(Note.created_at.desc()) \
                   .offset(start) \
                   .limit(amount) \
                   .all()
