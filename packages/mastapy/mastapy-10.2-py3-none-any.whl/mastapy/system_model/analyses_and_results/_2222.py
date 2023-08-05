'''_2222.py

CompoundPowerFlowAnalysis
'''


from typing import Iterable

from mastapy.system_model.part_model import (
    _2001, _2002, _2005, _2007,
    _2008, _2009, _2012, _2013,
    _2016, _2017, _2000, _2018,
    _2021, _2025, _2026, _2027,
    _2029, _2031, _2032, _2034,
    _2035, _2037, _2039, _2040,
    _2041
)
from mastapy.system_model.analyses_and_results.power_flows.compound import (
    _3366, _3367, _3372, _3383,
    _3384, _3389, _3400, _3411,
    _3412, _3416, _3371, _3420,
    _3424, _3435, _3436, _3437,
    _3438, _3439, _3445, _3446,
    _3447, _3452, _3456, _3479,
    _3480, _3453, _3393, _3395,
    _3413, _3415, _3368, _3370,
    _3375, _3377, _3378, _3379,
    _3380, _3382, _3396, _3398,
    _3407, _3409, _3410, _3417,
    _3419, _3421, _3423, _3426,
    _3428, _3429, _3431, _3432,
    _3434, _3444, _3457, _3459,
    _3463, _3465, _3466, _3468,
    _3469, _3470, _3481, _3483,
    _3484, _3486, _3440, _3442,
    _3374, _3385, _3387, _3390,
    _3392, _3401, _3403, _3405,
    _3406, _3448, _3454, _3450,
    _3449, _3460, _3462, _3471,
    _3472, _3473, _3474, _3475,
    _3477, _3478, _3404, _3373,
    _3388, _3399, _3425, _3443,
    _3451, _3455, _3376, _3394,
    _3414, _3464, _3381, _3397,
    _3369, _3408, _3422, _3427,
    _3430, _3433, _3458, _3467,
    _3482, _3485, _3418, _3441,
    _3386, _3391, _3402, _3461,
    _3476
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2044
from mastapy.system_model.part_model.gears import (
    _2082, _2083, _2089, _2090,
    _2074, _2075, _2076, _2077,
    _2078, _2079, _2080, _2081,
    _2084, _2085, _2086, _2087,
    _2088, _2091, _2093, _2095,
    _2096, _2097, _2098, _2099,
    _2100, _2101, _2102, _2103,
    _2104, _2105, _2106, _2107,
    _2108, _2109, _2110, _2111,
    _2112, _2113, _2114, _2115
)
from mastapy.system_model.part_model.couplings import (
    _2144, _2145, _2133, _2135,
    _2136, _2138, _2139, _2140,
    _2141, _2142, _2143, _2146,
    _2154, _2152, _2153, _2155,
    _2156, _2157, _2159, _2160,
    _2161, _2162, _2163, _2165
)
from mastapy.system_model.connections_and_sockets import (
    _1856, _1851, _1852, _1855,
    _1864, _1867, _1871, _1875
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1881, _1885, _1891, _1905,
    _1883, _1887, _1879, _1889,
    _1895, _1898, _1899, _1900,
    _1903, _1907, _1909, _1911,
    _1893
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1919, _1913, _1915, _1917,
    _1921, _1923
)
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.analyses_and_results import _2174

_ABSTRACT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractAssembly')
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaftOrHousing')
_BEARING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bearing')
_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')
_BOLTED_JOINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BoltedJoint')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')
_DATUM = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Datum')
_EXTERNAL_CAD_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ExternalCADModel')
_FLEXIBLE_PIN_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FlexiblePinAssembly')
_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')
_GUIDE_DXF_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideDxfModel')
_IMPORTED_FE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ImportedFEComponent')
_MASS_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MassDisc')
_MEASUREMENT_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MeasurementComponent')
_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')
_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')
_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Part')
_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')
_POINT_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PointLoad')
_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')
_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')
_SPECIALISED_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'SpecialisedAssembly')
_UNBALANCED_MASS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'UnbalancedMass')
_VIRTUAL_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'VirtualComponent')
_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ShaftModel', 'Shaft')
_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')
_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')
_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')
_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')
_AGMA_GLEASON_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGear')
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGearSet')
_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialPlanetGear')
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialSunGear')
_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGear')
_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGearSet')
_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGear')
_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGearSet')
_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGear')
_CYLINDRICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGearSet')
_CYLINDRICAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalPlanetGear')
_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'Gear')
_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSet')
_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')
_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGear')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGear')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGear')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearSet')
_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')
_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')
_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGearSet')
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGear')
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGearSet')
_STRAIGHT_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGear')
_STRAIGHT_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGearSet')
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelSunGear')
_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')
_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')
_ZEROL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGear')
_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')
_PART_TO_PART_SHEAR_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCoupling')
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCouplingHalf')
_BELT_DRIVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'BeltDrive')
_CLUTCH = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Clutch')
_CLUTCH_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ClutchHalf')
_CONCEPT_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCoupling')
_CONCEPT_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCouplingHalf')
_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')
_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CouplingHalf')
_CVT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVT')
_CVT_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVTPulley')
_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Pulley')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')
_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')
_ROLLING_RING_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRingAssembly')
_SPRING_DAMPER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamper')
_SPRING_DAMPER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamperHalf')
_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')
_SYNCHRONISER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserHalf')
_SYNCHRONISER_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserPart')
_SYNCHRONISER_SLEEVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserSleeve')
_TORQUE_CONVERTER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverter')
_TORQUE_CONVERTER_PUMP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterPump')
_TORQUE_CONVERTER_TURBINE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterTurbine')
_CVT_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTBeltConnection')
_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BeltConnection')
_COAXIAL_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CoaxialConnection')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InterMountableComponentConnection')
_PLANETARY_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetaryConnection')
_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ShaftToMountableComponentConnection')
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')
_CONCEPT_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearMesh')
_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelDiffGearMesh')
_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')
_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConicalGearMesh')
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'AGMAGleasonConicalGearMesh')
_CYLINDRICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearMesh')
_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidConicalGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidHypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearMesh')
_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'SpiralBevelGearMesh')
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelGearMesh')
_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')
_ZEROL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearMesh')
_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'PartToPartShearCouplingConnection')
_CLUTCH_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ClutchConnection')
_CONCEPT_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ConceptCouplingConnection')
_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingConnection')
_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')
_TORQUE_CONVERTER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterConnection')
_COMPOUND_POWER_FLOW_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundPowerFlowAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundPowerFlowAnalysis',)


