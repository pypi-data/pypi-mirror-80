'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._749 import HypoidGearDesign
    from ._750 import HypoidGearMeshDesign
    from ._751 import HypoidGearSetDesign
    from ._752 import HypoidMeshedGearDesign
