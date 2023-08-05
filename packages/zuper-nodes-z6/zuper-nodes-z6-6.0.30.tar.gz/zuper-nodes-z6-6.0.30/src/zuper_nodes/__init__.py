__version__ = "6.0.30"

from zuper_commons.logs import ZLogger


logger = ZLogger(__name__)

logger.info(f"version: {__version__}")

from .language import *

from .language_parse import *
from .language_recognize import *

from .structures import *
from .compatibility import *
