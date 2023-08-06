'''_3337.py

SpiralBevelGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2105
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6209
from mastapy.gears.rating.spiral_bevel import _204
from mastapy.system_model.analyses_and_results.power_flows import _3336, _3335, _3257
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SpiralBevelGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetPowerFlow',)


class SpiralBevelGearSetPowerFlow(_3257.BevelGearSetPowerFlow):
    '''SpiralBevelGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2105.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2105.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6209.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6209.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_204.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_204.SpiralBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_204.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_204.SpiralBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def gears_power_flow(self) -> 'List[_3336.SpiralBevelGearPowerFlow]':
        '''List[SpiralBevelGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3336.SpiralBevelGearPowerFlow))
        return value

    @property
    def spiral_bevel_gears_power_flow(self) -> 'List[_3336.SpiralBevelGearPowerFlow]':
        '''List[SpiralBevelGearPowerFlow]: 'SpiralBevelGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsPowerFlow, constructor.new(_3336.SpiralBevelGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3335.SpiralBevelGearMeshPowerFlow]':
        '''List[SpiralBevelGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3335.SpiralBevelGearMeshPowerFlow))
        return value

    @property
    def spiral_bevel_meshes_power_flow(self) -> 'List[_3335.SpiralBevelGearMeshPowerFlow]':
        '''List[SpiralBevelGearMeshPowerFlow]: 'SpiralBevelMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesPowerFlow, constructor.new(_3335.SpiralBevelGearMeshPowerFlow))
        return value
