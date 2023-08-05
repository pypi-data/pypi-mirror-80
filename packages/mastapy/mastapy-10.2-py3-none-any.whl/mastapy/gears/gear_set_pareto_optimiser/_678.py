'''_678.py

GearSetOptimiserCandidate
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.gears.rating import _155, _162, _163
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.zerol_bevel import _171
from mastapy.gears.rating.worm import _175, _176
from mastapy.gears.rating.straight_bevel_diff import _197
from mastapy.gears.rating.straight_bevel import _201
from mastapy.gears.rating.spiral_bevel import _204
from mastapy.gears.rating.klingelnberg_spiral_bevel import _207
from mastapy.gears.rating.klingelnberg_hypoid import _210
from mastapy.gears.rating.klingelnberg_conical import _213
from mastapy.gears.rating.hypoid import _240
from mastapy.gears.rating.face import _249, _250
from mastapy.gears.rating.cylindrical import _261, _262
from mastapy.gears.rating.conical import _325, _326
from mastapy.gears.rating.concept import _336, _337
from mastapy.gears.rating.bevel import _340
from mastapy.gears.rating.agma_gleason_conical import _351
from mastapy.gears.gear_set_pareto_optimiser import _674
from mastapy._internal.python_net import python_net_import

_GEAR_SET_OPTIMISER_CANDIDATE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'GearSetOptimiserCandidate')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetOptimiserCandidate',)


class GearSetOptimiserCandidate(_674.DesignSpaceSearchCandidateBase['_155.AbstractGearSetRating', 'GearSetOptimiserCandidate']):
    '''GearSetOptimiserCandidate

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_OPTIMISER_CANDIDATE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetOptimiserCandidate.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def add_design(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddDesign

    @property
    def candidate(self) -> '_155.AbstractGearSetRating':
        '''AbstractGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _155.AbstractGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to AbstractGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_gear_set_duty_cycle_rating(self) -> '_162.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _162.GearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to GearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_gear_set_rating(self) -> '_163.GearSetRating':
        '''GearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _163.GearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to GearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_zerol_bevel_gear_set_rating(self) -> '_171.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _171.ZerolBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ZerolBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_worm_gear_set_duty_cycle_rating(self) -> '_175.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _175.WormGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_worm_gear_set_rating(self) -> '_176.WormGearSetRating':
        '''WormGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _176.WormGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to WormGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_straight_bevel_diff_gear_set_rating(self) -> '_197.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _197.StraightBevelDiffGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to StraightBevelDiffGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_straight_bevel_gear_set_rating(self) -> '_201.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _201.StraightBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to StraightBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_spiral_bevel_gear_set_rating(self) -> '_204.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _204.SpiralBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to SpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(self) -> '_207.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _207.KlingelnbergCycloPalloidSpiralBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to KlingelnbergCycloPalloidSpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_rating(self) -> '_210.KlingelnbergCycloPalloidHypoidGearSetRating':
        '''KlingelnbergCycloPalloidHypoidGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _210.KlingelnbergCycloPalloidHypoidGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to KlingelnbergCycloPalloidHypoidGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_klingelnberg_cyclo_palloid_conical_gear_set_rating(self) -> '_213.KlingelnbergCycloPalloidConicalGearSetRating':
        '''KlingelnbergCycloPalloidConicalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _213.KlingelnbergCycloPalloidConicalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to KlingelnbergCycloPalloidConicalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_hypoid_gear_set_rating(self) -> '_240.HypoidGearSetRating':
        '''HypoidGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _240.HypoidGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to HypoidGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_face_gear_set_duty_cycle_rating(self) -> '_249.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _249.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_face_gear_set_rating(self) -> '_250.FaceGearSetRating':
        '''FaceGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _250.FaceGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to FaceGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_261.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _261.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_cylindrical_gear_set_rating(self) -> '_262.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _262.CylindricalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to CylindricalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_conical_gear_set_duty_cycle_rating(self) -> '_325.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _325.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_conical_gear_set_rating(self) -> '_326.ConicalGearSetRating':
        '''ConicalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _326.ConicalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConicalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_concept_gear_set_duty_cycle_rating(self) -> '_336.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _336.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_concept_gear_set_rating(self) -> '_337.ConceptGearSetRating':
        '''ConceptGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _337.ConceptGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConceptGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_bevel_gear_set_rating(self) -> '_340.BevelGearSetRating':
        '''BevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _340.BevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to BevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_agma_gleason_conical_gear_set_rating(self) -> '_351.AGMAGleasonConicalGearSetRating':
        '''AGMAGleasonConicalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _351.AGMAGleasonConicalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to AGMAGleasonConicalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Candidate.__class__)(self.wrapped.Candidate) if self.wrapped.Candidate else None
