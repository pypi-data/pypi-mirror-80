'''_2251.py

ClutchSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections import _2249, _2269
from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2135
from mastapy.system_model.analyses_and_results.static_loads import _6098
from mastapy.system_model.analyses_and_results.power_flows import _3262
from mastapy._internal.python_net import python_net_import

_CLUTCH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ClutchSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchSystemDeflection',)


class ClutchSystemDeflection(_2269.CouplingSystemDeflection):
    '''ClutchSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def clutch_connection(self) -> '_2249.ClutchConnectionSystemDeflection':
        '''ClutchConnectionSystemDeflection: 'ClutchConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2249.ClutchConnectionSystemDeflection)(self.wrapped.ClutchConnection) if self.wrapped.ClutchConnection else None

    @property
    def assembly_design(self) -> '_2135.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2135.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6098.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6098.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3262.ClutchPowerFlow':
        '''ClutchPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3262.ClutchPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
