'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._741 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._742 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._743 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._744 import KlingelnbergCycloPalloidHypoidMeshedGearDesign
