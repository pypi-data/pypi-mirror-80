'''_4094.py

StraightBevelDiffGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2107
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6216
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4093, _4092, _4007
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'StraightBevelDiffGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetModalAnalysesAtSpeeds',)


class StraightBevelDiffGearSetModalAnalysesAtSpeeds(_4007.BevelGearSetModalAnalysesAtSpeeds):
    '''StraightBevelDiffGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2107.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2107.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6216.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6216.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_diff_gears_modal_analyses_at_speeds(self) -> 'List[_4093.StraightBevelDiffGearModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearModalAnalysesAtSpeeds]: 'StraightBevelDiffGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsModalAnalysesAtSpeeds, constructor.new(_4093.StraightBevelDiffGearModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_diff_meshes_modal_analyses_at_speeds(self) -> 'List[_4092.StraightBevelDiffGearMeshModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearMeshModalAnalysesAtSpeeds]: 'StraightBevelDiffMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesModalAnalysesAtSpeeds, constructor.new(_4092.StraightBevelDiffGearMeshModalAnalysesAtSpeeds))
        return value
