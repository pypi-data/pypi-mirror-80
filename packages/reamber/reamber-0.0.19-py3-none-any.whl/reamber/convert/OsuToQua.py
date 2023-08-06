from reamber.quaver.QuaMapObject import QuaMapObject
from reamber.quaver.QuaMapObjectMeta import QuaMapObjectMode
from reamber.quaver.QuaSvObject import QuaSvObject
from reamber.osu.OsuMapObject import OsuMapObject
from reamber.base.BpmObject import BpmObject
from reamber.base.NoteObject import NoteObject
from reamber.quaver.QuaHitObject import QuaHitObject
from reamber.quaver.QuaHoldObject import QuaHoldObject
from reamber.quaver.QuaBpmObject import QuaBpmObject
from typing import List


class OsuToQua:
    @staticmethod
    def convert(osu: OsuMapObject) -> QuaMapObject:
        """ Converts Osu to a Qua Map
        :param osu: The Osu Map itself
        :return: A SM MapSet
        """
        assert osu.circleSize == 4 or osu.circleSize == 7
        notes: List[NoteObject] = []

        for note in osu.hitObjects():
            notes.append(QuaHitObject(offset=note.offset, column=note.column))
        for note in osu.holdObjects():
            notes.append(QuaHoldObject(offset=note.offset, column=note.column, length=note.length))

        bpms: List[BpmObject] = []
        svs: List[QuaSvObject] = []

        for bpm in osu.bpmPoints:
            bpms.append(QuaBpmObject(offset=bpm.offset, bpm=bpm.bpm))

        for sv in osu.svs:
            svs.append(QuaSvObject(offset=sv.offset, multiplier=sv.multiplier))

        qua: QuaMapObject = QuaMapObject(
            audioFile=osu.audioFileName,
            title=osu.titleUnicode,
            mode=QuaMapObjectMode.str(int(osu.circleSize)),
            artist=osu.artistUnicode,
            creator=osu.creator,
            backgroundFile=osu.backgroundFileName,
            songPreviewTime=osu.previewTime,
            noteObjects=notes,
            bpmPoints=bpms,
            svPoints=svs
        )

        return qua
