'''_6290.py

ConceptCouplingHalfAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2139
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6102
from mastapy.system_model.analyses_and_results.system_deflections import _2256
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6302
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ConceptCouplingHalfAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfAdvancedSystemDeflection',)


class ConceptCouplingHalfAdvancedSystemDeflection(_6302.CouplingHalfAdvancedSystemDeflection):
    '''ConceptCouplingHalfAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2139.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6102.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6102.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2256.ConceptCouplingHalfSystemDeflection]':
        '''List[ConceptCouplingHalfSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2256.ConceptCouplingHalfSystemDeflection))
        return value
