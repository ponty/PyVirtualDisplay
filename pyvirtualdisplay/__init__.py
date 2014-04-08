from display import Display
import logging

log = logging.getLogger(__name__)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

log.debug('version=' + __version__)
