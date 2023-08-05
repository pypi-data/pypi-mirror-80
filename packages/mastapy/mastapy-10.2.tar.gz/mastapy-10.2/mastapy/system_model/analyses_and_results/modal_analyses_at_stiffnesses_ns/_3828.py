'''_3828.py

PlanetCarrierModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model import _2032
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6191
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3820
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'PlanetCarrierModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierModalAnalysesAtStiffnesses',)


class PlanetCarrierModalAnalysesAtStiffnesses(_3820.MountableComponentModalAnalysesAtStiffnesses):
    '''PlanetCarrierModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2032.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2032.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6191.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6191.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
