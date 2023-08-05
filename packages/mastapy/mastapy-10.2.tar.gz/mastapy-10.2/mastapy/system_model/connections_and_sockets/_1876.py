'''_1876.py

Socket
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _2009, _2002, _2005, _2007,
    _2012, _2013, _2016, _2018,
    _2021, _2025, _2026, _2027,
    _2029, _2032, _2034, _2035,
    _2040, _2041, _2010
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2044
from mastapy.system_model.part_model.gears import (
    _2074, _2076, _2078, _2079,
    _2080, _2082, _2084, _2086,
    _2088, _2089, _2091, _2095,
    _2097, _2099, _2101, _2104,
    _2106, _2108, _2110, _2111,
    _2112, _2114
)
from mastapy.system_model.part_model.couplings import (
    _2136, _2139, _2141, _2143,
    _2145, _2146, _2152, _2154,
    _2156, _2159, _2160, _2161,
    _2163, _2165
)
from mastapy.system_model.connections_and_sockets import _1855
from mastapy._internal.python_net import python_net_import
from mastapy import _0

_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Socket')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')


__docformat__ = 'restructuredtext en'
__all__ = ('Socket',)


class Socket(_0.APIBase):
    '''Socket

    This is a mastapy class.
    '''

    TYPE = _SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Socket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def owner(self) -> '_2009.Component':
        '''Component: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.Component.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Component. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_abstract_shaft_or_housing(self) -> '_2002.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.AbstractShaftOrHousing.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_bearing(self) -> '_2005.Bearing':
        '''Bearing: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.Bearing.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Bearing. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_bolt(self) -> '_2007.Bolt':
        '''Bolt: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2007.Bolt.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Bolt. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_connector(self) -> '_2012.Connector':
        '''Connector: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.Connector.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Connector. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_datum(self) -> '_2013.Datum':
        '''Datum: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.Datum.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Datum. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_external_cad_model(self) -> '_2016.ExternalCADModel':
        '''ExternalCADModel: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.ExternalCADModel.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ExternalCADModel. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_guide_dxf_model(self) -> '_2018.GuideDxfModel':
        '''GuideDxfModel: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.GuideDxfModel.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to GuideDxfModel. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_imported_fe_component(self) -> '_2021.ImportedFEComponent':
        '''ImportedFEComponent: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.ImportedFEComponent.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ImportedFEComponent. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_mass_disc(self) -> '_2025.MassDisc':
        '''MassDisc: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.MassDisc.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to MassDisc. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_measurement_component(self) -> '_2026.MeasurementComponent':
        '''MeasurementComponent: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.MeasurementComponent.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to MeasurementComponent. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_mountable_component(self) -> '_2027.MountableComponent':
        '''MountableComponent: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.MountableComponent.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to MountableComponent. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_oil_seal(self) -> '_2029.OilSeal':
        '''OilSeal: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.OilSeal.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to OilSeal. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_planet_carrier(self) -> '_2032.PlanetCarrier':
        '''PlanetCarrier: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2032.PlanetCarrier.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to PlanetCarrier. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_point_load(self) -> '_2034.PointLoad':
        '''PointLoad: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.PointLoad.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to PointLoad. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_power_load(self) -> '_2035.PowerLoad':
        '''PowerLoad: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.PowerLoad.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to PowerLoad. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_unbalanced_mass(self) -> '_2040.UnbalancedMass':
        '''UnbalancedMass: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2040.UnbalancedMass.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to UnbalancedMass. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_virtual_component(self) -> '_2041.VirtualComponent':
        '''VirtualComponent: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.VirtualComponent.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to VirtualComponent. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_shaft(self) -> '_2044.Shaft':
        '''Shaft: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.Shaft.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Shaft. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_agma_gleason_conical_gear(self) -> '_2074.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.AGMAGleasonConicalGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_bevel_differential_gear(self) -> '_2076.BevelDifferentialGear':
        '''BevelDifferentialGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.BevelDifferentialGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_bevel_differential_planet_gear(self) -> '_2078.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2078.BevelDifferentialPlanetGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_bevel_differential_sun_gear(self) -> '_2079.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.BevelDifferentialSunGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_bevel_gear(self) -> '_2080.BevelGear':
        '''BevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2080.BevelGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_concept_gear(self) -> '_2082.ConceptGear':
        '''ConceptGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.ConceptGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ConceptGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_conical_gear(self) -> '_2084.ConicalGear':
        '''ConicalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.ConicalGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ConicalGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_cylindrical_gear(self) -> '_2086.CylindricalGear':
        '''CylindricalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.CylindricalGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to CylindricalGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_cylindrical_planet_gear(self) -> '_2088.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.CylindricalPlanetGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_face_gear(self) -> '_2089.FaceGear':
        '''FaceGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.FaceGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to FaceGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_gear(self) -> '_2091.Gear':
        '''Gear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.Gear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Gear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_hypoid_gear(self) -> '_2095.HypoidGear':
        '''HypoidGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2095.HypoidGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to HypoidGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2097.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2097.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2099.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2099.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2101.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_spiral_bevel_gear(self) -> '_2104.SpiralBevelGear':
        '''SpiralBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2104.SpiralBevelGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to SpiralBevelGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_straight_bevel_diff_gear(self) -> '_2106.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2106.StraightBevelDiffGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_straight_bevel_gear(self) -> '_2108.StraightBevelGear':
        '''StraightBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2108.StraightBevelGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_straight_bevel_planet_gear(self) -> '_2110.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2110.StraightBevelPlanetGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_straight_bevel_sun_gear(self) -> '_2111.StraightBevelSunGear':
        '''StraightBevelSunGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.StraightBevelSunGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_worm_gear(self) -> '_2112.WormGear':
        '''WormGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2112.WormGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to WormGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_zerol_bevel_gear(self) -> '_2114.ZerolBevelGear':
        '''ZerolBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.ZerolBevelGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ZerolBevelGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_clutch_half(self) -> '_2136.ClutchHalf':
        '''ClutchHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2136.ClutchHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ClutchHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_concept_coupling_half(self) -> '_2139.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2139.ConceptCouplingHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_coupling_half(self) -> '_2141.CouplingHalf':
        '''CouplingHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2141.CouplingHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to CouplingHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_cvt_pulley(self) -> '_2143.CVTPulley':
        '''CVTPulley: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.CVTPulley.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to CVTPulley. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_part_to_part_shear_coupling_half(self) -> '_2145.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2145.PartToPartShearCouplingHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_pulley(self) -> '_2146.Pulley':
        '''Pulley: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.Pulley.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Pulley. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_rolling_ring(self) -> '_2152.RollingRing':
        '''RollingRing: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2152.RollingRing.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to RollingRing. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_shaft_hub_connection(self) -> '_2154.ShaftHubConnection':
        '''ShaftHubConnection: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2154.ShaftHubConnection.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ShaftHubConnection. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_spring_damper_half(self) -> '_2156.SpringDamperHalf':
        '''SpringDamperHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2156.SpringDamperHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to SpringDamperHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_synchroniser_half(self) -> '_2159.SynchroniserHalf':
        '''SynchroniserHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.SynchroniserHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to SynchroniserHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_synchroniser_part(self) -> '_2160.SynchroniserPart':
        '''SynchroniserPart: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2160.SynchroniserPart.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to SynchroniserPart. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_synchroniser_sleeve(self) -> '_2161.SynchroniserSleeve':
        '''SynchroniserSleeve: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2161.SynchroniserSleeve.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_torque_converter_pump(self) -> '_2163.TorqueConverterPump':
        '''TorqueConverterPump: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.TorqueConverterPump.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to TorqueConverterPump. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def owner_of_type_torque_converter_turbine(self) -> '_2165.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2165.TorqueConverterTurbine.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner else None

    @property
    def connections(self) -> 'List[_1855.Connection]':
        '''List[Connection]: 'Connections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Connections, constructor.new(_1855.Connection))
        return value

    @property
    def connected_components(self) -> 'List[_2009.Component]':
        '''List[Component]: 'ConnectedComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectedComponents, constructor.new(_2009.Component))
        return value

    def connect_to_socket(self, socket: 'Socket') -> '_2010.ComponentsConnectedResult':
        ''' 'ConnectTo' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        method_result = self.wrapped.ConnectTo.Overloads[_SOCKET](socket.wrapped if socket else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_possible_sockets_to_connect_to(self, component_to_connect_to: '_2009.Component') -> 'List[Socket]':
        ''' 'GetPossibleSocketsToConnectTo' is the original name of this method.

        Args:
            component_to_connect_to (mastapy.system_model.part_model.Component)

        Returns:
            List[mastapy.system_model.connections_and_sockets.Socket]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.GetPossibleSocketsToConnectTo(component_to_connect_to.wrapped if component_to_connect_to else None), constructor.new(Socket))

    def connect_to(self, component: '_2009.Component') -> '_2010.ComponentsConnectedResult':
        ''' 'ConnectTo' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        method_result = self.wrapped.ConnectTo.Overloads[_COMPONENT](component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def connection_to(self, socket: 'Socket') -> '_1855.Connection':
        ''' 'ConnectionTo' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.connections_and_sockets.Connection
        '''

        method_result = self.wrapped.ConnectionTo(socket.wrapped if socket else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
