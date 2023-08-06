from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuSvObject import OsuSvObject
from typing import List


class OsuMapObjectSvs(List[OsuSvObject], TimedList):

    def data(self) -> List[OsuSvObject]:
        return self

    def multipliers(self) -> List[float]:
        return self.attribute('multiplier')
