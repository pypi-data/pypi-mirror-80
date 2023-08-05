'''_5774.py

PointLoadCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2034
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5381
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5808
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'PointLoadCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundGearWhineAnalysis',)


class PointLoadCompoundGearWhineAnalysis(_5808.VirtualComponentCompoundGearWhineAnalysis):
    '''PointLoadCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2034.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2034.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5381.PointLoadGearWhineAnalysis]':
        '''List[PointLoadGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5381.PointLoadGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5381.PointLoadGearWhineAnalysis]':
        '''List[PointLoadGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5381.PointLoadGearWhineAnalysis))
        return value
