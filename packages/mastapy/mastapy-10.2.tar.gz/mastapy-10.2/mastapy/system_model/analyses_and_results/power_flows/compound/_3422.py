﻿'''_3422.py

HypoidGearMeshCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1895
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3297
from mastapy.system_model.analyses_and_results.power_flows.compound import _3369
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'HypoidGearMeshCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshCompoundPowerFlow',)


class HypoidGearMeshCompoundPowerFlow(_3369.AGMAGleasonConicalGearMeshCompoundPowerFlow):
    '''HypoidGearMeshCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1895.HypoidGearMesh':
        '''HypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1895.HypoidGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1895.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1895.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3297.HypoidGearMeshPowerFlow]':
        '''List[HypoidGearMeshPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3297.HypoidGearMeshPowerFlow))
        return value

    @property
    def connection_power_flow_load_cases(self) -> 'List[_3297.HypoidGearMeshPowerFlow]':
        '''List[HypoidGearMeshPowerFlow]: 'ConnectionPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionPowerFlowLoadCases, constructor.new(_3297.HypoidGearMeshPowerFlow))
        return value
