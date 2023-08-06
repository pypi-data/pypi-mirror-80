""" This package handles all BPM Analysis Functions """
from reamber.base.BpmObject import BpmObject
from reamber.base.MapObject import MapObject
from typing import Tuple, List


def bpmActivity(m: MapObject) -> List[Tuple[BpmObject, float]]:
    """ Calculates how long the Bpm is active
    :return A List of Tuples in the format [(BPMPoint, Activity In ms), ...]
    """
    last = m.notes.lastOffset()

    # Describes the BPM and Length of it active
    # e.g. [(120.0, 2000<ms>), (180.0, 1000<ms>), ...]
    bpmLen: List[Tuple[BpmObject, float]] = []

    bpmRev = m.bpms.sorted()
    reversed(bpmRev)
    for bpm in bpmRev:
        if bpm.offset >= last:
            bpmLen.append((bpm, 0.0))  # If the BPM doesn't cover any notes it is inactive
        else:
            bpmLen.append((bpm, last - bpm.offset))
            last = bpm.offset
    return bpmLen


def aveBpm(m: MapObject) -> float:
    """ Calculates the average BPM based on the BPM's Activity on notes """
    activitySum = 0
    sumProd = 0
    for bpm, activity in bpmActivity(m):
        activitySum += activity
        sumProd += bpm.bpm * activity
    return sumProd / activitySum
