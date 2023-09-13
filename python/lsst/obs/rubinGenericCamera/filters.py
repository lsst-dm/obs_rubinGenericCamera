from lsst.obs.base import FilterDefinition, FilterDefinitionCollection

RUBIN_GENERIC_CAMERA_FILTER_DEFINITIONS = FilterDefinitionCollection(
    FilterDefinition(band="empty", physical_filter="empty"),
)
