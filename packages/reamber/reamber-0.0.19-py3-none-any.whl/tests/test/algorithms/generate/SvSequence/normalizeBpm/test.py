import unittest

from reamber.algorithms.generate.sv.generators.svNormalizeBpm import svNormalizeBpm
from reamber.base.lists.BpmList import BpmList, Bpm


class TestNormalize(unittest.TestCase):

    def testNormalize(self):
        seq = svNormalizeBpm(BpmList([Bpm(0, 200), Bpm(100, 50), Bpm(300, 100)]), 100)
        self.assertAlmostEqual(seq[0].multiplier, 0.5)
        self.assertAlmostEqual(seq[1].multiplier, 2.0)
        self.assertAlmostEqual(seq[2].multiplier, 1.0)


if __name__ == '__main__':
    unittest.main()
