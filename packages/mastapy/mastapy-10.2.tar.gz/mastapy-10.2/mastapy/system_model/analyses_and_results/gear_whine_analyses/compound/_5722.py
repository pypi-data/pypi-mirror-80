'''_5722.py

ConceptGearMeshCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1885
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5307
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5746
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'ConceptGearMeshCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshCompoundGearWhineAnalysis',)


class ConceptGearMeshCompoundGearWhineAnalysis(_5746.GearMeshCompoundGearWhineAnalysis):
    '''ConceptGearMeshCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1885.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1885.ConceptGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1885.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1885.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5307.ConceptGearMeshGearWhineAnalysis]':
        '''List[ConceptGearMeshGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5307.ConceptGearMeshGearWhineAnalysis))
        return value

    @property
    def connection_gear_whine_analysis_load_cases(self) -> 'List[_5307.ConceptGearMeshGearWhineAnalysis]':
        '''List[ConceptGearMeshGearWhineAnalysis]: 'ConnectionGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionGearWhineAnalysisLoadCases, constructor.new(_5307.ConceptGearMeshGearWhineAnalysis))
        return value
