'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1811 import Design
    from ._1812 import ComponentDampingOption
    from ._1813 import ConceptCouplingSpeedRatioSpecificationMethod
    from ._1814 import DesignEntity
    from ._1815 import DesignEntityId
    from ._1816 import DutyCycleImporter
    from ._1817 import DutyCycleImporterDesignEntityMatch
    from ._1818 import ExternalFullFELoader
    from ._1819 import HypoidWindUpRemovalMethod
    from ._1820 import IncludeDutyCycleOption
    from ._1821 import MemorySummary
    from ._1822 import MeshStiffnessModel
    from ._1823 import PowerLoadDragTorqueSpecificationMethod
    from ._1824 import PowerLoadInputTorqueSpecificationMethod
    from ._1825 import PowerLoadPIDControlSpeedInputType
    from ._1826 import PowerLoadType
    from ._1827 import RelativeComponentAlignment
    from ._1828 import RelativeOffsetOption
    from ._1829 import SystemReporting
    from ._1830 import TransmissionTemperatureSet
