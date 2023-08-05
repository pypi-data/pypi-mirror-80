'''_6015.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2102
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6013, _6014, _6009
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5894
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis(_6009.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2102.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2102.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2102.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2102.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_dynamic_analysis(self) -> 'List[_6013.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundDynamicAnalysis, constructor.new(_6013.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_dynamic_analysis(self) -> 'List[_6014.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundDynamicAnalysis, constructor.new(_6014.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5894.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5894.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_5894.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_5894.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis))
        return value
