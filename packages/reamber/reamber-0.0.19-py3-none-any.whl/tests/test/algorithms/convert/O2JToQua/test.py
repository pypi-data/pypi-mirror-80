import unittest

from reamber.algorithms.convert.O2JToQua import O2JToQua
from reamber.o2jam.O2JMapSet import O2JMapSet
from tests.test.RSC_PATHS import *


# import logging
#
# logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)


class TestO2JToQua(unittest.TestCase):

    # @profile
    def test(self):
        # Complex BPM Points
        o2j = O2JMapSet.readFile(O2J_FLY_MAGPIE_OJN)

        quas = O2JToQua.convert(o2j)
        # osus[0].writeFile("out.osu")
        # osus[1].writeFile("out.osu")
        # osus[2].writeFile("out.osu")


if __name__ == '__main__':
    unittest.main()
