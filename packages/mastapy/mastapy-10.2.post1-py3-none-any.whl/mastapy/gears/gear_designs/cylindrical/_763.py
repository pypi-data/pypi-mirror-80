'''_763.py

BacklashSpecification
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _793, _791, _820
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BACKLASH_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'BacklashSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('BacklashSpecification',)


class BacklashSpecification(_820.RelativeValuesSpecification['BacklashSpecification']):
    '''BacklashSpecification

    This is a mastapy class.
    '''

    TYPE = _BACKLASH_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BacklashSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def normal_backlash(self) -> '_793.CylindricalMeshLinearBacklashSpecification':
        '''CylindricalMeshLinearBacklashSpecification: 'NormalBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _793.CylindricalMeshLinearBacklashSpecification.TYPE not in self.wrapped.NormalBacklash.__class__.__mro__:
            raise CastException('Failed to cast normal_backlash to CylindricalMeshLinearBacklashSpecification. Expected: {}.'.format(self.wrapped.NormalBacklash.__class__.__qualname__))

        return constructor.new_override(self.wrapped.NormalBacklash.__class__)(self.wrapped.NormalBacklash) if self.wrapped.NormalBacklash else None

    @property
    def circumferential_backlash_pitch_circle(self) -> '_793.CylindricalMeshLinearBacklashSpecification':
        '''CylindricalMeshLinearBacklashSpecification: 'CircumferentialBacklashPitchCircle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _793.CylindricalMeshLinearBacklashSpecification.TYPE not in self.wrapped.CircumferentialBacklashPitchCircle.__class__.__mro__:
            raise CastException('Failed to cast circumferential_backlash_pitch_circle to CylindricalMeshLinearBacklashSpecification. Expected: {}.'.format(self.wrapped.CircumferentialBacklashPitchCircle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CircumferentialBacklashPitchCircle.__class__)(self.wrapped.CircumferentialBacklashPitchCircle) if self.wrapped.CircumferentialBacklashPitchCircle else None

    @property
    def circumferential_backlash_reference_circle(self) -> '_793.CylindricalMeshLinearBacklashSpecification':
        '''CylindricalMeshLinearBacklashSpecification: 'CircumferentialBacklashReferenceCircle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _793.CylindricalMeshLinearBacklashSpecification.TYPE not in self.wrapped.CircumferentialBacklashReferenceCircle.__class__.__mro__:
            raise CastException('Failed to cast circumferential_backlash_reference_circle to CylindricalMeshLinearBacklashSpecification. Expected: {}.'.format(self.wrapped.CircumferentialBacklashReferenceCircle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CircumferentialBacklashReferenceCircle.__class__)(self.wrapped.CircumferentialBacklashReferenceCircle) if self.wrapped.CircumferentialBacklashReferenceCircle else None

    @property
    def radial_backlash(self) -> '_793.CylindricalMeshLinearBacklashSpecification':
        '''CylindricalMeshLinearBacklashSpecification: 'RadialBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _793.CylindricalMeshLinearBacklashSpecification.TYPE not in self.wrapped.RadialBacklash.__class__.__mro__:
            raise CastException('Failed to cast radial_backlash to CylindricalMeshLinearBacklashSpecification. Expected: {}.'.format(self.wrapped.RadialBacklash.__class__.__qualname__))

        return constructor.new_override(self.wrapped.RadialBacklash.__class__)(self.wrapped.RadialBacklash) if self.wrapped.RadialBacklash else None

    @property
    def linear_backlash(self) -> 'List[_793.CylindricalMeshLinearBacklashSpecification]':
        '''List[CylindricalMeshLinearBacklashSpecification]: 'LinearBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LinearBacklash, constructor.new(_793.CylindricalMeshLinearBacklashSpecification))
        return value

    @property
    def angular_backlash(self) -> 'List[_791.CylindricalMeshAngularBacklash]':
        '''List[CylindricalMeshAngularBacklash]: 'AngularBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AngularBacklash, constructor.new(_791.CylindricalMeshAngularBacklash))
        return value
