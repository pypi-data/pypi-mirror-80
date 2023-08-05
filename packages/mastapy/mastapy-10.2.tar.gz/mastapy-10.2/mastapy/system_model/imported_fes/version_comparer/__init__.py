'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1994 import DesignResults
    from ._1995 import ImportedFEResults
    from ._1996 import ImportedFEVersionComparer
    from ._1997 import LoadCaseResults
    from ._1998 import LoadCasesToRun
    from ._1999 import NodeComparisonResult
