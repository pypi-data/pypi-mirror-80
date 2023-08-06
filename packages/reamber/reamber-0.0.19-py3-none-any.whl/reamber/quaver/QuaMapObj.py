from reamber.quaver.QuaMapObjMeta import QuaMapObjMeta
from reamber.base.MapObj import MapObj
from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaSvObj import QuaSvObj
from reamber.quaver.QuaBpmObj import QuaBpmObj
from reamber.quaver.QuaHitObj import QuaHitObj
from reamber.quaver.QuaHoldObj import QuaHoldObj
from dataclasses import dataclass, field
from typing import List, Dict, Union
import yaml
from yaml import CLoader as Loader, CDumper as Dumper

from reamber.quaver.lists.QuaNotePkg import QuaNotePkg
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.QuaSvList import QuaSvList


@dataclass
class QuaMapObj(QuaMapObjMeta, MapObj):

    notes: QuaNotePkg = field(default_factory=lambda: QuaNotePkg())
    bpms:  QuaBpmList = field(default_factory=lambda: QuaBpmList())
    svs:   QuaSvList  = field(default_factory=lambda: QuaSvList())

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes, bpms and svs as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms,
                'svs': self.svs}

    def readFile(self, filePath: str):
        """ Reads a .qua, loads inplace, hence it doesn't return anything

        :param filePath: The path to the .qua file."""

        self.__init__()

        with open(filePath, "r", encoding="utf8") as f:
            # Reading with CReader is much faster
            file = yaml.load(f, Loader=Loader)
        # We pop them so as to reduce the size needed to pass to _readMeta
        self._readNotes(file.pop('HitObjects'))
        self._readBpms(file.pop('TimingPoints'))
        self._readSVs(file.pop('SliderVelocities'))
        self._readMetadata(file)

    def writeFile(self, filePath: str):
        """ Writes a .qua, doesn't return anything.

        :param filePath: The path to a new .qua file."""
        file = self._writeMeta()

        bpm: QuaBpmObj
        file['TimingPoints'] = [bpm.asDict() for bpm in self.bpms]
        sv: QuaSvObj
        file['SliderVelocities'] = [sv.asDict() for sv in self.svs]
        note: Union[QuaHitObj, QuaHoldObj]

        # This long comprehension squishes the hits: {} and holds: {} to a list for asDict operation
        # noinspection PyTypeChecker
        file['HitObjects'] = [i.asDict() for j in [v for k, v in self.notes.data().items()] for i in j]
        with open(filePath, "w+", encoding="utf8") as f:
            # Writing with CDumper is much faster
            f.write(yaml.dump(file, default_flow_style=False, sort_keys=False, Dumper=Dumper))

    def _readBpms(self, bpms: List[Dict]):
        for bpm in bpms:
            self.bpms.append(QuaBpmObj(offset=bpm['StartTime'], bpm=bpm['Bpm']))

    def _readSVs(self, svs: List[Dict]):
        for sv in svs:
            self.svs.append(QuaSvObj(offset=sv['StartTime'], multiplier=sv['Multiplier']))

    def _readNotes(self, notes: List[Dict]):
        for note in notes:
            offset = note['StartTime']
            column = note['Lane'] - 1
            keySounds = note['KeySounds']
            if "EndTime" in note.keys():
                self.notes.holds().append(QuaHoldObj(offset=offset, length=note['EndTime'] - offset,
                                                      column=column, keySounds=keySounds))
            else:
                self.notes.hits().append(QuaHitObj(offset=offset, column=column, keySounds=keySounds))
