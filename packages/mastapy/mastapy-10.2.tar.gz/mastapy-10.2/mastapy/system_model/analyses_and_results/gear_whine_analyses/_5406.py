'''_5406.py

StraightBevelPlanetGearGearWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2110
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2347
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5400
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'StraightBevelPlanetGearGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearGearWhineAnalysis',)


class StraightBevelPlanetGearGearWhineAnalysis(_5400.StraightBevelDiffGearGearWhineAnalysis):
    '''StraightBevelPlanetGearGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2110.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2110.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2347.StraightBevelPlanetGearSystemDeflection':
        '''StraightBevelPlanetGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2347.StraightBevelPlanetGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
