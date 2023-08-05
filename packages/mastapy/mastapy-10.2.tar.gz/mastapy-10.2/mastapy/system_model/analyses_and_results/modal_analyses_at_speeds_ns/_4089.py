'''_4089.py

SpringDamperHalfModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _2156
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6211
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4027
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'SpringDamperHalfModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfModalAnalysesAtSpeeds',)


class SpringDamperHalfModalAnalysesAtSpeeds(_4027.CouplingHalfModalAnalysesAtSpeeds):
    '''SpringDamperHalfModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2156.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2156.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6211.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6211.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
