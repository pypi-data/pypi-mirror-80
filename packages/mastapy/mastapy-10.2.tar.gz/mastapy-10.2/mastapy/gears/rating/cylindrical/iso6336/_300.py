'''_300.py

CylindricalGearToothFatigueFractureResults
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical.iso6336 import _315
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TOOTH_FATIGUE_FRACTURE_RESULTS = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'CylindricalGearToothFatigueFractureResults')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearToothFatigueFractureResults',)


class CylindricalGearToothFatigueFractureResults(_0.APIBase):
    '''CylindricalGearToothFatigueFractureResults

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_TOOTH_FATIGUE_FRACTURE_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearToothFatigueFractureResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def witzigs_safety_factor(self) -> 'float':
        '''float: 'WitzigsSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WitzigsSafetyFactor

    @property
    def maximum_material_exposure(self) -> 'float':
        '''float: 'MaximumMaterialExposure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumMaterialExposure

    @property
    def critical_section(self) -> '_315.ToothFlankFractureAnalysisContactPoint':
        '''ToothFlankFractureAnalysisContactPoint: 'CriticalSection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_315.ToothFlankFractureAnalysisContactPoint)(self.wrapped.CriticalSection) if self.wrapped.CriticalSection else None

    @property
    def analysis_rows(self) -> 'List[_315.ToothFlankFractureAnalysisContactPoint]':
        '''List[ToothFlankFractureAnalysisContactPoint]: 'AnalysisRows' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AnalysisRows, constructor.new(_315.ToothFlankFractureAnalysisContactPoint))
        return value
