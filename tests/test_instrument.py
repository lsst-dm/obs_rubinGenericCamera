"""Tests of the RubinGenericCamera instrument class.
"""

import unittest

import lsst.utils.tests
import lsst.obs.rubinGenericCamera
from lsst.obs.base.instrument_tests import InstrumentTests, InstrumentTestData


class TestStarTracker(InstrumentTests, lsst.utils.tests.TestCase):
    def setUp(self):
        physical_filters = set(["empty"])

        self.data = InstrumentTestData(name="StarTracker",
                                       nDetectors=1,
                                       firstDetectorName="0",
                                       physical_filters=physical_filters)
        self.instrument = lsst.obs.rubinGenericCamera.StarTracker()

if __name__ == '__main__':
    lsst.utils.tests.init()
    unittest.main()
