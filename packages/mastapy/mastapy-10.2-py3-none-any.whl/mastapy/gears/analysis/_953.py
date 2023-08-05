'''_953.py

GearImplementationDetail
'''


from mastapy.utility.scripting import _1270
from mastapy._internal import constructor
from mastapy.gears.analysis import _950
from mastapy._internal.python_net import python_net_import

_GEAR_IMPLEMENTATION_DETAIL = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearImplementationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('GearImplementationDetail',)


class GearImplementationDetail(_950.GearDesignAnalysis):
    '''GearImplementationDetail

    This is a mastapy class.
    '''

    TYPE = _GEAR_IMPLEMENTATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearImplementationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def user_specified_data(self) -> '_1270.UserSpecifiedData':
        '''UserSpecifiedData: 'UserSpecifiedData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1270.UserSpecifiedData)(self.wrapped.UserSpecifiedData) if self.wrapped.UserSpecifiedData else None
