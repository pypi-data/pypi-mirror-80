'''_5085.py

PulleyMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import _2146, _2143
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6196, _6119
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5133
from mastapy.system_model.analyses_and_results.mbd_analyses import _5030
from mastapy._internal.python_net import python_net_import

_PULLEY_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'PulleyMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyMultiBodyDynamicsAnalysis',)


class PulleyMultiBodyDynamicsAnalysis(_5030.CouplingHalfMultiBodyDynamicsAnalysis):
    '''PulleyMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pulley_torque(self) -> 'List[float]':
        '''List[float]: 'PulleyTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.PulleyTorque)
        return value

    @property
    def component_design(self) -> '_2146.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6196.PulleyLoadCase':
        '''PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6196.PulleyLoadCase.TYPE not in self.wrapped.ComponentLoadCase.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to PulleyLoadCase. Expected: {}.'.format(self.wrapped.ComponentLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentLoadCase.__class__)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def peak_pulley_torque(self) -> 'List[_5133.DynamicTorqueResultAtTime]':
        '''List[DynamicTorqueResultAtTime]: 'PeakPulleyTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PeakPulleyTorque, constructor.new(_5133.DynamicTorqueResultAtTime))
        return value
