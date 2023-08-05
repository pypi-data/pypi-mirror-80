'''_3349.py

SynchroniserHalfPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows import _3260, _3350
from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2159
from mastapy.system_model.analyses_and_results.static_loads import _6222
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SynchroniserHalfPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfPowerFlow',)


class SynchroniserHalfPowerFlow(_3350.SynchroniserPartPowerFlow):
    '''SynchroniserHalfPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def clutch_connection(self) -> '_3260.ClutchConnectionPowerFlow':
        '''ClutchConnectionPowerFlow: 'ClutchConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3260.ClutchConnectionPowerFlow)(self.wrapped.ClutchConnection) if self.wrapped.ClutchConnection else None

    @property
    def component_design(self) -> '_2159.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2159.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6222.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6222.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
