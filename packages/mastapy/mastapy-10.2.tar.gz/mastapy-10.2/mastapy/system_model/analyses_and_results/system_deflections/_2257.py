'''_2257.py

ConceptCouplingSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2138
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6103
from mastapy.system_model.analyses_and_results.power_flows import _3267
from mastapy.system_model.analyses_and_results.system_deflections import _2269
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConceptCouplingSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingSystemDeflection',)


class ConceptCouplingSystemDeflection(_2269.CouplingSystemDeflection):
    '''ConceptCouplingSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2138.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2138.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6103.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6103.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3267.ConceptCouplingPowerFlow':
        '''ConceptCouplingPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3267.ConceptCouplingPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
