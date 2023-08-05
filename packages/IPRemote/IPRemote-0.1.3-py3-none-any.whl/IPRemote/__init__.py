# -*- coding: utf-8 -*-

"""Remote control Samsung televisions via TCP/IP connection"""

import logging
from logging import NullHandler

logger = logging.getLogger('IPRemote')
logger.addHandler(NullHandler())
logging.basicConfig(format="%(message)s", level=None)

__title__ = "IPRemote"
__version__ = "v0.1.3"
__url__ = "https://github.com/MikishVaughn/IPRemote"
__author__ = "Michael Vaughn"
__author_email__ = "mikish.vaughn@gmail.com"
__license__ = "MIT"

from .remote import Remote # NOQA
from .config import Config # NOQA


def discover(timeout=5):
    from .upnp.discover import discover as _discover

    for config in _discover(timeout=timeout):
        yield Remote(config)
