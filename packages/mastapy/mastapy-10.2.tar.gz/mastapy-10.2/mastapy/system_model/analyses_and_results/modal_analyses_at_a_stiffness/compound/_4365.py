'''_4365.py

AssemblyCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _2000, _2037
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4242
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _4366, _4368, _4371, _4377,
    _4378, _4379, _4384, _4389,
    _4399, _4403, _4409, _4410,
    _4417, _4418, _4425, _4428,
    _4429, _4430, _4432, _4434,
    _4439, _4440, _4441, _4448,
    _4443, _4447, _4453, _4454,
    _4459, _4462, _4465, _4469,
    _4473, _4477, _4480, _4360
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'AssemblyCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysisAtAStiffness',)


class AssemblyCompoundModalAnalysisAtAStiffness(_4360.AbstractAssemblyCompoundModalAnalysisAtAStiffness):
    '''AssemblyCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2000.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2000.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4242.AssemblyModalAnalysisAtAStiffness]':
        '''List[AssemblyModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4242.AssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4242.AssemblyModalAnalysisAtAStiffness]':
        '''List[AssemblyModalAnalysisAtAStiffness]: 'AssemblyModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtAStiffnessLoadCases, constructor.new(_4242.AssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def bearings(self) -> 'List[_4366.BearingCompoundModalAnalysisAtAStiffness]':
        '''List[BearingCompoundModalAnalysisAtAStiffness]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4366.BearingCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def belt_drives(self) -> 'List[_4368.BeltDriveCompoundModalAnalysisAtAStiffness]':
        '''List[BeltDriveCompoundModalAnalysisAtAStiffness]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4368.BeltDriveCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4371.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4371.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def bolts(self) -> 'List[_4377.BoltCompoundModalAnalysisAtAStiffness]':
        '''List[BoltCompoundModalAnalysisAtAStiffness]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4377.BoltCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def bolted_joints(self) -> 'List[_4378.BoltedJointCompoundModalAnalysisAtAStiffness]':
        '''List[BoltedJointCompoundModalAnalysisAtAStiffness]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4378.BoltedJointCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def clutches(self) -> 'List[_4379.ClutchCompoundModalAnalysisAtAStiffness]':
        '''List[ClutchCompoundModalAnalysisAtAStiffness]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4379.ClutchCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def concept_couplings(self) -> 'List[_4384.ConceptCouplingCompoundModalAnalysisAtAStiffness]':
        '''List[ConceptCouplingCompoundModalAnalysisAtAStiffness]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4384.ConceptCouplingCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4389.ConceptGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[ConceptGearSetCompoundModalAnalysisAtAStiffness]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4389.ConceptGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def cv_ts(self) -> 'List[_4399.CVTCompoundModalAnalysisAtAStiffness]':
        '''List[CVTCompoundModalAnalysisAtAStiffness]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4399.CVTCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4403.CylindricalGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[CylindricalGearSetCompoundModalAnalysisAtAStiffness]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4403.CylindricalGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4409.FaceGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[FaceGearSetCompoundModalAnalysisAtAStiffness]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4409.FaceGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4410.FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4410.FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4417.HypoidGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[HypoidGearSetCompoundModalAnalysisAtAStiffness]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4417.HypoidGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4418.ImportedFEComponentCompoundModalAnalysisAtAStiffness]':
        '''List[ImportedFEComponentCompoundModalAnalysisAtAStiffness]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4418.ImportedFEComponentCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4425.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4425.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4428.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4428.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def mass_discs(self) -> 'List[_4429.MassDiscCompoundModalAnalysisAtAStiffness]':
        '''List[MassDiscCompoundModalAnalysisAtAStiffness]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4429.MassDiscCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def measurement_components(self) -> 'List[_4430.MeasurementComponentCompoundModalAnalysisAtAStiffness]':
        '''List[MeasurementComponentCompoundModalAnalysisAtAStiffness]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4430.MeasurementComponentCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def oil_seals(self) -> 'List[_4432.OilSealCompoundModalAnalysisAtAStiffness]':
        '''List[OilSealCompoundModalAnalysisAtAStiffness]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4432.OilSealCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4434.PartToPartShearCouplingCompoundModalAnalysisAtAStiffness]':
        '''List[PartToPartShearCouplingCompoundModalAnalysisAtAStiffness]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4434.PartToPartShearCouplingCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def planet_carriers(self) -> 'List[_4439.PlanetCarrierCompoundModalAnalysisAtAStiffness]':
        '''List[PlanetCarrierCompoundModalAnalysisAtAStiffness]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4439.PlanetCarrierCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def point_loads(self) -> 'List[_4440.PointLoadCompoundModalAnalysisAtAStiffness]':
        '''List[PointLoadCompoundModalAnalysisAtAStiffness]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4440.PointLoadCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def power_loads(self) -> 'List[_4441.PowerLoadCompoundModalAnalysisAtAStiffness]':
        '''List[PowerLoadCompoundModalAnalysisAtAStiffness]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4441.PowerLoadCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4448.ShaftHubConnectionCompoundModalAnalysisAtAStiffness]':
        '''List[ShaftHubConnectionCompoundModalAnalysisAtAStiffness]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4448.ShaftHubConnectionCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4443.RollingRingAssemblyCompoundModalAnalysisAtAStiffness]':
        '''List[RollingRingAssemblyCompoundModalAnalysisAtAStiffness]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4443.RollingRingAssemblyCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def shafts(self) -> 'List[_4447.ShaftCompoundModalAnalysisAtAStiffness]':
        '''List[ShaftCompoundModalAnalysisAtAStiffness]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4447.ShaftCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4453.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[SpiralBevelGearSetCompoundModalAnalysisAtAStiffness]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4453.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def spring_dampers(self) -> 'List[_4454.SpringDamperCompoundModalAnalysisAtAStiffness]':
        '''List[SpringDamperCompoundModalAnalysisAtAStiffness]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4454.SpringDamperCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4459.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4459.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4462.StraightBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[StraightBevelGearSetCompoundModalAnalysisAtAStiffness]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4462.StraightBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def synchronisers(self) -> 'List[_4465.SynchroniserCompoundModalAnalysisAtAStiffness]':
        '''List[SynchroniserCompoundModalAnalysisAtAStiffness]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4465.SynchroniserCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def torque_converters(self) -> 'List[_4469.TorqueConverterCompoundModalAnalysisAtAStiffness]':
        '''List[TorqueConverterCompoundModalAnalysisAtAStiffness]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4469.TorqueConverterCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4473.UnbalancedMassCompoundModalAnalysisAtAStiffness]':
        '''List[UnbalancedMassCompoundModalAnalysisAtAStiffness]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4473.UnbalancedMassCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4477.WormGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[WormGearSetCompoundModalAnalysisAtAStiffness]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4477.WormGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4480.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearSetCompoundModalAnalysisAtAStiffness]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4480.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value
