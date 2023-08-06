'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._725 import StraightBevelDiffGearDesign
    from ._726 import StraightBevelDiffGearMeshDesign
    from ._727 import StraightBevelDiffGearSetDesign
    from ._728 import StraightBevelDiffMeshedGearDesign
