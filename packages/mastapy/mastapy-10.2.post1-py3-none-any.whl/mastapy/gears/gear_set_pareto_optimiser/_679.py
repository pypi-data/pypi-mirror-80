﻿'''_679.py

GearSetParetoOptimiser
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs import _714
from mastapy.gears.gear_designs.zerol_bevel import _718
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _723
from mastapy.gears.gear_designs.straight_bevel_diff import _727
from mastapy.gears.gear_designs.straight_bevel import _731
from mastapy.gears.gear_designs.spiral_bevel import _735
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _739
from mastapy.gears.gear_designs.klingelnberg_hypoid import _743
from mastapy.gears.gear_designs.klingelnberg_conical import _747
from mastapy.gears.gear_designs.hypoid import _751
from mastapy.gears.gear_designs.face import _759
from mastapy.gears.gear_designs.cylindrical import _785, _794
from mastapy.gears.gear_designs.conical import _891
from mastapy.gears.gear_designs.concept import _913
from mastapy.gears.gear_designs.bevel import _917
from mastapy.gears.gear_designs.agma_gleason_conical import _930
from mastapy.gears.gear_set_pareto_optimiser import _673, _678
from mastapy.gears.rating import _155
from mastapy._internal.python_net import python_net_import

_GEAR_SET_PARETO_OPTIMISER = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'GearSetParetoOptimiser')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetParetoOptimiser',)


class GearSetParetoOptimiser(_673.DesignSpaceSearchBase['_155.AbstractGearSetRating', '_678.GearSetOptimiserCandidate']):
    '''GearSetParetoOptimiser

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_PARETO_OPTIMISER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetParetoOptimiser.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def remove_candidates_which_cannot_be_manufactured_with_cutters_from_database(self) -> 'bool':
        '''bool: 'RemoveCandidatesWhichCannotBeManufacturedWithCuttersFromDatabase' is the original name of this property.'''

        return self.wrapped.RemoveCandidatesWhichCannotBeManufacturedWithCuttersFromDatabase

    @remove_candidates_which_cannot_be_manufactured_with_cutters_from_database.setter
    def remove_candidates_which_cannot_be_manufactured_with_cutters_from_database(self, value: 'bool'):
        self.wrapped.RemoveCandidatesWhichCannotBeManufacturedWithCuttersFromDatabase = bool(value) if value else False

    @property
    def number_of_designs_with_gears_which_cannot_be_manufactured_from_cutters(self) -> 'int':
        '''int: 'NumberOfDesignsWithGearsWhichCannotBeManufacturedFromCutters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfDesignsWithGearsWhichCannotBeManufacturedFromCutters

    @property
    def remove_candidates_with_warnings(self) -> 'bool':
        '''bool: 'RemoveCandidatesWithWarnings' is the original name of this property.'''

        return self.wrapped.RemoveCandidatesWithWarnings

    @remove_candidates_with_warnings.setter
    def remove_candidates_with_warnings(self, value: 'bool'):
        self.wrapped.RemoveCandidatesWithWarnings = bool(value) if value else False

    @property
    def reset_charts(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ResetCharts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ResetCharts

    @property
    def add_chart(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddChart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddChart

    @property
    def selected_candidate_geometry(self) -> '_714.GearSetDesign':
        '''GearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _714.GearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to GearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_zerol_bevel_gear_set_design(self) -> '_718.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _718.ZerolBevelGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_worm_gear_set_design(self) -> '_723.WormGearSetDesign':
        '''WormGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _723.WormGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to WormGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_straight_bevel_diff_gear_set_design(self) -> '_727.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _727.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_straight_bevel_gear_set_design(self) -> '_731.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _731.StraightBevelGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_spiral_bevel_gear_set_design(self) -> '_735.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _735.SpiralBevelGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_739.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _739.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_743.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _743.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_klingelnberg_conical_gear_set_design(self) -> '_747.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _747.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_hypoid_gear_set_design(self) -> '_751.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _751.HypoidGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_face_gear_set_design(self) -> '_759.FaceGearSetDesign':
        '''FaceGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _759.FaceGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to FaceGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_cylindrical_gear_set_design(self) -> '_785.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _785.CylindricalGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_cylindrical_planetary_gear_set_design(self) -> '_794.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _794.CylindricalPlanetaryGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_conical_gear_set_design(self) -> '_891.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _891.ConicalGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to ConicalGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_concept_gear_set_design(self) -> '_913.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _913.ConceptGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to ConceptGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_bevel_gear_set_design(self) -> '_917.BevelGearSetDesign':
        '''BevelGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.BevelGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def selected_candidate_geometry_of_type_agma_gleason_conical_gear_set_design(self) -> '_930.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'SelectedCandidateGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _930.AGMAGleasonConicalGearSetDesign.TYPE not in self.wrapped.SelectedCandidateGeometry.__class__.__mro__:
            raise CastException('Failed to cast selected_candidate_geometry to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.wrapped.SelectedCandidateGeometry.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedCandidateGeometry.__class__)(self.wrapped.SelectedCandidateGeometry) if self.wrapped.SelectedCandidateGeometry else None

    @property
    def candidate_gear_sets(self) -> 'List[_714.GearSetDesign]':
        '''List[GearSetDesign]: 'CandidateGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CandidateGearSets, constructor.new(_714.GearSetDesign))
        return value

    @property
    def all_candidate_gear_sets(self) -> 'List[_714.GearSetDesign]':
        '''List[GearSetDesign]: 'AllCandidateGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllCandidateGearSets, constructor.new(_714.GearSetDesign))
        return value
