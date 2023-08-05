'''_1959.py

ImportedFeLinkWithSelection
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.system_model.imported_fes import (
    _1926, _1956, _1957, _1958,
    _1960, _1961, _1962, _1963,
    _1964, _1965, _1966, _1978,
    _1989, _1990
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_LINK_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFeLinkWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFeLinkWithSelection',)


class ImportedFeLinkWithSelection(_0.APIBase):
    '''ImportedFeLinkWithSelection

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_LINK_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFeLinkWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def add_selected_nodes(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddSelectedNodes

    @property
    def delete_all_nodes(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteAllNodes

    @property
    def select_component(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectComponent

    @property
    def link(self) -> '_1926.ImportedFELink':
        '''ImportedFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1926.ImportedFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_electric_machine_stator_link(self) -> '_1956.ImportedFEElectricMachineStatorLink':
        '''ImportedFEElectricMachineStatorLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1956.ImportedFEElectricMachineStatorLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEElectricMachineStatorLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_gear_mesh_link(self) -> '_1957.ImportedFEGearMeshLink':
        '''ImportedFEGearMeshLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1957.ImportedFEGearMeshLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEGearMeshLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_gear_with_duplicated_meshes_link(self) -> '_1958.ImportedFEGearWithDuplicatedMeshesLink':
        '''ImportedFEGearWithDuplicatedMeshesLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1958.ImportedFEGearWithDuplicatedMeshesLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEGearWithDuplicatedMeshesLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_multi_node_connector_link(self) -> '_1960.ImportedFEMultiNodeConnectorLink':
        '''ImportedFEMultiNodeConnectorLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1960.ImportedFEMultiNodeConnectorLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEMultiNodeConnectorLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_multi_node_link(self) -> '_1961.ImportedFEMultiNodeLink':
        '''ImportedFEMultiNodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1961.ImportedFEMultiNodeLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEMultiNodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_node_link(self) -> '_1962.ImportedFENodeLink':
        '''ImportedFENodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.ImportedFENodeLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFENodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planetary_connector_multi_node_link(self) -> '_1963.ImportedFEPlanetaryConnectorMultiNodeLink':
        '''ImportedFEPlanetaryConnectorMultiNodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.ImportedFEPlanetaryConnectorMultiNodeLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPlanetaryConnectorMultiNodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planet_based_link(self) -> '_1964.ImportedFEPlanetBasedLink':
        '''ImportedFEPlanetBasedLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.ImportedFEPlanetBasedLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPlanetBasedLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planet_carrier_link(self) -> '_1965.ImportedFEPlanetCarrierLink':
        '''ImportedFEPlanetCarrierLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.ImportedFEPlanetCarrierLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPlanetCarrierLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_point_load_link(self) -> '_1966.ImportedFEPointLoadLink':
        '''ImportedFEPointLoadLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1966.ImportedFEPointLoadLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPointLoadLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_multi_angle_connection_link(self) -> '_1978.MultiAngleConnectionLink':
        '''MultiAngleConnectionLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1978.MultiAngleConnectionLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to MultiAngleConnectionLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_rolling_ring_connection_link(self) -> '_1989.RollingRingConnectionLink':
        '''RollingRingConnectionLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.RollingRingConnectionLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to RollingRingConnectionLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_shaft_hub_connection_fe_link(self) -> '_1990.ShaftHubConnectionFELink':
        '''ShaftHubConnectionFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.ShaftHubConnectionFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ShaftHubConnectionFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Link.__class__)(self.wrapped.Link) if self.wrapped.Link else None
