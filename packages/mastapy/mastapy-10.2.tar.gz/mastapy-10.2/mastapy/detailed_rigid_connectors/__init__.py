'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._972 import DetailedRigidConnectorDesign
    from ._973 import DetailedRigidConnectorHalfDesign
