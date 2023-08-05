'''_5919.py

SpiralBevelGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2105
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6209
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5917, _5918, _5840
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'SpiralBevelGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetDynamicAnalysis',)


class SpiralBevelGearSetDynamicAnalysis(_5840.BevelGearSetDynamicAnalysis):
    '''SpiralBevelGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetDynamicAnalysis.TYPE'):
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
    def spiral_bevel_gears_dynamic_analysis(self) -> 'List[_5917.SpiralBevelGearDynamicAnalysis]':
        '''List[SpiralBevelGearDynamicAnalysis]: 'SpiralBevelGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsDynamicAnalysis, constructor.new(_5917.SpiralBevelGearDynamicAnalysis))
        return value

    @property
    def spiral_bevel_meshes_dynamic_analysis(self) -> 'List[_5918.SpiralBevelGearMeshDynamicAnalysis]':
        '''List[SpiralBevelGearMeshDynamicAnalysis]: 'SpiralBevelMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesDynamicAnalysis, constructor.new(_5918.SpiralBevelGearMeshDynamicAnalysis))
        return value
