'''_4100.py

SynchroniserHalfModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _2159
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6222
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4102
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'SynchroniserHalfModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfModalAnalysesAtSpeeds',)


class SynchroniserHalfModalAnalysesAtSpeeds(_4102.SynchroniserPartModalAnalysesAtSpeeds):
    '''SynchroniserHalfModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2159.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2159.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6222.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6222.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
