'''_5548.py

TorqueConverterConnectionSingleMeshWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _1923
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6228
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5472
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'TorqueConverterConnectionSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionSingleMeshWhineAnalysis',)


class TorqueConverterConnectionSingleMeshWhineAnalysis(_5472.CouplingConnectionSingleMeshWhineAnalysis):
    '''TorqueConverterConnectionSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1923.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1923.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6228.TorqueConverterConnectionLoadCase':
        '''TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6228.TorqueConverterConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
