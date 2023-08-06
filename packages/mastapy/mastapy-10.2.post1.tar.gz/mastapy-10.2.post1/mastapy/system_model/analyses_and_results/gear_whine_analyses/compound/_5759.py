﻿'''_5759.py

KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2100
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5757, _5758, _5756
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5365
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis(_5756.KlingelnbergCycloPalloidConicalGearSetCompoundGearWhineAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2100.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2100.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2100.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2100.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_gear_whine_analysis(self) -> 'List[_5757.KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundGearWhineAnalysis, constructor.new(_5757.KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_gear_whine_analysis(self) -> 'List[_5758.KlingelnbergCycloPalloidHypoidGearMeshCompoundGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundGearWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundGearWhineAnalysis, constructor.new(_5758.KlingelnbergCycloPalloidHypoidGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5365.KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5365.KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5365.KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5365.KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis))
        return value
