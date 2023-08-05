'''_2318.py

PartToPartShearCouplingHalfSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2145
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6186
from mastapy.system_model.analyses_and_results.power_flows import _3317
from mastapy.system_model.analyses_and_results.system_deflections import _2268
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'PartToPartShearCouplingHalfSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfSystemDeflection',)


class PartToPartShearCouplingHalfSystemDeflection(_2268.CouplingHalfSystemDeflection):
    '''PartToPartShearCouplingHalfSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2145.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2145.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6186.PartToPartShearCouplingHalfLoadCase':
        '''PartToPartShearCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6186.PartToPartShearCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3317.PartToPartShearCouplingHalfPowerFlow':
        '''PartToPartShearCouplingHalfPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3317.PartToPartShearCouplingHalfPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
