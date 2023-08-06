import logging

from isilon.__version__ import __version__
from isilon.client import IsilonClient

logging.getLogger("isilon-client").addHandler(logging.NullHandler())
