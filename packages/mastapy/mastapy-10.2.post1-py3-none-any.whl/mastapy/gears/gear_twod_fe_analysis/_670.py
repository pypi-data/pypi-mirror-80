﻿'''_670.py

CylindricalGearTIFFAnalysis
'''


from mastapy.gears.analysis import _952
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TIFF_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.GearTwoDFEAnalysis', 'CylindricalGearTIFFAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearTIFFAnalysis',)


class CylindricalGearTIFFAnalysis(_952.GearDesignAnalysis):
    '''CylindricalGearTIFFAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_TIFF_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearTIFFAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
