__version__ = '6.0.11'

from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)
from .check_tagged import *
from .commons import *
from .update_req_versions import *
from .check_not_dirty import *
from .version_check import *
