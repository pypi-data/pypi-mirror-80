'''_4282.py

DatumModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model import _2013
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6128
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4260
from mastapy._internal.python_net import python_net_import

_DATUM_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'DatumModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumModalAnalysisAtAStiffness',)


class DatumModalAnalysisAtAStiffness(_4260.ComponentModalAnalysisAtAStiffness):
    '''DatumModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _DATUM_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2013.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2013.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6128.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6128.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
