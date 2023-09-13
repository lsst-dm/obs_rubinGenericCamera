"""Unit tests for Gen3 RubinGC raw data ingest.
"""

import unittest
import os
import lsst.utils.tests

from lsst.obs.base.ingest_tests import IngestTestBase
from lsst.obs.rubinGenericCamera import StarTracker
from lsst.obs.rubinGenericCamera.filters import RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS

testDataPackage = "testdata_rubinGenericCamera"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except (LookupError, lsst.pex.exceptions.NotFoundError):
    testDataDirectory = None


#@unittest.skipIf(testDataDirectory is None, "testdata_example must be set up")
class StarTrackerIngestTestCase(IngestTestBase, lsst.utils.tests.TestCase):
    instrumentClassName = "lsst.obs.rubinGenericCamera.StarTracker"

    visits = None                       # we don't have a definition of visits

    def setUp(self):
        self.ingestdir = os.path.dirname(__file__)
        self.instrument = StarTracker()
        if testDataDirectory:
            self.file = os.path.join(testDataDirectory, "example", "raw", "somefile.fits.gz")
        else:
            self.file = os.path.join(os.path.expanduser("~rlupton"),
                                     "Data", "RubinGenericCamera", "raw", "102", "2022-12-08",
                                     "GC102_O_20221208_000211.fits")
        self.dataIds = [dict(instrument="StarTracker", exposure=2022120800211, detector=0)]
        self.filterLabel = RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS[0].makeFilterLabel()

        super().setUp()


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
