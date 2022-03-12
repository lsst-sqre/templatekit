from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("templatekit").version
except DistributionNotFound:
    # package is not installed
    pass

from .jinjaext import TemplatekitExtension
