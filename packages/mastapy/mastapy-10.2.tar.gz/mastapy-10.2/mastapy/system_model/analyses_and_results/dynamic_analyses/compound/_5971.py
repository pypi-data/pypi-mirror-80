'''_5971.py

ConceptCouplingCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2138
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5849
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _5982
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ConceptCouplingCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingCompoundDynamicAnalysis',)


class ConceptCouplingCompoundDynamicAnalysis(_5982.CouplingCompoundDynamicAnalysis):
    '''ConceptCouplingCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2138.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2138.ConceptCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2138.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2138.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5849.ConceptCouplingDynamicAnalysis]':
        '''List[ConceptCouplingDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5849.ConceptCouplingDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_5849.ConceptCouplingDynamicAnalysis]':
        '''List[ConceptCouplingDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_5849.ConceptCouplingDynamicAnalysis))
        return value
