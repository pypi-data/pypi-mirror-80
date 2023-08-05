'''_6382.py

UseVariableBearingStiffnessOptions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_USE_VARIABLE_BEARING_STIFFNESS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'UseVariableBearingStiffnessOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('UseVariableBearingStiffnessOptions',)


class UseVariableBearingStiffnessOptions(Enum):
    '''UseVariableBearingStiffnessOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _USE_VARIABLE_BEARING_STIFFNESS_OPTIONS

    __hash__ = None

    YES = 0
    NO = 1
    SPECIFY_FOR_EACH_BEARING = 2


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


UseVariableBearingStiffnessOptions.__setattr__ = __enum_setattr
UseVariableBearingStiffnessOptions.__delattr__ = __enum_delattr
