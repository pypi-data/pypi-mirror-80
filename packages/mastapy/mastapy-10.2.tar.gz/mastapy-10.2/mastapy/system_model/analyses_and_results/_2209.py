'''_2209.py

CompoundDynamicAnalysisAnalysis
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
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import (
    _5947, _5948, _5953, _5964,
    _5965, _5970, _5981, _5992,
    _5993, _5997, _5952, _6001,
    _6005, _6016, _6017, _6018,
    _6019, _6020, _6026, _6027,
    _6028, _6033, _6037, _6060,
    _6061, _6034, _5974, _5976,
    _5994, _5996, _5949, _5951,
    _5956, _5958, _5959, _5960,
    _5961, _5963, _5977, _5979,
    _5988, _5990, _5991, _5998,
    _6000, _6002, _6004, _6007,
    _6009, _6010, _6012, _6013,
    _6015, _6025, _6038, _6040,
    _6044, _6046, _6047, _6049,
    _6050, _6051, _6062, _6064,
    _6065, _6067, _6021, _6023,
    _5955, _5966, _5968, _5971,
    _5973, _5982, _5984, _5986,
    _5987, _6029, _6035, _6031,
    _6030, _6041, _6043, _6052,
    _6053, _6054, _6055, _6056,
    _6058, _6059, _5985, _5954,
    _5969, _5980, _6006, _6024,
    _6032, _6036, _5957, _5975,
    _5995, _6045, _5962, _5978,
    _5950, _5989, _6003, _6008,
    _6011, _6014, _6039, _6048,
    _6063, _6066, _5999, _6022,
    _5967, _5972, _5983, _6042,
    _6057
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
_COMPOUND_DYNAMIC_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundDynamicAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundDynamicAnalysisAnalysis',)


class CompoundDynamicAnalysisAnalysis(_2174.CompoundAnalysis):
    '''CompoundDynamicAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_DYNAMIC_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundDynamicAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def results_for_abstract_assembly(self, design_entity: '_2001.AbstractAssembly') -> 'Iterable[_5947.AbstractAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AbstractAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5947.AbstractAssemblyCompoundDynamicAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_2002.AbstractShaftOrHousing') -> 'Iterable[_5948.AbstractShaftOrHousingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AbstractShaftOrHousingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING](design_entity.wrapped if design_entity else None), constructor.new(_5948.AbstractShaftOrHousingCompoundDynamicAnalysis))

    def results_for_bearing(self, design_entity: '_2005.Bearing') -> 'Iterable[_5953.BearingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BearingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEARING](design_entity.wrapped if design_entity else None), constructor.new(_5953.BearingCompoundDynamicAnalysis))

    def results_for_bolt(self, design_entity: '_2007.Bolt') -> 'Iterable[_5964.BoltCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BoltCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BOLT](design_entity.wrapped if design_entity else None), constructor.new(_5964.BoltCompoundDynamicAnalysis))

    def results_for_bolted_joint(self, design_entity: '_2008.BoltedJoint') -> 'Iterable[_5965.BoltedJointCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BoltedJointCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BOLTED_JOINT](design_entity.wrapped if design_entity else None), constructor.new(_5965.BoltedJointCompoundDynamicAnalysis))

    def results_for_component(self, design_entity: '_2009.Component') -> 'Iterable[_5970.ComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_5970.ComponentCompoundDynamicAnalysis))

    def results_for_connector(self, design_entity: '_2012.Connector') -> 'Iterable[_5981.ConnectorCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConnectorCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONNECTOR](design_entity.wrapped if design_entity else None), constructor.new(_5981.ConnectorCompoundDynamicAnalysis))

    def results_for_datum(self, design_entity: '_2013.Datum') -> 'Iterable[_5992.DatumCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.DatumCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_DATUM](design_entity.wrapped if design_entity else None), constructor.new(_5992.DatumCompoundDynamicAnalysis))

    def results_for_external_cad_model(self, design_entity: '_2016.ExternalCADModel') -> 'Iterable[_5993.ExternalCADModelCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ExternalCADModelCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_EXTERNAL_CAD_MODEL](design_entity.wrapped if design_entity else None), constructor.new(_5993.ExternalCADModelCompoundDynamicAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_2017.FlexiblePinAssembly') -> 'Iterable[_5997.FlexiblePinAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FlexiblePinAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5997.FlexiblePinAssemblyCompoundDynamicAnalysis))

    def results_for_assembly(self, design_entity: '_2000.Assembly') -> 'Iterable[_5952.AssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_5952.AssemblyCompoundDynamicAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_2018.GuideDxfModel') -> 'Iterable[_6001.GuideDxfModelCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GuideDxfModelCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GUIDE_DXF_MODEL](design_entity.wrapped if design_entity else None), constructor.new(_6001.GuideDxfModelCompoundDynamicAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_2021.ImportedFEComponent') -> 'Iterable[_6005.ImportedFEComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ImportedFEComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_IMPORTED_FE_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_6005.ImportedFEComponentCompoundDynamicAnalysis))

    def results_for_mass_disc(self, design_entity: '_2025.MassDisc') -> 'Iterable[_6016.MassDiscCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MassDiscCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MASS_DISC](design_entity.wrapped if design_entity else None), constructor.new(_6016.MassDiscCompoundDynamicAnalysis))

    def results_for_measurement_component(self, design_entity: '_2026.MeasurementComponent') -> 'Iterable[_6017.MeasurementComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MeasurementComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MEASUREMENT_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_6017.MeasurementComponentCompoundDynamicAnalysis))

    def results_for_mountable_component(self, design_entity: '_2027.MountableComponent') -> 'Iterable[_6018.MountableComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MountableComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MOUNTABLE_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_6018.MountableComponentCompoundDynamicAnalysis))

    def results_for_oil_seal(self, design_entity: '_2029.OilSeal') -> 'Iterable[_6019.OilSealCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.OilSealCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_OIL_SEAL](design_entity.wrapped if design_entity else None), constructor.new(_6019.OilSealCompoundDynamicAnalysis))

    def results_for_part(self, design_entity: '_2031.Part') -> 'Iterable[_6020.PartCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART](design_entity.wrapped if design_entity else None), constructor.new(_6020.PartCompoundDynamicAnalysis))

    def results_for_planet_carrier(self, design_entity: '_2032.PlanetCarrier') -> 'Iterable[_6026.PlanetCarrierCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetCarrierCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANET_CARRIER](design_entity.wrapped if design_entity else None), constructor.new(_6026.PlanetCarrierCompoundDynamicAnalysis))

    def results_for_point_load(self, design_entity: '_2034.PointLoad') -> 'Iterable[_6027.PointLoadCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PointLoadCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_POINT_LOAD](design_entity.wrapped if design_entity else None), constructor.new(_6027.PointLoadCompoundDynamicAnalysis))

    def results_for_power_load(self, design_entity: '_2035.PowerLoad') -> 'Iterable[_6028.PowerLoadCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PowerLoadCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_POWER_LOAD](design_entity.wrapped if design_entity else None), constructor.new(_6028.PowerLoadCompoundDynamicAnalysis))

    def results_for_root_assembly(self, design_entity: '_2037.RootAssembly') -> 'Iterable[_6033.RootAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RootAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROOT_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_6033.RootAssemblyCompoundDynamicAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_2039.SpecialisedAssembly') -> 'Iterable[_6037.SpecialisedAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpecialisedAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPECIALISED_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_6037.SpecialisedAssemblyCompoundDynamicAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_2040.UnbalancedMass') -> 'Iterable[_6060.UnbalancedMassCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.UnbalancedMassCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_UNBALANCED_MASS](design_entity.wrapped if design_entity else None), constructor.new(_6060.UnbalancedMassCompoundDynamicAnalysis))

    def results_for_virtual_component(self, design_entity: '_2041.VirtualComponent') -> 'Iterable[_6061.VirtualComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.VirtualComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_VIRTUAL_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_6061.VirtualComponentCompoundDynamicAnalysis))

    def results_for_shaft(self, design_entity: '_2044.Shaft') -> 'Iterable[_6034.ShaftCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT](design_entity.wrapped if design_entity else None), constructor.new(_6034.ShaftCompoundDynamicAnalysis))

    def results_for_concept_gear(self, design_entity: '_2082.ConceptGear') -> 'Iterable[_5974.ConceptGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5974.ConceptGearCompoundDynamicAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_2083.ConceptGearSet') -> 'Iterable[_5976.ConceptGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5976.ConceptGearSetCompoundDynamicAnalysis))

    def results_for_face_gear(self, design_entity: '_2089.FaceGear') -> 'Iterable[_5994.FaceGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5994.FaceGearCompoundDynamicAnalysis))

    def results_for_face_gear_set(self, design_entity: '_2090.FaceGearSet') -> 'Iterable[_5996.FaceGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5996.FaceGearSetCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2074.AGMAGleasonConicalGear') -> 'Iterable[_5949.AGMAGleasonConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5949.AGMAGleasonConicalGearCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2075.AGMAGleasonConicalGearSet') -> 'Iterable[_5951.AGMAGleasonConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5951.AGMAGleasonConicalGearSetCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2076.BevelDifferentialGear') -> 'Iterable[_5956.BevelDifferentialGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5956.BevelDifferentialGearCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2077.BevelDifferentialGearSet') -> 'Iterable[_5958.BevelDifferentialGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5958.BevelDifferentialGearSetCompoundDynamicAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2078.BevelDifferentialPlanetGear') -> 'Iterable[_5959.BevelDifferentialPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5959.BevelDifferentialPlanetGearCompoundDynamicAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2079.BevelDifferentialSunGear') -> 'Iterable[_5960.BevelDifferentialSunGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialSunGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5960.BevelDifferentialSunGearCompoundDynamicAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2080.BevelGear') -> 'Iterable[_5961.BevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5961.BevelGearCompoundDynamicAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_2081.BevelGearSet') -> 'Iterable[_5963.BevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5963.BevelGearSetCompoundDynamicAnalysis))

    def results_for_conical_gear(self, design_entity: '_2084.ConicalGear') -> 'Iterable[_5977.ConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5977.ConicalGearCompoundDynamicAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_2085.ConicalGearSet') -> 'Iterable[_5979.ConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5979.ConicalGearSetCompoundDynamicAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_2086.CylindricalGear') -> 'Iterable[_5988.CylindricalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5988.CylindricalGearCompoundDynamicAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_2087.CylindricalGearSet') -> 'Iterable[_5990.CylindricalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_5990.CylindricalGearSetCompoundDynamicAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2088.CylindricalPlanetGear') -> 'Iterable[_5991.CylindricalPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5991.CylindricalPlanetGearCompoundDynamicAnalysis))

    def results_for_gear(self, design_entity: '_2091.Gear') -> 'Iterable[_5998.GearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_5998.GearCompoundDynamicAnalysis))

    def results_for_gear_set(self, design_entity: '_2093.GearSet') -> 'Iterable[_6000.GearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6000.GearSetCompoundDynamicAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2095.HypoidGear') -> 'Iterable[_6002.HypoidGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6002.HypoidGearCompoundDynamicAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_2096.HypoidGearSet') -> 'Iterable[_6004.HypoidGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6004.HypoidGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2097.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_6007.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6007.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2098.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_6009.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6009.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2099.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_6010.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6010.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2100.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_6012.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6012.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2101.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_6013.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6013.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2102.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_6015.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6015.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_2103.PlanetaryGearSet') -> 'Iterable[_6025.PlanetaryGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetaryGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANETARY_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6025.PlanetaryGearSetCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2104.SpiralBevelGear') -> 'Iterable[_6038.SpiralBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6038.SpiralBevelGearCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2105.SpiralBevelGearSet') -> 'Iterable[_6040.SpiralBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6040.SpiralBevelGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2106.StraightBevelDiffGear') -> 'Iterable[_6044.StraightBevelDiffGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6044.StraightBevelDiffGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2107.StraightBevelDiffGearSet') -> 'Iterable[_6046.StraightBevelDiffGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6046.StraightBevelDiffGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2108.StraightBevelGear') -> 'Iterable[_6047.StraightBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6047.StraightBevelGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2109.StraightBevelGearSet') -> 'Iterable[_6049.StraightBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6049.StraightBevelGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2110.StraightBevelPlanetGear') -> 'Iterable[_6050.StraightBevelPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6050.StraightBevelPlanetGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2111.StraightBevelSunGear') -> 'Iterable[_6051.StraightBevelSunGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelSunGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6051.StraightBevelSunGearCompoundDynamicAnalysis))

    def results_for_worm_gear(self, design_entity: '_2112.WormGear') -> 'Iterable[_6062.WormGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6062.WormGearCompoundDynamicAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_2113.WormGearSet') -> 'Iterable[_6064.WormGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6064.WormGearSetCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2114.ZerolBevelGear') -> 'Iterable[_6065.ZerolBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_6065.ZerolBevelGearCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2115.ZerolBevelGearSet') -> 'Iterable[_6067.ZerolBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_6067.ZerolBevelGearSetCompoundDynamicAnalysis))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2144.PartToPartShearCoupling') -> 'Iterable[_6021.PartToPartShearCouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartToPartShearCouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_6021.PartToPartShearCouplingCompoundDynamicAnalysis))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2145.PartToPartShearCouplingHalf') -> 'Iterable[_6023.PartToPartShearCouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartToPartShearCouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_6023.PartToPartShearCouplingHalfCompoundDynamicAnalysis))

    def results_for_belt_drive(self, design_entity: '_2133.BeltDrive') -> 'Iterable[_5955.BeltDriveCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BeltDriveCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BELT_DRIVE](design_entity.wrapped if design_entity else None), constructor.new(_5955.BeltDriveCompoundDynamicAnalysis))

    def results_for_clutch(self, design_entity: '_2135.Clutch') -> 'Iterable[_5966.ClutchCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH](design_entity.wrapped if design_entity else None), constructor.new(_5966.ClutchCompoundDynamicAnalysis))

    def results_for_clutch_half(self, design_entity: '_2136.ClutchHalf') -> 'Iterable[_5968.ClutchHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5968.ClutchHalfCompoundDynamicAnalysis))

    def results_for_concept_coupling(self, design_entity: '_2138.ConceptCoupling') -> 'Iterable[_5971.ConceptCouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_5971.ConceptCouplingCompoundDynamicAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2139.ConceptCouplingHalf') -> 'Iterable[_5973.ConceptCouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5973.ConceptCouplingHalfCompoundDynamicAnalysis))

    def results_for_coupling(self, design_entity: '_2140.Coupling') -> 'Iterable[_5982.CouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_5982.CouplingCompoundDynamicAnalysis))

    def results_for_coupling_half(self, design_entity: '_2141.CouplingHalf') -> 'Iterable[_5984.CouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_5984.CouplingHalfCompoundDynamicAnalysis))

    def results_for_cvt(self, design_entity: '_2142.CVT') -> 'Iterable[_5986.CVTCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT](design_entity.wrapped if design_entity else None), constructor.new(_5986.CVTCompoundDynamicAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2143.CVTPulley') -> 'Iterable[_5987.CVTPulleyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTPulleyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT_PULLEY](design_entity.wrapped if design_entity else None), constructor.new(_5987.CVTPulleyCompoundDynamicAnalysis))

    def results_for_pulley(self, design_entity: '_2146.Pulley') -> 'Iterable[_6029.PulleyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PulleyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PULLEY](design_entity.wrapped if design_entity else None), constructor.new(_6029.PulleyCompoundDynamicAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_2154.ShaftHubConnection') -> 'Iterable[_6035.ShaftHubConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftHubConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT_HUB_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_6035.ShaftHubConnectionCompoundDynamicAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2152.RollingRing') -> 'Iterable[_6031.RollingRingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING](design_entity.wrapped if design_entity else None), constructor.new(_6031.RollingRingCompoundDynamicAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_2153.RollingRingAssembly') -> 'Iterable[_6030.RollingRingAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_6030.RollingRingAssemblyCompoundDynamicAnalysis))

    def results_for_spring_damper(self, design_entity: '_2155.SpringDamper') -> 'Iterable[_6041.SpringDamperCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER](design_entity.wrapped if design_entity else None), constructor.new(_6041.SpringDamperCompoundDynamicAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2156.SpringDamperHalf') -> 'Iterable[_6043.SpringDamperHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_HALF](design_entity.wrapped if design_entity else None), constructor.new(_6043.SpringDamperHalfCompoundDynamicAnalysis))

    def results_for_synchroniser(self, design_entity: '_2157.Synchroniser') -> 'Iterable[_6052.SynchroniserCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER](design_entity.wrapped if design_entity else None), constructor.new(_6052.SynchroniserCompoundDynamicAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2159.SynchroniserHalf') -> 'Iterable[_6053.SynchroniserHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_HALF](design_entity.wrapped if design_entity else None), constructor.new(_6053.SynchroniserHalfCompoundDynamicAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2160.SynchroniserPart') -> 'Iterable[_6054.SynchroniserPartCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserPartCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_PART](design_entity.wrapped if design_entity else None), constructor.new(_6054.SynchroniserPartCompoundDynamicAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2161.SynchroniserSleeve') -> 'Iterable[_6055.SynchroniserSleeveCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserSleeveCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_SLEEVE](design_entity.wrapped if design_entity else None), constructor.new(_6055.SynchroniserSleeveCompoundDynamicAnalysis))

    def results_for_torque_converter(self, design_entity: '_2162.TorqueConverter') -> 'Iterable[_6056.TorqueConverterCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER](design_entity.wrapped if design_entity else None), constructor.new(_6056.TorqueConverterCompoundDynamicAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2163.TorqueConverterPump') -> 'Iterable[_6058.TorqueConverterPumpCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterPumpCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_PUMP](design_entity.wrapped if design_entity else None), constructor.new(_6058.TorqueConverterPumpCompoundDynamicAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2165.TorqueConverterTurbine') -> 'Iterable[_6059.TorqueConverterTurbineCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterTurbineCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_TURBINE](design_entity.wrapped if design_entity else None), constructor.new(_6059.TorqueConverterTurbineCompoundDynamicAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1856.CVTBeltConnection') -> 'Iterable[_5985.CVTBeltConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTBeltConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT_BELT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5985.CVTBeltConnectionCompoundDynamicAnalysis))

    def results_for_belt_connection(self, design_entity: '_1851.BeltConnection') -> 'Iterable[_5954.BeltConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BeltConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BELT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5954.BeltConnectionCompoundDynamicAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1852.CoaxialConnection') -> 'Iterable[_5969.CoaxialConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CoaxialConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COAXIAL_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5969.CoaxialConnectionCompoundDynamicAnalysis))

    def results_for_connection(self, design_entity: '_1855.Connection') -> 'Iterable[_5980.ConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5980.ConnectionCompoundDynamicAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1864.InterMountableComponentConnection') -> 'Iterable[_6006.InterMountableComponentConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.InterMountableComponentConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_6006.InterMountableComponentConnectionCompoundDynamicAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1867.PlanetaryConnection') -> 'Iterable[_6024.PlanetaryConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetaryConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANETARY_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_6024.PlanetaryConnectionCompoundDynamicAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1871.RollingRingConnection') -> 'Iterable[_6032.RollingRingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_6032.RollingRingConnectionCompoundDynamicAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1875.ShaftToMountableComponentConnection') -> 'Iterable[_6036.ShaftToMountableComponentConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftToMountableComponentConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_6036.ShaftToMountableComponentConnectionCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1881.BevelDifferentialGearMesh') -> 'Iterable[_5957.BevelDifferentialGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5957.BevelDifferentialGearMeshCompoundDynamicAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1885.ConceptGearMesh') -> 'Iterable[_5975.ConceptGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5975.ConceptGearMeshCompoundDynamicAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1891.FaceGearMesh') -> 'Iterable[_5995.FaceGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5995.FaceGearMeshCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1905.StraightBevelDiffGearMesh') -> 'Iterable[_6045.StraightBevelDiffGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_6045.StraightBevelDiffGearMeshCompoundDynamicAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1883.BevelGearMesh') -> 'Iterable[_5962.BevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5962.BevelGearMeshCompoundDynamicAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1887.ConicalGearMesh') -> 'Iterable[_5978.ConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5978.ConicalGearMeshCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1879.AGMAGleasonConicalGearMesh') -> 'Iterable[_5950.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5950.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1889.CylindricalGearMesh') -> 'Iterable[_5989.CylindricalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5989.CylindricalGearMeshCompoundDynamicAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1895.HypoidGearMesh') -> 'Iterable[_6003.HypoidGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_6003.HypoidGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1898.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_6008.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_6008.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1899.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_6011.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_6011.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1900.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_6014.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_6014.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1903.SpiralBevelGearMesh') -> 'Iterable[_6039.SpiralBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_6039.SpiralBevelGearMeshCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1907.StraightBevelGearMesh') -> 'Iterable[_6048.StraightBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_6048.StraightBevelGearMeshCompoundDynamicAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1909.WormGearMesh') -> 'Iterable[_6063.WormGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_6063.WormGearMeshCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1911.ZerolBevelGearMesh') -> 'Iterable[_6066.ZerolBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_6066.ZerolBevelGearMeshCompoundDynamicAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1893.GearMesh') -> 'Iterable[_5999.GearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_5999.GearMeshCompoundDynamicAnalysis))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1919.PartToPartShearCouplingConnection') -> 'Iterable[_6022.PartToPartShearCouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartToPartShearCouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_6022.PartToPartShearCouplingConnectionCompoundDynamicAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1913.ClutchConnection') -> 'Iterable[_5967.ClutchConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5967.ClutchConnectionCompoundDynamicAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1915.ConceptCouplingConnection') -> 'Iterable[_5972.ConceptCouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5972.ConceptCouplingConnectionCompoundDynamicAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1917.CouplingConnection') -> 'Iterable[_5983.CouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_5983.CouplingConnectionCompoundDynamicAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1921.SpringDamperConnection') -> 'Iterable[_6042.SpringDamperConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_6042.SpringDamperConnectionCompoundDynamicAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1923.TorqueConverterConnection') -> 'Iterable[_6057.TorqueConverterConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_6057.TorqueConverterConnectionCompoundDynamicAnalysis))
