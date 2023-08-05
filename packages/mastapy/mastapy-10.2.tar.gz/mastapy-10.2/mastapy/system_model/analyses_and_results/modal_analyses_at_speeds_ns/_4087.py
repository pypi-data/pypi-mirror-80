'''_4087.py

SpiralBevelGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2105
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6209
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4086, _4085, _4007
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'SpiralBevelGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetModalAnalysesAtSpeeds',)


class SpiralBevelGearSetModalAnalysesAtSpeeds(_4007.BevelGearSetModalAnalysesAtSpeeds):
    '''SpiralBevelGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetModalAnalysesAtSpeeds.TYPE'):
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
    def spiral_bevel_gears_modal_analyses_at_speeds(self) -> 'List[_4086.SpiralBevelGearModalAnalysesAtSpeeds]':
        '''List[SpiralBevelGearModalAnalysesAtSpeeds]: 'SpiralBevelGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsModalAnalysesAtSpeeds, constructor.new(_4086.SpiralBevelGearModalAnalysesAtSpeeds))
        return value

    @property
    def spiral_bevel_meshes_modal_analyses_at_speeds(self) -> 'List[_4085.SpiralBevelGearMeshModalAnalysesAtSpeeds]':
        '''List[SpiralBevelGearMeshModalAnalysesAtSpeeds]: 'SpiralBevelMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesModalAnalysesAtSpeeds, constructor.new(_4085.SpiralBevelGearMeshModalAnalysesAtSpeeds))
        return value
