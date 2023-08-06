from reamber.base.lists.NoteObjList import NoteObjList
from reamber.base.lists.BpmList import BpmList


class MapObject:
    notes: NoteObjList
    bpms: BpmList

    def addOffset(self, by: float):
        """ Move all by a specific ms """
        self.notes.addOffset(by)
        self.bpms.addOffset(by)

    # from reamber.base.lists.TimedList import TimedList
    # from typing import TypeVar
    #
    # Base = TypeVar('Base', bound=TimedList)

    # @property
    # @abstractmethod
    # def notes(self) -> Base: pass
    #
    # @property
    # @abstractmethod
    # def bpms(self) -> Base: pass

    # The TRUE nature of notes and bpms is NoteList and BpmList respectively
    # The reason for having a Union with List[NoteObject] is to facilitate the __init__ generated.
    # Having a custom __init__ would break a lot of subclasses so I just used a __post_init__ correction.
    # notes: Union[NoteList, List[NoteType]] = field(default_factory=lambda: NoteList())
    # bpms:  Union[BpmList,  List[BpmType]]   = field(default_factory=lambda: BpmList())

    # def _recast(self):
    #     self._recast()
    #     """ Recast helps recast all List[Singulars] into the correct base class """
    #     self.notes = NoteList(self.notes)
    #     self.bpms  = BpmList(self.bpms)
    #
    # def __post_init__(self) -> None:
    #     """ This corrects all List objects that can be implicitly casted as the classes """
