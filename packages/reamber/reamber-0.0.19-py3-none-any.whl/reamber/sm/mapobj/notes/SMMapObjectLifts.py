from reamber.sm.lists.notes.SMNoteList import SMNoteList
from reamber.sm.SMLiftObject import SMLiftObject
from typing import List


class SMMapObjectLifts(List[SMLiftObject], SMNoteList):
    def data(self) -> List[SMLiftObject]:
        return self
