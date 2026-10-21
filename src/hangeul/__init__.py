__version__ = "0.2.0"

from .check import (
    is_han,
    is_pure_han,
    has_batchim,
    can_cho,
    can_jung,
    can_jong,
)
from .core import (
    assemble,
    disassemble,
    qwerty2han,
)
from .josa import (
    get_josa,
    attach,
)
from .search import (
    matches,
    get_chosung,
    search_filter,
)
from .constants import (
    CHOSOENG,
    JUNGSOENG,
    JONGSOENG,
)
from .similarity import similarity
from .number import num2han


__all__: list[str] = [
    # Metadata
    "__version__",
    # Check API
    "is_han",
    "is_pure_han",
    "has_batchim",
    "can_cho",
    "can_jung",
    "can_jong",
    # Core API
    "assemble",
    "disassemble",
    "qwerty2han",
    # Josa API
    "get_josa",
    "josa",
    "attach",
    # Search API
    "matches",
    "get_chosung",
    "search_filter",
    # Constants
    "CHOSOENG",
    "JUNGSOENG",
    "JONGSOENG",
    "similarity",
    "num2han",
]
