'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1913 import ClutchConnection
    from ._1914 import ClutchSocket
    from ._1915 import ConceptCouplingConnection
    from ._1916 import ConceptCouplingSocket
    from ._1917 import CouplingConnection
    from ._1918 import CouplingSocket
    from ._1919 import PartToPartShearCouplingConnection
    from ._1920 import PartToPartShearCouplingSocket
    from ._1921 import SpringDamperConnection
    from ._1922 import SpringDamperSocket
    from ._1923 import TorqueConverterConnection
    from ._1924 import TorqueConverterPumpSocket
    from ._1925 import TorqueConverterTurbineSocket
