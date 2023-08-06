import pkg_resources

__version__ = pkg_resources.get_distribution('ddconst').version

from . import plotting
