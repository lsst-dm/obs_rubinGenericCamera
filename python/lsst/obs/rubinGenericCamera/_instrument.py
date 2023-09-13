# This file is part of obs_rubinGenericCamera
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ("RubinGenericCamera", "StarTracker", "StarTrackerWide", "StarTrackerFast", "FiberSpectrograph")

import os.path

import lsst.obs.base.yamlCamera as yamlCamera
from lsst.utils.introspection import get_full_type_name
from lsst.utils import getPackageDir
from lsst.obs.base import VisitSystem
from lsst.obs.lsst import LsstCam
from .filters import RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS

from .translator import *

PACKAGE_DIR = getPackageDir("obs_rubinGenericCamera")


class RubinGenericCamera(LsstCam):
    """Gen3 Butler specialization for the Rubin Generic Cameras

    Parameters
    ----------
    camera : `lsst.cameraGeom.Camera`
        Camera object from which to extract detector information.
    filters : `list` of `FilterDefinition`
        An ordered list of filters to define the set of PhysicalFilters
        associated with this instrument in the registry.

    While both the camera geometry and the set of filters associated with a
    camera are expected to change with time in general, their Butler Registry
    representations defined by an Instrument do not.  Instead:

     - We only extract names, IDs, and purposes from the detectors in the
       camera, which should be static information that actually reflects
       detector "slots" rather than the physical sensors themselves.  Because
       the distinction between physical sensors and slots is unimportant in
       the vast majority of Butler use cases, we just use "detector" even
       though the concept really maps better to "detector slot".  Ideally in
       the future this distinction between static and time-dependent
       information would be encoded in cameraGeom itself (e.g. by making the
       time-dependent Detector class inherit from a related class that only
       carries static content).

     - The Butler Registry is expected to contain physical_filter entries for
       all filters an instrument has ever had, because we really only care
       about which filters were used for particular observations, not which
       filters were *available* at some point in the past.  And changes in
       individual filters over time will be captured as changes in their
       TransmissionCurve datasets, not changes in the registry content (which
       is really just a label).  While at present Instrument and Registry
       do not provide a way to add new physical_filters, they will in the
       future.
    """
    filterDefinitions = RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS
    instrument = None                   # you must specialise this class
    policyName = None                   # you must specialise this class
    translatorClass = None              # you must specialise this class
    visitSystem = VisitSystem.BY_SEQ_START_END

    @classmethod
    def getCamera(cls):
        # Constructing a YAML camera takes a long time but we rely on
        # yamlCamera to cache for us.
        # N.b. can't inherit as PACKAGE_DIR isn't in the class 
        cameraYamlFile = os.path.join(PACKAGE_DIR, "policy", f"{cls.policyName}.yaml")
        return yamlCamera.makeCamera(cameraYamlFile)

    def getRawFormatter(self, dataId):
        return None

    def extractDetectorRecord(self, camGeomDetector):
        """Create a Gen3 Detector entry dict from a cameraGeom.Detector.
        """
        return dict(
            instrument=self.getName(),
            id=camGeomDetector.getId(),
            full_name=camGeomDetector.getName(),
        )


class StarTracker(RubinGenericCamera):
    """Gen3 Butler specialization of the Rubin Generic Camera for the narrow-field StarTracker

    Parameters
    ----------
    camera : `lsst.cameraGeom.Camera`
        Camera object from which to extract detector information.
    filters : `list` of `FilterDefinition`
        An ordered list of filters to define the set of PhysicalFilters
        associated with this instrument in the registry.
    """
    instrument = "StarTracker"
    policyName = "starTracker"
    translatorClass = StarTrackerTranslator

    def getRawFormatter(self, dataId):
        # Docstring inherited from Instrument.getRawFormatter
        # local import to prevent circular dependency
        from .rawFormatter import StarTrackerRawFormatter
        return StarTrackerRawFormatter


class StarTrackerWide(StarTracker):
    """Gen3 Butler specialization of the Rubin Generic Camera for the wide-field StarTracker

    Parameters
    ----------
    camera : `lsst.cameraGeom.Camera`
        Camera object from which to extract detector information.
    filters : `list` of `FilterDefinition`
        An ordered list of filters to define the set of PhysicalFilters
        associated with this instrument in the registry.
    """
    instrument = "StarTrackerWide"
    policyName = "starTrackerWide"
    translatorClass = StarTrackerWideTranslator

    def getRawFormatter(self, dataId):
        # Docstring inherited from Instrument.getRawFormatter
        # local import to prevent circular dependency
        from .rawFormatter import StarTrackerWideRawFormatter
        return StarTrackerWideRawFormatter


class StarTrackerFast(StarTracker):
    """Gen3 Butler specialization of the Rubin Generic Camera for the high-cadence Star Tracker

    Parameters
    ----------
    camera : `lsst.cameraGeom.Camera`
        Camera object from which to extract detector information.
    filters : `list` of `FilterDefinition`
        An ordered list of filters to define the set of PhysicalFilters
        associated with this instrument in the registry.
    """
    instrument = "StarTrackerFast"
    policyName = "starTrackerFast"
    translatorClass = StarTrackerFastTranslator

    def getRawFormatter(self, dataId):
        # Docstring inherited from Instrument.getRawFormatter
        # local import to prevent circular dependency
        from .rawFormatter import StarTrackerFastRawFormatter
        return StarTrackerFastRawFormatter


class FiberSpectrograph(RubinGenericCamera):
    """Gen3 Butler specialization of the Rubin Generic Camera for the fiber spectrograph

    Parameters
    ----------
    camera : `lsst.cameraGeom.Camera`
        Camera object from which to extract detector information.
    filters : `list` of `FilterDefinition`
        An ordered list of filters to define the set of PhysicalFilters
        associated with this instrument in the registry.
    """
    instrument = "FiberSpec"
    policyName = "fiberSpectrograph"
    translatorClass = FiberSpectrographTranslator

    def getRawFormatter(self, dataId):
        # Docstring inherited from Instrument.getRawFormatter
        # local import to prevent circular dependency
        from .rawFormatter import FiberSpectrographRawFormatter
        return FiberSpectrographRawFormatter
