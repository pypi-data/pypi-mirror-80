'''_2345.py

StraightBevelGearSetSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2109
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6219
from mastapy.system_model.analyses_and_results.power_flows import _3346
from mastapy.gears.rating.straight_bevel import _201
from mastapy.system_model.analyses_and_results.system_deflections import _2346, _2344, _2245
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'StraightBevelGearSetSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetSystemDeflection',)


class StraightBevelGearSetSystemDeflection(_2245.BevelGearSetSystemDeflection):
    '''StraightBevelGearSetSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2109.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2109.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6219.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6219.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3346.StraightBevelGearSetPowerFlow':
        '''StraightBevelGearSetPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3346.StraightBevelGearSetPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_201.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_201.StraightBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_201.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_201.StraightBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def straight_bevel_gears_system_deflection(self) -> 'List[_2346.StraightBevelGearSystemDeflection]':
        '''List[StraightBevelGearSystemDeflection]: 'StraightBevelGearsSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsSystemDeflection, constructor.new(_2346.StraightBevelGearSystemDeflection))
        return value

    @property
    def straight_bevel_meshes_system_deflection(self) -> 'List[_2344.StraightBevelGearMeshSystemDeflection]':
        '''List[StraightBevelGearMeshSystemDeflection]: 'StraightBevelMeshesSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesSystemDeflection, constructor.new(_2344.StraightBevelGearMeshSystemDeflection))
        return value
