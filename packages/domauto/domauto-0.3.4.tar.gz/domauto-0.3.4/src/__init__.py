import sys, pathlib
from pkg_resources import get_distribution, DistributionNotFound

try:
    version = get_distribution(__name__).version
except DistributionNotFound:
    version = "unknown version"

from .crawler        import crawler
from .status_plotter import status_plotter
from .scp_plotter    import scp_plotter
#from .web_maker      import web_maker
from .SC_PARAMETERS  import SC_PARAMETERS
