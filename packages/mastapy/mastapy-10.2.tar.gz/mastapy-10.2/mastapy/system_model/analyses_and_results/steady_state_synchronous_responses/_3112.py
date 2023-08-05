'''_3112.py

ZerolBevelGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2115
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6243
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3113, _3111, _3004
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ZerolBevelGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetSteadyStateSynchronousResponse',)


class ZerolBevelGearSetSteadyStateSynchronousResponse(_3004.BevelGearSetSteadyStateSynchronousResponse):
    '''ZerolBevelGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2115.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2115.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6243.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6243.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_steady_state_synchronous_response(self) -> 'List[_3113.ZerolBevelGearSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSteadyStateSynchronousResponse]: 'ZerolBevelGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsSteadyStateSynchronousResponse, constructor.new(_3113.ZerolBevelGearSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_meshes_steady_state_synchronous_response(self) -> 'List[_3111.ZerolBevelGearMeshSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearMeshSteadyStateSynchronousResponse]: 'ZerolBevelMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesSteadyStateSynchronousResponse, constructor.new(_3111.ZerolBevelGearMeshSteadyStateSynchronousResponse))
        return value
