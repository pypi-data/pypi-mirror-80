﻿'''_4055.py

KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtSpeeds
'''


from mastapy.system_model.connections_and_sockets.gears import _1899
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6172
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4052
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtSpeeds',)


class KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtSpeeds(_4052.KlingelnbergCycloPalloidConicalGearMeshModalAnalysesAtSpeeds):
    '''KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1899.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1899.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6172.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6172.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
