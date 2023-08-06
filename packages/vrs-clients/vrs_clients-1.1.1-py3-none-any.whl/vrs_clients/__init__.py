__version__ = "1.1.1"

__all__ = ["PlotlyVisualizationResourceClient", "VisualizationResourceClient"]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from .vrs_clients import (
        PlotlyVisualizationResourceClient,
        VisualizationResourceClient,
    )
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
