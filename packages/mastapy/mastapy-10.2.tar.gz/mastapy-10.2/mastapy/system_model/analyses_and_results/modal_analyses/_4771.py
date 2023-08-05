'''_4771.py

ExternalCADModelModalAnalysis
'''


from mastapy.system_model.part_model import _2016
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6141
from mastapy.system_model.analyses_and_results.system_deflections import _2284
from mastapy.system_model.analyses_and_results.modal_analyses import _4747
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ExternalCADModelModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelModalAnalysis',)


class ExternalCADModelModalAnalysis(_4747.ComponentModalAnalysis):
    '''ExternalCADModelModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2016.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2016.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6141.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6141.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2284.ExternalCADModelSystemDeflection':
        '''ExternalCADModelSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2284.ExternalCADModelSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
