'''_1040.py

BoltGeometryDatabase
'''


from mastapy.utility.databases import _1345
from mastapy.bolts import _1039
from mastapy._internal.python_net import python_net_import

_BOLT_GEOMETRY_DATABASE = python_net_import('SMT.MastaAPI.Bolts', 'BoltGeometryDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltGeometryDatabase',)


class BoltGeometryDatabase(_1345.NamedDatabase['_1039.BoltGeometry']):
    '''BoltGeometryDatabase

    This is a mastapy class.
    '''

    TYPE = _BOLT_GEOMETRY_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltGeometryDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
