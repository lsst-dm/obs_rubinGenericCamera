__all__ = ["StarTrackerRawFormatter",  "StarTrackerWideRawFormatter",  "StarTrackerFastRawFormatter",]

from .translator import *
from lsst.obs.base import FitsRawFormatterBase
from .filters import RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS
from . import *

class RubinGenericCameraRawFormatter(FitsRawFormatterBase):
    cameraClass = None
    translatorClass = None
    filterDefinitions = RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS

    def getDetector(self, id):
        return self.cameraClass().getCamera()[id]

    def makeWcs(self, visitInfo, detector):
        """Create a SkyWcs from information about the exposure.

        If VisitInfo is not None, use it and the detector to create a SkyWcs,
        otherwise return the metadata-based SkyWcs (always created, so that
        the relevant metadata keywords are stripped).

        Parameters
        ----------
        visitInfo : `~lsst.afw.image.VisitInfo`
            The information about the telescope boresight and camera
            orientation angle for this exposure.
        detector : `~lsst.afw.cameraGeom.Detector`
            The detector used to acquire this exposure.

        Returns
        -------
        skyWcs : `~lsst.afw.geom.SkyWcs`
            Reversible mapping from pixel coordinates to sky coordinates.

        Raises
        ------
        InitialSkyWcsError
            Raised if there is an error generating the SkyWcs, chained from the
            lower-level exception if available.
        """
        if not self.isOnSky():
            # This is not an on-sky observation
            return None

        if visitInfo is None:
            msg = "No VisitInfo; cannot access boresight information. Defaulting to metadata-based SkyWcs."
            log.warning(msg)
            skyWcs = self._createSkyWcsFromMetadata()
            if skyWcs is None:
                raise InitialSkyWcsError(
                    "Failed to create both metadata and boresight-based SkyWcs."
                    "See warnings in log messages for details."
                )
            return skyWcs

        return self.makeRawSkyWcsFromBoresight(
            visitInfo.getBoresightRaDec(), visitInfo.getBoresightRotAngle(), detector
        )


class StarTrackerRawFormatter(RubinGenericCameraRawFormatter):
    cameraClass = StarTracker
    translatorClass = StarTrackerTranslator


class StarTrackerWideRawFormatter(RubinGenericCameraRawFormatter):
    cameraClass = StarTrackerWide
    translatorClass = StarTrackerWideTranslator


class StarTrackerFastRawFormatter(RubinGenericCameraRawFormatter):
    cameraClass = StarTrackerFast
    translatorClass = StarTrackerFastTranslator


class FiberSpectrographRawFormatter(RubinGenericCameraRawFormatter):
    cameraClass = FiberSpectrograph
    translatorClass = FiberSpectrographTranslator
