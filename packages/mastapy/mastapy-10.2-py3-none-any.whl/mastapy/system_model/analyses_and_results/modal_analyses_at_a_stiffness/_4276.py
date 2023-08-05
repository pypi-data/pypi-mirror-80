'''_4276.py

CVTModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.couplings import _2142
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4245
from mastapy._internal.python_net import python_net_import

_CVT_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'CVTModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTModalAnalysisAtAStiffness',)


class CVTModalAnalysisAtAStiffness(_4245.BeltDriveModalAnalysisAtAStiffness):
    '''CVTModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CVT_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2142.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
