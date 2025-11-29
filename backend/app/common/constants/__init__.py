from typing import List

# Import submodules as module objects so we can safely build __all__ from them
from . import constants as _constants
from . import protocol_constants as _protocol_constants
from . import port_constants as _port_constants
from . import scan_constants as _scan_constants
from . import mac_constants as _mac_constants
from . import ping_constants as _ping_constants
from . import discovery_constants as _discovery_constants
from . import scanning_constants as _scanning_constants

# Re-export all names from each submodule into the package namespace
from .constants import *
from .protocol_constants import *
from .port_constants import *
from .scan_constants import *
from .mac_constants import *
from .ping_constants import *
from .discovery_constants import *
from .scanning_constants import *

__all__: List[str] = []
for mod in (
    _constants,
    _protocol_constants,
    _port_constants,
    _scan_constants,
    _mac_constants,
    _ping_constants,
    _discovery_constants,
    _scanning_constants,
):
    # Prefer explicit __all__ from the module; otherwise include public names
    mod_all = getattr(mod, "__all__", None)
    if mod_all:
        __all__ += list(mod_all)  # type: ignore[arg-type]
    else:
        __all__ += [n for n in dir(mod) if not n.startswith("_")]
