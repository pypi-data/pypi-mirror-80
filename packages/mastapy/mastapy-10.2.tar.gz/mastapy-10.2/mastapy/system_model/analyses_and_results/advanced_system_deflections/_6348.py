'''_6348.py

PowerLoadAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2035
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6195
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6380, _6383
from mastapy.system_model.analyses_and_results.system_deflections import _2323
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'PowerLoadAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadAdvancedSystemDeflection',)


class PowerLoadAdvancedSystemDeflection(_6383.VirtualComponentAdvancedSystemDeflection):
    '''PowerLoadAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2035.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2035.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6195.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6195.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def transmission_error_to_other_power_loads(self) -> 'List[_6380.TransmissionErrorToOtherPowerLoad]':
        '''List[TransmissionErrorToOtherPowerLoad]: 'TransmissionErrorToOtherPowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TransmissionErrorToOtherPowerLoads, constructor.new(_6380.TransmissionErrorToOtherPowerLoad))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2323.PowerLoadSystemDeflection]':
        '''List[PowerLoadSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2323.PowerLoadSystemDeflection))
        return value
