'''_161.py

GearRating
'''


from mastapy.gears.rating import _156, _154
from mastapy._internal import constructor
from mastapy.materials import (
    _83, _55, _58, _59
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'GearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GearRating',)


class GearRating(_154.AbstractGearRating):
    '''GearRating

    This is a mastapy class.
    '''

    TYPE = _GEAR_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def static_safety_factor(self) -> '_156.BendingAndContactReportingObject':
        '''BendingAndContactReportingObject: 'StaticSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_156.BendingAndContactReportingObject)(self.wrapped.StaticSafetyFactor) if self.wrapped.StaticSafetyFactor else None

    @property
    def bending_safety_factor_results(self) -> '_83.SafetyFactorItem':
        '''SafetyFactorItem: 'BendingSafetyFactorResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _83.SafetyFactorItem.TYPE not in self.wrapped.BendingSafetyFactorResults.__class__.__mro__:
            raise CastException('Failed to cast bending_safety_factor_results to SafetyFactorItem. Expected: {}.'.format(self.wrapped.BendingSafetyFactorResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BendingSafetyFactorResults.__class__)(self.wrapped.BendingSafetyFactorResults) if self.wrapped.BendingSafetyFactorResults else None

    @property
    def contact_safety_factor_results(self) -> '_83.SafetyFactorItem':
        '''SafetyFactorItem: 'ContactSafetyFactorResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _83.SafetyFactorItem.TYPE not in self.wrapped.ContactSafetyFactorResults.__class__.__mro__:
            raise CastException('Failed to cast contact_safety_factor_results to SafetyFactorItem. Expected: {}.'.format(self.wrapped.ContactSafetyFactorResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContactSafetyFactorResults.__class__)(self.wrapped.ContactSafetyFactorResults) if self.wrapped.ContactSafetyFactorResults else None
