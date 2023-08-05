'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1008 import AGMA6123SplineHalfRating
    from ._1009 import AGMA6123SplineJointRating
    from ._1010 import DIN5466SplineHalfRating
    from ._1011 import DIN5466SplineRating
    from ._1012 import GBT17855SplineHalfRating
    from ._1013 import GBT17855SplineJointRating
    from ._1014 import SAESplineHalfRating
    from ._1015 import SAESplineJointRating
    from ._1016 import SplineHalfRating
    from ._1017 import SplineJointRating
