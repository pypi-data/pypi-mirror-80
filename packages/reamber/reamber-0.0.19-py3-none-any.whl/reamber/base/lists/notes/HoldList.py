from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Tuple

from reamber.base.Hold import Hold


class HoldList(ABC):
    @abstractmethod
    def data(self) -> List[Hold]: ...

    def columns(self) -> List[int]:
        return [i.column for i in self.data()]

    def deepcopy(self):
        """ Returns a deep copy of itself """
        return deepcopy(self)

    def lastOffset(self) -> float:
        """ Get Last Note Offset """
        if len(self.data()) == 0: return 0.0
        return sorted(self.data())[-1].tailOffset()

    def firstLastOffset(self) -> Tuple[float, float]:
        """ Get First and Last Note Offset
        This is slightly faster than separately calling the singular functions since it sorts once only
        """
        hos = sorted(self.data())
        return hos[0].offset, hos[-1].tailOffset()

    def multOffset(self, by: float, inplace:bool = False):
        this = self if inplace else self.deepcopy()
        [i.multOffset(by, inplace=True) for i in this.data()]
        return None if inplace else this

    def headOffsets(self) -> List[float]:
        return [obj.offset for obj in self.data()]

    def tailOffsets(self) -> List[float]:
        return [obj.tailOffset() for obj in self.data()]

    def lengths(self) -> List[float]:
        """ Grabs all object lengths as a list """
        return [obj.length for obj in self.data()]
