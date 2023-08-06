import unittest

from reamber.algorithms.convert.QuaToBMS import QuaToBMS
from reamber.quaver.QuaMap import QuaMap
from tests.test.RSC_PATHS import *
from reamber.bms.BMSChannel import BMSChannel


import logging

logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestQuaToBMS(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        qua = QuaMap.readFile(QUA_CARRY_ME_AWAY)

        bms = QuaToBMS.convert(qua, moveRightBy=1)
        bms.writeFile('out.bme', BMSChannel.BME)


if __name__ == '__main__':
    unittest.main()
