__version__ = "1.1.1"

__all__ = ["ChartImageServicePlotlyClient"]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from .plotly_client import ChartImageServicePlotlyClient
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
