'''_4828.py

SpringDamperModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _2155
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6212
from mastapy.system_model.analyses_and_results.system_deflections import _2340
from mastapy.system_model.analyses_and_results.modal_analyses import _4762
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'SpringDamperModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperModalAnalysis',)


class SpringDamperModalAnalysis(_4762.CouplingModalAnalysis):
    '''SpringDamperModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2155.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2155.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6212.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6212.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2340.SpringDamperSystemDeflection':
        '''SpringDamperSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2340.SpringDamperSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
