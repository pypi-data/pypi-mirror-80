'''_117.py

BevelHypoidGearRatingSettings
'''


from mastapy.gears.materials import _388
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.rating.hypoid import _241
from mastapy.gears.rating.iso_10300 import _228, _220, _235
from mastapy.utility import _1143
from mastapy._internal.python_net import python_net_import

_BEVEL_HYPOID_GEAR_RATING_SETTINGS = python_net_import('SMT.MastaAPI.Gears', 'BevelHypoidGearRatingSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelHypoidGearRatingSettings',)


class BevelHypoidGearRatingSettings(_1143.PerMachineSettings):
    '''BevelHypoidGearRatingSettings

    This is a mastapy class.
    '''

    TYPE = _BEVEL_HYPOID_GEAR_RATING_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelHypoidGearRatingSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_rating_method(self) -> '_388.RatingMethods':
        '''RatingMethods: 'BevelGearRatingMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BevelGearRatingMethod)
        return constructor.new(_388.RatingMethods)(value) if value else None

    @bevel_gear_rating_method.setter
    def bevel_gear_rating_method(self, value: '_388.RatingMethods'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BevelGearRatingMethod = value

    @property
    def hypoid_gear_rating_method(self) -> '_241.HypoidRatingMethod':
        '''HypoidRatingMethod: 'HypoidGearRatingMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HypoidGearRatingMethod)
        return constructor.new(_241.HypoidRatingMethod)(value) if value else None

    @hypoid_gear_rating_method.setter
    def hypoid_gear_rating_method(self, value: '_241.HypoidRatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGearRatingMethod = value

    @property
    def include_mesh_node_misalignments_in_default_report(self) -> 'bool':
        '''bool: 'IncludeMeshNodeMisalignmentsInDefaultReport' is the original name of this property.'''

        return self.wrapped.IncludeMeshNodeMisalignmentsInDefaultReport

    @include_mesh_node_misalignments_in_default_report.setter
    def include_mesh_node_misalignments_in_default_report(self, value: 'bool'):
        self.wrapped.IncludeMeshNodeMisalignmentsInDefaultReport = bool(value) if value else False

    @property
    def iso_rating_method_for_bevel_gears(self) -> '_228.ISO10300RatingMethod':
        '''ISO10300RatingMethod: 'ISORatingMethodForBevelGears' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ISORatingMethodForBevelGears)
        return constructor.new(_228.ISO10300RatingMethod)(value) if value else None

    @iso_rating_method_for_bevel_gears.setter
    def iso_rating_method_for_bevel_gears(self, value: '_228.ISO10300RatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ISORatingMethodForBevelGears = value

    @property
    def iso_rating_method_for_hypoid_gears(self) -> '_228.ISO10300RatingMethod':
        '''ISO10300RatingMethod: 'ISORatingMethodForHypoidGears' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ISORatingMethodForHypoidGears)
        return constructor.new(_228.ISO10300RatingMethod)(value) if value else None

    @iso_rating_method_for_hypoid_gears.setter
    def iso_rating_method_for_hypoid_gears(self, value: '_228.ISO10300RatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ISORatingMethodForHypoidGears = value

    @property
    def bevel_general_load_factors_k_method(self) -> '_220.GeneralLoadFactorCalculationMethod':
        '''GeneralLoadFactorCalculationMethod: 'BevelGeneralLoadFactorsKMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BevelGeneralLoadFactorsKMethod)
        return constructor.new(_220.GeneralLoadFactorCalculationMethod)(value) if value else None

    @bevel_general_load_factors_k_method.setter
    def bevel_general_load_factors_k_method(self, value: '_220.GeneralLoadFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BevelGeneralLoadFactorsKMethod = value

    @property
    def hypoid_general_load_factors_k_method(self) -> '_220.GeneralLoadFactorCalculationMethod':
        '''GeneralLoadFactorCalculationMethod: 'HypoidGeneralLoadFactorsKMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HypoidGeneralLoadFactorsKMethod)
        return constructor.new(_220.GeneralLoadFactorCalculationMethod)(value) if value else None

    @hypoid_general_load_factors_k_method.setter
    def hypoid_general_load_factors_k_method(self, value: '_220.GeneralLoadFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGeneralLoadFactorsKMethod = value

    @property
    def bevel_pitting_factor_calculation_method(self) -> '_235.PittingFactorCalculationMethod':
        '''PittingFactorCalculationMethod: 'BevelPittingFactorCalculationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BevelPittingFactorCalculationMethod)
        return constructor.new(_235.PittingFactorCalculationMethod)(value) if value else None

    @bevel_pitting_factor_calculation_method.setter
    def bevel_pitting_factor_calculation_method(self, value: '_235.PittingFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BevelPittingFactorCalculationMethod = value

    @property
    def hypoid_pitting_factor_calculation_method(self) -> '_235.PittingFactorCalculationMethod':
        '''PittingFactorCalculationMethod: 'HypoidPittingFactorCalculationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HypoidPittingFactorCalculationMethod)
        return constructor.new(_235.PittingFactorCalculationMethod)(value) if value else None

    @hypoid_pitting_factor_calculation_method.setter
    def hypoid_pitting_factor_calculation_method(self, value: '_235.PittingFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidPittingFactorCalculationMethod = value
