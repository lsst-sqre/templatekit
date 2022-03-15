__all__ = ["TemplatekitExtension", "__version__", "version_info"]

from importlib.metadata import PackageNotFoundError, version

from .jinjaext import TemplatekitExtension

__version__: str
"""The version string of Templatekit (PEP 440 / SemVer compatible)."""

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"

version_info = __version__.split(".")
"""The decomposed version, split across "``.``."

Use this for version comparison.
"""
