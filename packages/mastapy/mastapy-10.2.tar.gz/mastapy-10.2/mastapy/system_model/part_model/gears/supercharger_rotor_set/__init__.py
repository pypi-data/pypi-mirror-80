'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2116 import BoostPressureInputOptions
    from ._2117 import InputPowerInputOptions
    from ._2118 import PressureRatioInputOptions
    from ._2119 import RotorSetDataInputFileOptions
    from ._2120 import RotorSetMeasuredPoint
    from ._2121 import RotorSpeedInputOptions
    from ._2122 import SuperchargerMap
    from ._2123 import SuperchargerMaps
    from ._2124 import SuperchargerRotorSet
    from ._2125 import SuperchargerRotorSetDatabase
    from ._2126 import YVariableForImportedData
