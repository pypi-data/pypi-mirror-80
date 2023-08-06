from typing import List, Tuple
from reamber.base.NoteObject import NoteObject
from reamber.base.HitObject import HitObject
from reamber.base.HoldObject import HoldObject
import pandas as pd


class MapObjectNotes(List[NoteObject]):

    def __init__(self, *args):
        list.__init__(self, *args)

    def noteDf(self) -> pd.DataFrame:
        return pd.DataFrame({'noteObjects': self})

    def noteObjectsSorted(self) -> List[NoteObject]:
        """ Returns a copy of Sorted NoteObjs """
        return sorted(self)

    def keys(self) -> int:
        """ CALCULATES the key of the map
        Note that keys of the map isn't stored, it's dynamic and not a stored parameter.
        The function just finds the maximum column.
        """
        return max([note.column for note in self])

    def hitObjects(self, sort: bool = False) -> List[HitObject]:
        """ Returns a copy of (Sorted) HitObjs """
        if sort:
            return sorted([note for note in self if isinstance(note, HitObject)], key=lambda x: x.offset)
        else:
            return [note for note in self if isinstance(note, HitObject)]

    def holdObjects(self, sort: bool = False) -> List[HoldObject]:
        """ Returns a copy of (Sorted) HoldObjs """
        if sort:
            return sorted([note for note in self if isinstance(note, HoldObject)])
        else:
            return [note for note in self if isinstance(note, HoldObject)]

    def hitObjectOffsets(self, sort: bool = True) -> List[float]:
        """ Returns a copy of the HitObj Offsets """
        return [ho.offset for ho in self.hitObjects(sort)]

    def holdObjectOffsets(self, sort: bool = True) -> List[Tuple[float, float]]:
        """ Returns a copy of the HoldObj Offsets [(Head0, Tail0), (Head1, Tail1), ...]"""
        return [(ho.offset, ho.tailOffset()) for ho in self.holdObjects(sort)]

    def addNoteOffsets(self, by: float):
        """ Move all notes by a specific ms """
        for note in self: note.offset += by

    def lastNoteOffset(self) -> float:
        """ Get Last Note Offset """
        hos = self.noteObjectsSorted()
        lastHit = self.hitObjects()[-1]
        lastHold = self.holdObjects()[-1]

        if lastHit.offset > lastHold.offset + lastHold.length:
            return lastHit.offset
        else:
            return lastHold.offset + lastHold.length

    def firstNoteOffset(self) -> float:
        """ Get First Note Offset """
        hos = self.noteObjectsSorted()
        return hos[0].offset

    def firstLastNoteOffset(self) -> Tuple[float, float]:
        """ Get First and Last Note Offset
        This is slightly faster than separately calling the singular functions since it sorts once only
        """
        hos = self.noteObjectsSorted()
        lastHit = self.hitObjects()[-1]
        lastHold = self.holdObjects()[-1]

        if lastHit.offset > lastHold.offset + lastHold.length:
            return hos[0].offset, lastHit.offset
        else:
            return hos[0].offset, lastHold.offset + lastHold.length

# t = NoteList([NoteObject(1, 2), NoteObject(3, 4)])
# t.append(NoteObject(3,44))
# print(t.noteDf())