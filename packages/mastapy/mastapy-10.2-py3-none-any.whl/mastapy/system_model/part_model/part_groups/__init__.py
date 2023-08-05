'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2048 import ConcentricOrParallelPartGroup
    from ._2049 import ConcentricPartGroup
    from ._2050 import ConcentricPartGroupParallelToThis
    from ._2051 import DesignMeasurements
    from ._2052 import ParallelPartGroup
    from ._2053 import PartGroup
