'''_3438.py

OilSealCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2029
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3314
from mastapy.system_model.analyses_and_results.power_flows.compound import _3400
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'OilSealCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundPowerFlow',)


class OilSealCompoundPowerFlow(_3400.ConnectorCompoundPowerFlow):
    '''OilSealCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2029.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2029.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3314.OilSealPowerFlow]':
        '''List[OilSealPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3314.OilSealPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3314.OilSealPowerFlow]':
        '''List[OilSealPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3314.OilSealPowerFlow))
        return value
