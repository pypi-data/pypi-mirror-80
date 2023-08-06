from .interfaceutils import interfaceutils

from .jumaUtils import jumaUtils
from .commonkeywords import commonkeywords
from SeleniumLibrary.base.robotlibcore import DynamicCore
from .initLib import initlib

__verison__ = "1.0.0"


# class cmutillib(DynamicCore):
#     ROBOT_LIBRARY_SCOPE = 'GLOBAL'
#     ROBOT_LIBRARY_VERSION = __verison__
#
#     def __init__(self):
#         libraries = [
#             commonkeywords(self),
#             jumaUtils(self),
#             interfaceutils(self)
#         ]
#         DynamicCore.__init__(self, libraries)
class cmutillib(jumaUtils, commonkeywords, interfaceutils):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __verison__