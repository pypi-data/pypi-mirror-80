'''_3418.py

GearMeshCompoundPowerFlow
'''


from mastapy.gears.rating import _165
from mastapy._internal import constructor
from mastapy.gears.rating.worm import _177
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _246
from mastapy.gears.rating.cylindrical import _264
from mastapy.gears.rating.conical import _328
from mastapy.gears.rating.concept import _333
from mastapy.system_model.analyses_and_results.power_flows.compound import _3425
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'GearMeshCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundPowerFlow',)


class GearMeshCompoundPowerFlow(_3425.InterMountableComponentConnectionCompoundPowerFlow):
    '''GearMeshCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_mesh_duty_cycle_rating(self) -> '_165.MeshDutyCycleRating':
        '''MeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _165.MeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to MeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMeshDutyCycleRating.__class__)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_worm_mesh_duty_cycle_rating(self) -> '_177.WormMeshDutyCycleRating':
        '''WormMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _177.WormMeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to WormMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMeshDutyCycleRating.__class__)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_face_gear_mesh_duty_cycle_rating(self) -> '_246.FaceGearMeshDutyCycleRating':
        '''FaceGearMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _246.FaceGearMeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to FaceGearMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMeshDutyCycleRating.__class__)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_cylindrical_mesh_duty_cycle_rating(self) -> '_264.CylindricalMeshDutyCycleRating':
        '''CylindricalMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _264.CylindricalMeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to CylindricalMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMeshDutyCycleRating.__class__)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_conical_mesh_duty_cycle_rating(self) -> '_328.ConicalMeshDutyCycleRating':
        '''ConicalMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _328.ConicalMeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to ConicalMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMeshDutyCycleRating.__class__)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_concept_gear_mesh_duty_cycle_rating(self) -> '_333.ConceptGearMeshDutyCycleRating':
        '''ConceptGearMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _333.ConceptGearMeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to ConceptGearMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearMeshDutyCycleRating.__class__)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None
