'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1510 import CustomLineChart
    from ._1511 import CustomTableAndChart
