import unittest

from reamber.algorithms.convert.QuaToSM import QuaToSM
from reamber.quaver.QuaMap import QuaMap
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestQuaToSM(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        qua = QuaMap.readFile(QUA_NEURO_CLOUD)

        sm = QuaToSM.convert(qua)
        # sm.writeFile("out.sm")


if __name__ == '__main__':
    unittest.main()