class CompoundPowerFlowAnalysis(_2174.CompoundAnalysis):
    '''CompoundPowerFlowAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_POWER_FLOW_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundPowerFlowAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def results_for_abstract_assembly(self, design_entity: '_2001.AbstractAssembly') -> 'Iterable[_3366.AbstractAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AbstractAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_3366.AbstractAssemblyCompoundPowerFlow))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_2002.AbstractShaftOrHousing') -> 'Iterable[_3367.AbstractShaftOrHousingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AbstractShaftOrHousingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING](design_entity.wrapped if design_entity else None), constructor.new(_3367.AbstractShaftOrHousingCompoundPowerFlow))

    def results_for_bearing(self, design_entity: '_2005.Bearing') -> 'Iterable[_3372.BearingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BearingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEARING](design_entity.wrapped if design_entity else None), constructor.new(_3372.BearingCompoundPowerFlow))

    def results_for_bolt(self, design_entity: '_2007.Bolt') -> 'Iterable[_3383.BoltCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BoltCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BOLT](design_entity.wrapped if design_entity else None), constructor.new(_3383.BoltCompoundPowerFlow))

    def results_for_bolted_joint(self, design_entity: '_2008.BoltedJoint') -> 'Iterable[_3384.BoltedJointCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BoltedJointCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BOLTED_JOINT](design_entity.wrapped if design_entity else None), constructor.new(_3384.BoltedJointCompoundPowerFlow))

    def results_for_component(self, design_entity: '_2009.Component') -> 'Iterable[_3389.ComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_3389.ComponentCompoundPowerFlow))

    def results_for_connector(self, design_entity: '_2012.Connector') -> 'Iterable[_3400.ConnectorCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConnectorCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONNECTOR](design_entity.wrapped if design_entity else None), constructor.new(_3400.ConnectorCompoundPowerFlow))

    def results_for_datum(self, design_entity: '_2013.Datum') -> 'Iterable[_3411.DatumCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.DatumCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_DATUM](design_entity.wrapped if design_entity else None), constructor.new(_3411.DatumCompoundPowerFlow))

    def results_for_external_cad_model(self, design_entity: '_2016.ExternalCADModel') -> 'Iterable[_3412.ExternalCADModelCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ExternalCADModelCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_EXTERNAL_CAD_MODEL](design_entity.wrapped if design_entity else None), constructor.new(_3412.ExternalCADModelCompoundPowerFlow))

    def results_for_flexible_pin_assembly(self, design_entity: '_2017.FlexiblePinAssembly') -> 'Iterable[_3416.FlexiblePinAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FlexiblePinAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_3416.FlexiblePinAssemblyCompoundPowerFlow))

    def results_for_assembly(self, design_entity: '_2000.Assembly') -> 'Iterable[_3371.AssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_3371.AssemblyCompoundPowerFlow))

    def results_for_guide_dxf_model(self, design_entity: '_2018.GuideDxfModel') -> 'Iterable[_3420.GuideDxfModelCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GuideDxfModelCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GUIDE_DXF_MODEL](design_entity.wrapped if design_entity else None), constructor.new(_3420.GuideDxfModelCompoundPowerFlow))

    def results_for_imported_fe_component(self, design_entity: '_2021.ImportedFEComponent') -> 'Iterable[_3424.ImportedFEComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ImportedFEComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_IMPORTED_FE_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_3424.ImportedFEComponentCompoundPowerFlow))

    def results_for_mass_disc(self, design_entity: '_2025.MassDisc') -> 'Iterable[_3435.MassDiscCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MassDiscCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MASS_DISC](design_entity.wrapped if design_entity else None), constructor.new(_3435.MassDiscCompoundPowerFlow))

    def results_for_measurement_component(self, design_entity: '_2026.MeasurementComponent') -> 'Iterable[_3436.MeasurementComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MeasurementComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MEASUREMENT_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_3436.MeasurementComponentCompoundPowerFlow))

    def results_for_mountable_component(self, design_entity: '_2027.MountableComponent') -> 'Iterable[_3437.MountableComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MountableComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MOUNTABLE_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_3437.MountableComponentCompoundPowerFlow))

    def results_for_oil_seal(self, design_entity: '_2029.OilSeal') -> 'Iterable[_3438.OilSealCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.OilSealCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_OIL_SEAL](design_entity.wrapped if design_entity else None), constructor.new(_3438.OilSealCompoundPowerFlow))

    def results_for_part(self, design_entity: '_2031.Part') -> 'Iterable[_3439.PartCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART](design_entity.wrapped if design_entity else None), constructor.new(_3439.PartCompoundPowerFlow))

    def results_for_planet_carrier(self, design_entity: '_2032.PlanetCarrier') -> 'Iterable[_3445.PlanetCarrierCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetCarrierCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANET_CARRIER](design_entity.wrapped if design_entity else None), constructor.new(_3445.PlanetCarrierCompoundPowerFlow))

    def results_for_point_load(self, design_entity: '_2034.PointLoad') -> 'Iterable[_3446.PointLoadCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PointLoadCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_POINT_LOAD](design_entity.wrapped if design_entity else None), constructor.new(_3446.PointLoadCompoundPowerFlow))

    def results_for_power_load(self, design_entity: '_2035.PowerLoad') -> 'Iterable[_3447.PowerLoadCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PowerLoadCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_POWER_LOAD](design_entity.wrapped if design_entity else None), constructor.new(_3447.PowerLoadCompoundPowerFlow))

    def results_for_root_assembly(self, design_entity: '_2037.RootAssembly') -> 'Iterable[_3452.RootAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RootAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROOT_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_3452.RootAssemblyCompoundPowerFlow))

    def results_for_specialised_assembly(self, design_entity: '_2039.SpecialisedAssembly') -> 'Iterable[_3456.SpecialisedAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpecialisedAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPECIALISED_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_3456.SpecialisedAssemblyCompoundPowerFlow))

    def results_for_unbalanced_mass(self, design_entity: '_2040.UnbalancedMass') -> 'Iterable[_3479.UnbalancedMassCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.UnbalancedMassCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_UNBALANCED_MASS](design_entity.wrapped if design_entity else None), constructor.new(_3479.UnbalancedMassCompoundPowerFlow))

    def results_for_virtual_component(self, design_entity: '_2041.VirtualComponent') -> 'Iterable[_3480.VirtualComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.VirtualComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_VIRTUAL_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_3480.VirtualComponentCompoundPowerFlow))

    def results_for_shaft(self, design_entity: '_2044.Shaft') -> 'Iterable[_3453.ShaftCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT](design_entity.wrapped if design_entity else None), constructor.new(_3453.ShaftCompoundPowerFlow))

    def results_for_concept_gear(self, design_entity: '_2082.ConceptGear') -> 'Iterable[_3393.ConceptGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3393.ConceptGearCompoundPowerFlow))

    def results_for_concept_gear_set(self, design_entity: '_2083.ConceptGearSet') -> 'Iterable[_3395.ConceptGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3395.ConceptGearSetCompoundPowerFlow))

    def results_for_face_gear(self, design_entity: '_2089.FaceGear') -> 'Iterable[_3413.FaceGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3413.FaceGearCompoundPowerFlow))

    def results_for_face_gear_set(self, design_entity: '_2090.FaceGearSet') -> 'Iterable[_3415.FaceGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3415.FaceGearSetCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2074.AGMAGleasonConicalGear') -> 'Iterable[_3368.AGMAGleasonConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3368.AGMAGleasonConicalGearCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2075.AGMAGleasonConicalGearSet') -> 'Iterable[_3370.AGMAGleasonConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3370.AGMAGleasonConicalGearSetCompoundPowerFlow))

    def results_for_bevel_differential_gear(self, design_entity: '_2076.BevelDifferentialGear') -> 'Iterable[_3375.BevelDifferentialGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3375.BevelDifferentialGearCompoundPowerFlow))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2077.BevelDifferentialGearSet') -> 'Iterable[_3377.BevelDifferentialGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3377.BevelDifferentialGearSetCompoundPowerFlow))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2078.BevelDifferentialPlanetGear') -> 'Iterable[_3378.BevelDifferentialPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3378.BevelDifferentialPlanetGearCompoundPowerFlow))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2079.BevelDifferentialSunGear') -> 'Iterable[_3379.BevelDifferentialSunGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialSunGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3379.BevelDifferentialSunGearCompoundPowerFlow))

    def results_for_bevel_gear(self, design_entity: '_2080.BevelGear') -> 'Iterable[_3380.BevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3380.BevelGearCompoundPowerFlow))

    def results_for_bevel_gear_set(self, design_entity: '_2081.BevelGearSet') -> 'Iterable[_3382.BevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3382.BevelGearSetCompoundPowerFlow))

    def results_for_conical_gear(self, design_entity: '_2084.ConicalGear') -> 'Iterable[_3396.ConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3396.ConicalGearCompoundPowerFlow))

    def results_for_conical_gear_set(self, design_entity: '_2085.ConicalGearSet') -> 'Iterable[_3398.ConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3398.ConicalGearSetCompoundPowerFlow))

    def results_for_cylindrical_gear(self, design_entity: '_2086.CylindricalGear') -> 'Iterable[_3407.CylindricalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3407.CylindricalGearCompoundPowerFlow))

    def results_for_cylindrical_gear_set(self, design_entity: '_2087.CylindricalGearSet') -> 'Iterable[_3409.CylindricalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3409.CylindricalGearSetCompoundPowerFlow))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2088.CylindricalPlanetGear') -> 'Iterable[_3410.CylindricalPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3410.CylindricalPlanetGearCompoundPowerFlow))

    def results_for_gear(self, design_entity: '_2091.Gear') -> 'Iterable[_3417.GearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3417.GearCompoundPowerFlow))

    def results_for_gear_set(self, design_entity: '_2093.GearSet') -> 'Iterable[_3419.GearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3419.GearSetCompoundPowerFlow))

    def results_for_hypoid_gear(self, design_entity: '_2095.HypoidGear') -> 'Iterable[_3421.HypoidGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3421.HypoidGearCompoundPowerFlow))

    def results_for_hypoid_gear_set(self, design_entity: '_2096.HypoidGearSet') -> 'Iterable[_3423.HypoidGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3423.HypoidGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2097.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_3426.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3426.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2098.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_3428.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3428.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2099.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_3429.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3429.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2100.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_3431.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3431.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2101.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_3432.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3432.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2102.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_3434.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3434.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow))

    def results_for_planetary_gear_set(self, design_entity: '_2103.PlanetaryGearSet') -> 'Iterable[_3444.PlanetaryGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetaryGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANETARY_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3444.PlanetaryGearSetCompoundPowerFlow))

    def results_for_spiral_bevel_gear(self, design_entity: '_2104.SpiralBevelGear') -> 'Iterable[_3457.SpiralBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3457.SpiralBevelGearCompoundPowerFlow))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2105.SpiralBevelGearSet') -> 'Iterable[_3459.SpiralBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3459.SpiralBevelGearSetCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2106.StraightBevelDiffGear') -> 'Iterable[_3463.StraightBevelDiffGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3463.StraightBevelDiffGearCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2107.StraightBevelDiffGearSet') -> 'Iterable[_3465.StraightBevelDiffGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3465.StraightBevelDiffGearSetCompoundPowerFlow))

    def results_for_straight_bevel_gear(self, design_entity: '_2108.StraightBevelGear') -> 'Iterable[_3466.StraightBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3466.StraightBevelGearCompoundPowerFlow))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2109.StraightBevelGearSet') -> 'Iterable[_3468.StraightBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3468.StraightBevelGearSetCompoundPowerFlow))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2110.StraightBevelPlanetGear') -> 'Iterable[_3469.StraightBevelPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3469.StraightBevelPlanetGearCompoundPowerFlow))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2111.StraightBevelSunGear') -> 'Iterable[_3470.StraightBevelSunGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelSunGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3470.StraightBevelSunGearCompoundPowerFlow))

    def results_for_worm_gear(self, design_entity: '_2112.WormGear') -> 'Iterable[_3481.WormGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3481.WormGearCompoundPowerFlow))

    def results_for_worm_gear_set(self, design_entity: '_2113.WormGearSet') -> 'Iterable[_3483.WormGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3483.WormGearSetCompoundPowerFlow))

    def results_for_zerol_bevel_gear(self, design_entity: '_2114.ZerolBevelGear') -> 'Iterable[_3484.ZerolBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_3484.ZerolBevelGearCompoundPowerFlow))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2115.ZerolBevelGearSet') -> 'Iterable[_3486.ZerolBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_3486.ZerolBevelGearSetCompoundPowerFlow))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2144.PartToPartShearCoupling') -> 'Iterable[_3440.PartToPartShearCouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartToPartShearCouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_3440.PartToPartShearCouplingCompoundPowerFlow))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2145.PartToPartShearCouplingHalf') -> 'Iterable[_3442.PartToPartShearCouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartToPartShearCouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_3442.PartToPartShearCouplingHalfCompoundPowerFlow))

    def results_for_belt_drive(self, design_entity: '_2133.BeltDrive') -> 'Iterable[_3374.BeltDriveCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BeltDriveCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BELT_DRIVE](design_entity.wrapped if design_entity else None), constructor.new(_3374.BeltDriveCompoundPowerFlow))

    def results_for_clutch(self, design_entity: '_2135.Clutch') -> 'Iterable[_3385.ClutchCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH](design_entity.wrapped if design_entity else None), constructor.new(_3385.ClutchCompoundPowerFlow))

    def results_for_clutch_half(self, design_entity: '_2136.ClutchHalf') -> 'Iterable[_3387.ClutchHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH_HALF](design_entity.wrapped if design_entity else None), constructor.new(_3387.ClutchHalfCompoundPowerFlow))

    def results_for_concept_coupling(self, design_entity: '_2138.ConceptCoupling') -> 'Iterable[_3390.ConceptCouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_3390.ConceptCouplingCompoundPowerFlow))

    def results_for_concept_coupling_half(self, design_entity: '_2139.ConceptCouplingHalf') -> 'Iterable[_3392.ConceptCouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_3392.ConceptCouplingHalfCompoundPowerFlow))

    def results_for_coupling(self, design_entity: '_2140.Coupling') -> 'Iterable[_3401.CouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_3401.CouplingCompoundPowerFlow))

    def results_for_coupling_half(self, design_entity: '_2141.CouplingHalf') -> 'Iterable[_3403.CouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_3403.CouplingHalfCompoundPowerFlow))

    def results_for_cvt(self, design_entity: '_2142.CVT') -> 'Iterable[_3405.CVTCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT](design_entity.wrapped if design_entity else None), constructor.new(_3405.CVTCompoundPowerFlow))

    def results_for_cvt_pulley(self, design_entity: '_2143.CVTPulley') -> 'Iterable[_3406.CVTPulleyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTPulleyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT_PULLEY](design_entity.wrapped if design_entity else None), constructor.new(_3406.CVTPulleyCompoundPowerFlow))

    def results_for_pulley(self, design_entity: '_2146.Pulley') -> 'Iterable[_3448.PulleyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PulleyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PULLEY](design_entity.wrapped if design_entity else None), constructor.new(_3448.PulleyCompoundPowerFlow))

    def results_for_shaft_hub_connection(self, design_entity: '_2154.ShaftHubConnection') -> 'Iterable[_3454.ShaftHubConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftHubConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT_HUB_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3454.ShaftHubConnectionCompoundPowerFlow))

    def results_for_rolling_ring(self, design_entity: '_2152.RollingRing') -> 'Iterable[_3450.RollingRingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING](design_entity.wrapped if design_entity else None), constructor.new(_3450.RollingRingCompoundPowerFlow))

    def results_for_rolling_ring_assembly(self, design_entity: '_2153.RollingRingAssembly') -> 'Iterable[_3449.RollingRingAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_3449.RollingRingAssemblyCompoundPowerFlow))

    def results_for_spring_damper(self, design_entity: '_2155.SpringDamper') -> 'Iterable[_3460.SpringDamperCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER](design_entity.wrapped if design_entity else None), constructor.new(_3460.SpringDamperCompoundPowerFlow))

    def results_for_spring_damper_half(self, design_entity: '_2156.SpringDamperHalf') -> 'Iterable[_3462.SpringDamperHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_HALF](design_entity.wrapped if design_entity else None), constructor.new(_3462.SpringDamperHalfCompoundPowerFlow))

    def results_for_synchroniser(self, design_entity: '_2157.Synchroniser') -> 'Iterable[_3471.SynchroniserCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER](design_entity.wrapped if design_entity else None), constructor.new(_3471.SynchroniserCompoundPowerFlow))

    def results_for_synchroniser_half(self, design_entity: '_2159.SynchroniserHalf') -> 'Iterable[_3472.SynchroniserHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_HALF](design_entity.wrapped if design_entity else None), constructor.new(_3472.SynchroniserHalfCompoundPowerFlow))

    def results_for_synchroniser_part(self, design_entity: '_2160.SynchroniserPart') -> 'Iterable[_3473.SynchroniserPartCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserPartCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_PART](design_entity.wrapped if design_entity else None), constructor.new(_3473.SynchroniserPartCompoundPowerFlow))

    def results_for_synchroniser_sleeve(self, design_entity: '_2161.SynchroniserSleeve') -> 'Iterable[_3474.SynchroniserSleeveCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserSleeveCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_SLEEVE](design_entity.wrapped if design_entity else None), constructor.new(_3474.SynchroniserSleeveCompoundPowerFlow))

    def results_for_torque_converter(self, design_entity: '_2162.TorqueConverter') -> 'Iterable[_3475.TorqueConverterCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER](design_entity.wrapped if design_entity else None), constructor.new(_3475.TorqueConverterCompoundPowerFlow))

    def results_for_torque_converter_pump(self, design_entity: '_2163.TorqueConverterPump') -> 'Iterable[_3477.TorqueConverterPumpCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterPumpCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_PUMP](design_entity.wrapped if design_entity else None), constructor.new(_3477.TorqueConverterPumpCompoundPowerFlow))

    def results_for_torque_converter_turbine(self, design_entity: '_2165.TorqueConverterTurbine') -> 'Iterable[_3478.TorqueConverterTurbineCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterTurbineCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_TURBINE](design_entity.wrapped if design_entity else None), constructor.new(_3478.TorqueConverterTurbineCompoundPowerFlow))

    def results_for_cvt_belt_connection(self, design_entity: '_1856.CVTBeltConnection') -> 'Iterable[_3404.CVTBeltConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTBeltConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT_BELT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3404.CVTBeltConnectionCompoundPowerFlow))

    def results_for_belt_connection(self, design_entity: '_1851.BeltConnection') -> 'Iterable[_3373.BeltConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BeltConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BELT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3373.BeltConnectionCompoundPowerFlow))

    def results_for_coaxial_connection(self, design_entity: '_1852.CoaxialConnection') -> 'Iterable[_3388.CoaxialConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CoaxialConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COAXIAL_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3388.CoaxialConnectionCompoundPowerFlow))

    def results_for_connection(self, design_entity: '_1855.Connection') -> 'Iterable[_3399.ConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3399.ConnectionCompoundPowerFlow))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1864.InterMountableComponentConnection') -> 'Iterable[_3425.InterMountableComponentConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.InterMountableComponentConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3425.InterMountableComponentConnectionCompoundPowerFlow))

    def results_for_planetary_connection(self, design_entity: '_1867.PlanetaryConnection') -> 'Iterable[_3443.PlanetaryConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetaryConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANETARY_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3443.PlanetaryConnectionCompoundPowerFlow))

    def results_for_rolling_ring_connection(self, design_entity: '_1871.RollingRingConnection') -> 'Iterable[_3451.RollingRingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3451.RollingRingConnectionCompoundPowerFlow))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1875.ShaftToMountableComponentConnection') -> 'Iterable[_3455.ShaftToMountableComponentConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftToMountableComponentConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3455.ShaftToMountableComponentConnectionCompoundPowerFlow))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1881.BevelDifferentialGearMesh') -> 'Iterable[_3376.BevelDifferentialGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3376.BevelDifferentialGearMeshCompoundPowerFlow))

    def results_for_concept_gear_mesh(self, design_entity: '_1885.ConceptGearMesh') -> 'Iterable[_3394.ConceptGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3394.ConceptGearMeshCompoundPowerFlow))

    def results_for_face_gear_mesh(self, design_entity: '_1891.FaceGearMesh') -> 'Iterable[_3414.FaceGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3414.FaceGearMeshCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1905.StraightBevelDiffGearMesh') -> 'Iterable[_3464.StraightBevelDiffGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3464.StraightBevelDiffGearMeshCompoundPowerFlow))

    def results_for_bevel_gear_mesh(self, design_entity: '_1883.BevelGearMesh') -> 'Iterable[_3381.BevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3381.BevelGearMeshCompoundPowerFlow))

    def results_for_conical_gear_mesh(self, design_entity: '_1887.ConicalGearMesh') -> 'Iterable[_3397.ConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3397.ConicalGearMeshCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1879.AGMAGleasonConicalGearMesh') -> 'Iterable[_3369.AGMAGleasonConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3369.AGMAGleasonConicalGearMeshCompoundPowerFlow))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1889.CylindricalGearMesh') -> 'Iterable[_3408.CylindricalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3408.CylindricalGearMeshCompoundPowerFlow))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1895.HypoidGearMesh') -> 'Iterable[_3422.HypoidGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3422.HypoidGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1898.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_3427.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3427.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1899.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_3430.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3430.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1900.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_3433.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3433.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1903.SpiralBevelGearMesh') -> 'Iterable[_3458.SpiralBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3458.SpiralBevelGearMeshCompoundPowerFlow))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1907.StraightBevelGearMesh') -> 'Iterable[_3467.StraightBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3467.StraightBevelGearMeshCompoundPowerFlow))

    def results_for_worm_gear_mesh(self, design_entity: '_1909.WormGearMesh') -> 'Iterable[_3482.WormGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3482.WormGearMeshCompoundPowerFlow))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1911.ZerolBevelGearMesh') -> 'Iterable[_3485.ZerolBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3485.ZerolBevelGearMeshCompoundPowerFlow))

    def results_for_gear_mesh(self, design_entity: '_1893.GearMesh') -> 'Iterable[_3418.GearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_3418.GearMeshCompoundPowerFlow))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1919.PartToPartShearCouplingConnection') -> 'Iterable[_3441.PartToPartShearCouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartToPartShearCouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3441.PartToPartShearCouplingConnectionCompoundPowerFlow))

    def results_for_clutch_connection(self, design_entity: '_1913.ClutchConnection') -> 'Iterable[_3386.ClutchConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3386.ClutchConnectionCompoundPowerFlow))

    def results_for_concept_coupling_connection(self, design_entity: '_1915.ConceptCouplingConnection') -> 'Iterable[_3391.ConceptCouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3391.ConceptCouplingConnectionCompoundPowerFlow))

    def results_for_coupling_connection(self, design_entity: '_1917.CouplingConnection') -> 'Iterable[_3402.CouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3402.CouplingConnectionCompoundPowerFlow))

    def results_for_spring_damper_connection(self, design_entity: '_1921.SpringDamperConnection') -> 'Iterable[_3461.SpringDamperConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3461.SpringDamperConnectionCompoundPowerFlow))

    def results_for_torque_converter_connection(self, design_entity: '_1923.TorqueConverterConnection') -> 'Iterable[_3476.TorqueConverterConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_3476.TorqueConverterConnectionCompoundPowerFlow))
