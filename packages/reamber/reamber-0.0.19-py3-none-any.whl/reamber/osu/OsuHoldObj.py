from __future__ import annotations
from reamber.base.HoldObj import HoldObj
from reamber.osu.OsuNoteObjMeta import OsuNoteObjMeta
from dataclasses import dataclass


@dataclass
class OsuHoldObj(HoldObj, OsuNoteObjMeta):
    @staticmethod
    def readString(s: str, keys: int) -> OsuHoldObj or None:
        """ Reads a single line under the [HitObject] Label. This must explicitly be a Hold Object.

        keys must be specified for conversion of code value to actual column."""
        if s.isspace():
            return None

        sComma = s.split(",")
        if len(sComma) < 5:
            return None

        sColon = sComma[-1].split(":")
        if len(sColon) < 6:
            return None

        this = OsuHoldObj()
        this.column = this.xAxisToColumn(int(sComma[0]), keys)
        this.offset = float(sComma[2])
        this.hitsoundSet = int(sComma[4])
        this.length = float(sColon[0]) - this.offset
        this.sampleSet = int(sColon[1])
        this.additionSet = int(sColon[2])
        this.customSet = int(sColon[3])
        this.volume = int(sColon[4])
        this.hitsoundFile = sColon[5]

        return this

    def writeString(self, keys: int) -> str:
        """ Exports a .osu writable string """
        return f"{OsuNoteObjMeta.columnToXAxis(self.column, keys=keys)},{192}," \
               f"{int(self.offset)},{128},{self.hitsoundSet},{int(self.offset + self.length)}:" \
               f"{self.sampleSet}:{self.additionSet}:{self.customSet}:{self.volume}:{self.hitsoundFile}"
