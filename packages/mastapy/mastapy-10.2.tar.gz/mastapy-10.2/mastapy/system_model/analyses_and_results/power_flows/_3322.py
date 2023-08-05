'''_3322.py

PointLoadPowerFlow
'''


from mastapy.system_model.part_model import _2034
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6194
from mastapy.system_model.analyses_and_results.power_flows import _3359
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PointLoadPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadPowerFlow',)


class PointLoadPowerFlow(_3359.VirtualComponentPowerFlow):
    '''PointLoadPowerFlow

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2034.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2034.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6194.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6194.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
