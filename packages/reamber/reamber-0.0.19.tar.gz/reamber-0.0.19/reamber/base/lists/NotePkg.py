from __future__ import annotations

from abc import abstractmethod
from copy import deepcopy
from dataclasses import asdict
from typing import Tuple, List, Dict, Any

import pandas as pd

from reamber.base.Hit import Hit
from reamber.base.Hold import Hold
from reamber.base.lists.notes.HoldList import HoldList
from reamber.base.lists.notes.NoteList import NoteList


class NotePkg:
    """ This Package holds multiple note lists """

    @abstractmethod
    def hits(self) -> List[Hit]: ...

    @abstractmethod
    def holds(self) -> List[Hold]: ...

    @abstractmethod
    def data(self) -> Dict[str, NoteList]:
        """ This grabs the data from inherited instances.
        :rtype: Dict[str, NoteList]
        :return: The inherited instances must return a dictionary of the lists. \
            It is advised to follow the names used in the convention. Such as hit for hits, note for hits and holds.
        """
        ...

    @abstractmethod
    def _upcast(self, dataDict: Dict[str, NoteList]) -> NotePkg:
        """ This just upcasts the current class so that inplace methods can work
        :param dataDict: A dictionary similar to what self.data() outputs
        :rtype: NotePkg
        """
        ...

    def deepcopy(self) -> NotePkg:
        """ Creates a deep copy of itself """
        return deepcopy(self)

    def df(self) -> Dict[str, pd.DataFrame]:
        """ Creates a dict pandas DataFrame by looping through the self.data

        :return: Returns a Dictionary of pd.DataFrames
        """
        # noinspection PyDataclass,PyTypeChecker
        return {key: pd.DataFrame([asdict(obj) for obj in data]) for key, data in self.data().items()}

    def __len__(self) -> int:
        """ Returns the number of lists. For total number of items see objCount() """
        # return sum([len(dataDict) for dataDict in self.data()])
        return len(self.data())

    def __iter__(self):
        """ Yields the Dictionary item by item """
        yield from self.data()

    def objCount(self) -> int:
        """ Returns the total sum number of items in each list. For number of lists use len() """
        return sum([len(data) for data in self.data().values()])

    def method(self, method: str, **kwargs) -> Dict[str, Any]:
        """ Calls each list's method with eval. Specify method with a string.

        :param method: The method to call, the string must be **EXACT**
        :param kwargs: The extra parameter to use
        :return: Returns a Dict as it may not return a NotePkg init-able
        """
        expression = f"_.{method}(" + ",".join([f"{k}={v}" for k, v in kwargs.items()]) + ")"
        asFunc = eval('lambda _: ' + expression)
        return {key: asFunc(_) for key, _ in self.data().items()}

        # The above is faster for some reason
        # return {key: eval(f"_.{method}(" + ",".join([f"{k}={v}" for k, v in kwargs.items()]) + ")")
        #         for key, _ in self.data().items()}

    def addOffset(self, by, inplace: bool = False) -> NotePkg:
        """ Adds Offset to all items

        :param by: The offset to add, in milliseconds
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.method('addOffset', by=by, inplace=True)
        else: return self._upcast(self.method('addOffset', by=by, inplace=False))

    def multOffset(self, by, inplace: bool = False) -> NotePkg:
        """ Multiplies Offset to all items

        :param by: The value to multiply by
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.method('multOffset', by=by, inplace=True)
        else: return self._upcast(self.method('multOffset', by=by, inplace=False))

    def inColumns(self, columns: List[int], inplace: bool = False) -> NotePkg:
        """ Filters by columns for all items

        :param columns: The columns to filter by, as a list
        :param inplace: Whether to just modify this instance or return a modified copy
        :return: Returns a modified copy if not inplace
        """
        if inplace: self.method('inColumns', columns=columns, inplace=True)
        else: return self._upcast(self.method('inColumns', columns=columns, inplace=False))

    def columns(self, flatten:bool = False) -> Dict[str, List[int]] or List[int]:
        """ Gets the columns """
        return [j for i in self.method('columns').values() for j in i] if flatten else self.method('columns')

    def maxColumn(self) -> int:
        """ Gets the maximum column, can be used to determine Key Count if not explicitly stated """
        return max(self.method('maxColumn').values())

    def offsets(self, flatten:bool = False) -> Dict[str, List[float]] or List[float]:
        """ Gets the offsets

        :param flatten: Whether to return a Dict or a flattened float list. Flattening will remove categories.
        """
        return [j for i in self.method('offsets').values() for j in i] if flatten else self.method('offsets')

    def tailOffsets(self, flatten:bool = False):
        """ Gets the tail offsets from all available Hold Lists

        :param flatten: Whether to return a Dict or a flattened float list. Flattening will remove categories.
        """
        # Statement 1 loops through data and finds any Hold List, then does a dict comp
        # Statement 2 does that and flattens it with the outer list comp
        return {k: v.tailOffsets() for k, v in self.data().items() if isinstance(v, HoldList)} if not flatten else \
            [i for j in [v.tailOffsets() for k, v in self.data().items() if isinstance(v, HoldList)] for i in j]

    def firstOffset(self) -> float:
        """ Gets the first offset """
        return min(self.method('firstOffset').values())

    def lastOffset(self) -> float:
        """ Gets the last offset """
        return max(self.method('lastOffset').values())

    def firstLastOffset(self) -> Tuple[float, float]:
        """ Gets the first and last offset, slightly faster because it's only sorted once """
        if len(self.offsets()) == 0: return 0.0, float("inf")
        offsets = sorted([i for j in self.offsets().values() for i in j])  # Flattens the offset list
        return offsets[0], offsets[-1]

    def describeNotes(self, rounding: int = 2):
        """ Describes a single NotePkg

        Prints out Count, Median, 75% quantile and max for each note type

        :param rounding: The decimal rounding
        """
        for s, lis in self.data().items():
            print(s)
            lis.describeNotes(rounding=rounding)

    def rollingDensity(self, window: int = 1000, stride: int = None,
                       firstOffset: float = None, lastOffset: float = None) -> Dict[str, Dict[int, int]]:
        """ Returns the Density List Dictionary

        First offset and last offset is recalculated here in Package to make sure that the indexes are consistent.

        :param window: The window to search in milliseconds.
        :param stride: The stride length of each search in milliseconds, if None, stride = window
        :param firstOffset: The first offset to start search on. If None, firstOffset will be used.
        :param lastOffset: The last offset to end search on. If None, lastOffset will be used. \
            (The search will intentionally exceed if it doesn't fit.)
        :return: Dictionary of offset as key and count as value
        """
        return self.method('rollingDensity', window=window, stride=stride,
                           firstOffset=firstOffset if firstOffset else self.firstOffset(),
                           lastOffset=lastOffset if lastOffset else self.lastOffset())

    def duration(self):
        """ Gets the duration of this package. """
        return self.lastOffset() - self.firstOffset()
