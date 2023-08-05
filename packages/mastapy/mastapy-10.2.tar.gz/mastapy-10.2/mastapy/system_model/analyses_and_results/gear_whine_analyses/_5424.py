﻿'''_5424.py

ZerolBevelGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2115
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6243
from mastapy.system_model.analyses_and_results.system_deflections import _2368
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5422, _5423, _5294
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ZerolBevelGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetGearWhineAnalysis',)


class ZerolBevelGearSetGearWhineAnalysis(_5294.BevelGearSetGearWhineAnalysis):
    '''ZerolBevelGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2115.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2115.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6243.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6243.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2368.ZerolBevelGearSetSystemDeflection':
        '''ZerolBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2368.ZerolBevelGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5422.ZerolBevelGearGearWhineAnalysis]':
        '''List[ZerolBevelGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5422.ZerolBevelGearGearWhineAnalysis))
        return value

    @property
    def zerol_bevel_gears_gear_whine_analysis(self) -> 'List[_5422.ZerolBevelGearGearWhineAnalysis]':
        '''List[ZerolBevelGearGearWhineAnalysis]: 'ZerolBevelGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsGearWhineAnalysis, constructor.new(_5422.ZerolBevelGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5423.ZerolBevelGearMeshGearWhineAnalysis]':
        '''List[ZerolBevelGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5423.ZerolBevelGearMeshGearWhineAnalysis))
        return value

    @property
    def zerol_bevel_meshes_gear_whine_analysis(self) -> 'List[_5423.ZerolBevelGearMeshGearWhineAnalysis]':
        '''List[ZerolBevelGearMeshGearWhineAnalysis]: 'ZerolBevelMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesGearWhineAnalysis, constructor.new(_5423.ZerolBevelGearMeshGearWhineAnalysis))
        return value
