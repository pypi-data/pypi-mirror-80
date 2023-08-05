'''_2466.py

RootAssemblyCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections.compound import _2425, _2384
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3452
from mastapy.system_model.imported_fes import _1986
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'RootAssemblyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundSystemDeflection',)


class RootAssemblyCompoundSystemDeflection(_2384.AssemblyCompoundSystemDeflection):
    '''RootAssemblyCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_efficiency_results(self) -> '_2425.DutyCycleEfficiencyResults':
        '''DutyCycleEfficiencyResults: 'DutyCycleEfficiencyResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2425.DutyCycleEfficiencyResults)(self.wrapped.DutyCycleEfficiencyResults) if self.wrapped.DutyCycleEfficiencyResults else None

    @property
    def root_assembly_compound_power_flow(self) -> '_3452.RootAssemblyCompoundPowerFlow':
        '''RootAssemblyCompoundPowerFlow: 'RootAssemblyCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3452.RootAssemblyCompoundPowerFlow)(self.wrapped.RootAssemblyCompoundPowerFlow) if self.wrapped.RootAssemblyCompoundPowerFlow else None

    @property
    def bearing_race_fes(self) -> 'List[_1986.RaceBearingFESystemDeflection]':
        '''List[RaceBearingFESystemDeflection]: 'BearingRaceFEs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BearingRaceFEs, constructor.new(_1986.RaceBearingFESystemDeflection))
        return value
