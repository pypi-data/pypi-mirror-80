try:
    from pyWmiHandler.wmi_wrapper import WmiHandler
    from pyWmiHandler import helpers
except ModuleNotFoundError:
    from .wmi_wrapper import WmiHandler
    from .helpers import *
