'''_2431.py

GearCompoundSystemDeflection
'''


from mastapy.gears.rating import _158
from mastapy._internal import constructor
from mastapy.gears.rating.worm import _172
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _245
from mastapy.gears.rating.cylindrical import _252
from mastapy.gears.rating.conical import _322
from mastapy.gears.rating.concept import _332
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2451
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'GearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundSystemDeflection',)


class GearCompoundSystemDeflection(_2451.MountableComponentCompoundSystemDeflection):
    '''GearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_rating(self) -> '_158.GearDutyCycleRating':
        '''GearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _158.GearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to GearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_worm_gear_duty_cycle_rating(self) -> '_172.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _172.WormGearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to WormGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_face_gear_duty_cycle_rating(self) -> '_245.FaceGearDutyCycleRating':
        '''FaceGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _245.FaceGearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to FaceGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_cylindrical_gear_duty_cycle_rating(self) -> '_252.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _252.CylindricalGearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to CylindricalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_conical_gear_duty_cycle_rating(self) -> '_322.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _322.ConicalGearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to ConicalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_concept_gear_duty_cycle_rating(self) -> '_332.ConceptGearDutyCycleRating':
        '''ConceptGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _332.ConceptGearDutyCycleRating.TYPE not in self.wrapped.DutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_rating to ConceptGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DutyCycleRating.__class__)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None
